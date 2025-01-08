<template>
  <div class="page-container">
    <NavBar :username="user.username" />
    <div class="content-container">
      <h1 class="title">My tasks</h1>
      <div class="deadline-wrapper">
        <button class="scroll-button scroll-left" @click="scrollLeft" aria-label="Scroll Left">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="#7f8c8d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div ref="deadlineListRef" class="deadline-list">
          <div
            v-for="(tasks, day) in allDaysWithTasks"
            :key="day"
            class="deadline-day-wrapper"
          >
            <h2 class="day-title">{{ formatDate(day) }}</h2> <!-- Вынесли заголовок -->
            <div class="deadline-day">
              <div class="tasks">
                <div v-if="tasks.length === 0" class="empty-task-card">
                  <p>Все задачи завершены!</p>
                </div>
                <div
                  v-else
                  v-for="task in tasks"
                  :key="task.id"
                  class="task-card"
                >
                  <div class="task-status">
                    <input
                      type="radio"
                      @change="markTaskAsComplete(task.id)"
                    />
                  </div>
                  <div class="task-details">
                    <p class="task-name">{{ task.description }}</p>
                    <div class="task-time-container">
                      <svg class="time-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"></path>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                      </svg>
                      <p class="task-time">{{ formatTime(task.deadline_time) }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div class="new-task-form">
                <input
                  v-model="newTask[day].description"
                  class="new-task-input"
                  type="text"
                  placeholder="Add task"
                />
                <input
                  v-model="newTask[day].time"
                  class="new-task-time"
                  type="time"
                />
                <button
                  class="create-task-button"
                  @click="createTask(day)"
                  title="Add Task"
                >
                  ↑
                </button>
              </div>
            </div>
          </div>
        </div>
        <button class="scroll-button scroll-right" @click="scrollRight" aria-label="Scroll Right">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="#7f8c8d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";
import NavBar from "./components/NavBar.vue";

export default {
  name: "DeadlinePage",
  components: { NavBar },
  setup() {
    const user = ref({ username: "Loading..." });
    const deadlines = ref([]);
    const deadlineListRef = ref(null);

    // Initialize tasks storage per day
    const newTask = ref({});

    const getToken = () => {
      const token = localStorage.getItem("chronoJWTToken");
      if (!token) {
        throw new Error("Token is missing. Please log in.");
      }
      return token;
    };

    const fetchUser = async () => {
      try {
        const token = getToken();
        const response = await axios.get("http://localhost:8080/api/v1/user/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        user.value = response.data;
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    };

    const fetchDeadlines = async () => {
      try {
        const token = getToken();
        const response = await axios.get(
          "http://localhost:8080/api/v1/deadline_task/get_tasks/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        deadlines.value = response.data.filter((task) => task.status === 0);
      } catch (error) {
        console.error("Error fetching deadlines:", error);
      }
    };

    const createTask = async (day) => {
      if (!newTask.value[day]) {
        newTask.value[day] = { description: "", time: "" };
      }
      try {
        const token = getToken();
        const deadline_time = `${day}T${newTask.value[day].time}:00`;
        const description = newTask.value[day].description;

        const response = await axios.post(
          "http://localhost:8080/api/v1/deadline_task/create_deadline_task",
          { description, deadline_time },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        console.log("Task created:", response.data);

        // Clear the form for this day
        newTask.value[day] = { description: "", time: "" };
        await fetchDeadlines();
      } catch (error) {
        console.error("Error creating task:", error);
      }
    };

    const groupedDeadlines = computed(() => {
      return deadlines.value.reduce((groups, task) => {
        const dateKey = task.deadline_time.split("T")[0];
        if (!groups[dateKey]) {
          groups[dateKey] = [];
        }
        groups[dateKey].push(task);
        return groups;
      }, {});
    });

    const allDaysWithTasks = computed(() => {
      const days = Array.from({ length: 30 }, (_, i) => {
        const date = new Date();
        date.setDate(date.getDate() + i);
        return date.toISOString().split("T")[0];
      });

      return days.reduce((result, day) => {
        if (!newTask.value[day]) {
          newTask.value[day] = { description: "", time: "" };
        }
        result[day] = groupedDeadlines.value[day] || [];
        return result;
      }, {});
    });

    const formatDate = (dateString) => {
      const today = new Date();
      const tomorrow = new Date();
      tomorrow.setDate(today.getDate() + 1);

      const date = new Date(dateString);

      if (date.toDateString() === today.toDateString()) {
        return `Today, ${date.toLocaleDateString("en-US", { month: "long", day: "numeric" })}`;
      }

      if (date.toDateString() === tomorrow.toDateString()) {
        return `Tomorrow, ${date.toLocaleDateString("en-US", { month: "long", day: "numeric" })}`;
      }

      return date.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric",
      });
    };
    const formatTime = (datetime) => {
      const time = new Date(datetime);
      return time.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      });
    };

    const markTaskAsComplete = async (taskId) => {
    try {
      const token = getToken();
      if (!token) {
        throw new Error("Token is missing. Please log in.");
      }

      // Отправляем запрос для завершения задачи
      await axios.post(
        "http://localhost:8080/api/v1/deadline_task/complete_task",
        { id: taskId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // Обновляем список задач после выполнения
      await fetchDeadlines();
    } catch (error) {
      console.error("Error completing task:", error);
    }
  };

    const scrollLeft = () => {
      const deadlineList = deadlineListRef.value;
      if (deadlineList) {
        deadlineList.scrollBy({ left: -500, behavior: "smooth" });
      }
    };

    const scrollRight = () => {
      const deadlineList = deadlineListRef.value;
      if (deadlineList) {
        deadlineList.scrollBy({ left: 500, behavior: "smooth" });
      }
    };

    onMounted(async () => {
      await fetchUser();
      await fetchDeadlines();
    });

    return {
      user,
      allDaysWithTasks,
      formatDate,
      formatTime,
      scrollLeft,
      scrollRight,
      deadlineListRef,
      newTask,
      createTask,
      markTaskAsComplete
    };
  },
};
</script>

<style scoped>
.page-container {
  display: flex;
  min-height: 100vh;
  box-sizing: border-box;
}

.content-container {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
  background-color: #f8f9fa;
}

.title {
  margin-bottom: 20px;
}

.deadline-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.deadline-list {
  display: flex;
  overflow-x: auto; /* Изменено с hidden на auto */
  scroll-behavior: smooth;
  flex-wrap: nowrap;
  width: 100%;
  
  /* Дополнительные стили для скрытия полосы прокрутки (опционально) */
  -ms-overflow-style: none; /* Для IE и Edge */
  scrollbar-width: none; /* Для Firefox */
}

/* Скрытие полосы прокрутки для WebKit-браузеров (Chrome, Safari, Edge) */
.deadline-list::-webkit-scrollbar {
  display: none;
}

.deadline-day {
  display: flex;
  flex-direction: column;
  flex-shrink: 0; /* Удерживаем фиксированную ширину */
  width: 300px;
  margin-right: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.tasks {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 50px;
  /* Добавляем: */
  width: 100%;
}

.empty-task-card {
  color: #9e9e9e; /* Темный серый цвет текста */
  font-style: normal; /* Убираем курсив */
  text-align: center; /* Центрируем текст */
  display: flex; /* Добавляем flexbox для выравнивания */
  justify-content: center; /* Горизонтальное выравнивание */
  align-items: center; /* Вертикальное выравнивание */
  min-height: 50px; /* Обеспечиваем минимальную высоту блока */
}

.task-card {
  display: flex;
  align-items: center; /* Изменено с center на flex-start для верхнего выравнивания */
  margin-bottom: 10px;
  border: 1px solid #ebebeb;
  border-radius: 5px;
  padding: 10px;
  background-color: #fafafa;
  gap: 10px;
  word-wrap: break-word;
  
  /* Добавляем flex-direction: column для вертикального расположения при необходимости */
  flex-direction: row;
  
  /* Убираем фиксированную высоту, если есть */
  height: auto;
}

.task-status {
  flex-shrink: 0; /* Чекбокс фиксированного размера */
  display: flex;
  align-items: center;
}

.task-status input {
  width: 15px;
  height: 15px;
  cursor: pointer; /* Курсор в виде руки */
}

.task-details {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-wrap: break-word;
  word-break: break-word; /* Добавлено для лучшего переноса */
}

/* Дополнительные улучшения для .task-name */
.task-name {
  font-weight: bold;
  margin: 0;
  word-wrap: break-word;
  white-space: normal;
  /* Добавляем: */
  overflow: hidden;
}

.task-time {
  margin: 5px 0 0;
  font-size: 0.9rem;
  color: #555;
}

.new-task-form {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.new-task-input {
  flex: 2;
  padding: 5px;
  height: 35px; /* Уменьшаем высоту */
  border: 2px solid #ccc; /* Толстая серая граница */
  border-radius: 50px; /* Почти овальная форма */
  font-size: 0.9rem; /* Уменьшаем шрифт */
  color: #555;
  background-color: white; /* Белый фон */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* Лёгкая тень */
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  box-sizing: border-box;
}

.new-task-input:focus {
  border-color: #3498db; /* Подсветка границы при фокусе */
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5); /* Лёгкая подсветка */
}

.new-task-time {
  flex: 1;
  padding: 5px;
  height: 35px; /* Такой же размер, как у описания */
  border: 2px solid #ccc; /* Толстая серая граница */
  border-radius: 50px; /* Почти овальная форма */
  font-size: 0.9rem; /* Уменьшаем шрифт */
  text-align: center; /* Центрируем текст */
  color: #555; /* Серый цвет текста */
  appearance: none; /* Убираем стандартное оформление браузера */
  background-color: white; /* Белый фон */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); /* Лёгкая тень */
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  box-sizing: border-box;
}

.new-task-time:focus {
  border-color: #3498db; /* Подсветка границы при фокусе */
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5); /* Лёгкая подсветка */
}

.new-task-time::placeholder {
  color: #aaa; /* Цвет для `--:--` */
  font-style: italic; /* Наклонный текст */
}

/* Убираем значок часов */
.new-task-time::-webkit-calendar-picker-indicator {
  display: none; /* Убираем значок в Chrome и Edge */
}

.create-task-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px; /* Размер кнопки */
  height: 40px; /* Размер кнопки */
  color: gray; /* Серый цвет стрелки */
  font-size: 1.2rem;
  border: none; /* Убираем границы */
  background-color: transparent; /* Убираем фон */
  cursor: pointer;
  transition: transform 0.2s;
}

.create-task-button:hover {
  transform: scale(1.1); /* Увеличиваем размер при наведении */
}

.deadline-day-wrapper {
  display: flex;
  flex-direction: column;
  margin-right: 20px;
}

.day-title {
  margin-bottom: 10px; /* Отступ между заголовком и карточкой */
  font-size: 1.5rem; /* Размер шрифта */
  color: #333; /* Цвет текста */
  text-align: center; /* Центровка текста */
}

.deadline-day {
  background-color: #ffffff;
  border-radius: 20px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  width: 300px;
}
.scroll-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  background-color: white;
  border: 2px solid #bdc3c7; /* Серая граница */
  border-radius: 50%; /* Круглая форма */
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
}

.scroll-button:hover {
  background-color: #ecf0f1; /* Немного серого при наведении */
  transform: scale(1.05); /* Лёгкое увеличение при наведении */
}

.scroll-button:active {
  transform: scale(0.95); /* Небольшое уменьшение при нажатии */
}

.scroll-left {
  margin-right: 10px;
}

.scroll-right {
  margin-left: 10px;
}

.task-time-container {
  display: flex;
  align-items: center; /* Выравниваем значок и текст по вертикали */
  gap: 5px; /* Расстояние между значком и временем */
}

.time-icon {
  width: 12px; /* Уменьшенный размер значка */
  height: 12px; /* Уменьшенный размер значка */
  color: #555; /* Цвет значка */
  flex-shrink: 0; /* Убираем сжатие значка */
}

.task-time {
  font-size: 0.9rem; /* Размер шрифта времени */
  margin: 0; /* Убираем лишние отступы */
  line-height: 1; /* Выравниваем текст по вертикали */
  position: relative; /* Для выравнивания */
  top: 0px; /* Поднимаем текст чуть выше */
}
</style>
