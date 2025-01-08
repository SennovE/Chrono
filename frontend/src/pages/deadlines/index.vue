<template>
  <div class="page-container">
    <NavBar :username="user.username" />
    <div class="content-container">
      <h1 class="title">My tasks</h1>
      <div class="deadline-wrapper">
        <button class="scroll-button scroll-left" @click="scrollLeft">◀</button>
        <div ref="deadlineList" class="deadline-list">
          <div
            v-for="(tasks, day) in allDaysWithTasks"
            :key="day"
            class="deadline-day"
          >
            <h2 class="day-title">{{ formatDate(day) }}</h2>
            <div class="tasks">
              <div v-if="tasks.length === 0" class="empty-task-card">
                <p>No tasks for this day</p>
              </div>
              <div
                v-else
                v-for="task in tasks"
                :key="task.description"
                class="task-card"
              >
                <p class="task-name">{{ task.description }}</p>
                <p class="task-time">{{ formatTime(task.deadline_time) }}</p>
                <div class="task-status">
                  <input
                    type="radio"
                    @change="markTaskAsComplete(task.id)"
                  />
                </div>
              </div>
            </div>
            <div class="new-task-form">
              <input
                v-model="newTask[day].description"
                class="new-task-input"
                type="text"
                placeholder="Task description"
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
        <button class="scroll-button scroll-right" @click="scrollRight">▶</button>
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
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    };

    const formatTime = (datetime) => {
      const time = new Date(datetime);
      return time.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
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
        deadlineList.scrollBy({ left: -300, behavior: "smooth" });
      }
    };

    const scrollRight = () => {
      const deadlineList = deadlineListRef.value;
      if (deadlineList) {
        deadlineList.scrollBy({ left: 300, behavior: "smooth" });
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

.scroll-button {
  background-color: transparent;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #2c3e50;
  margin: 0 10px;
}

.deadline-list {
  display: flex;
  overflow-x: hidden;
  scroll-behavior: smooth;
  flex-wrap: nowrap;
  width: 100%;
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
  max-height: fit-content; /* Ограничиваем высоту только содержимым */
  overflow: hidden; /* Убираем лишний скролл */
}

.tasks {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px; /* Добавляем промежутки между карточками */
  min-height: 50px; /* Минимальная высота для пустого состояния */
}

.empty-task-card {
  color: #aaa;
  font-style: italic;
}

.task-card {
  margin-bottom: 10px;
  border: 1px solid #ebebeb;
  border-radius: 5px;
  padding: 10px;
  background-color: #fafafa;
}

.task-name {
  font-weight: bold;
  margin: 0;
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
</style>
