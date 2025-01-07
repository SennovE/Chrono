<template>
  <div class="page-container">
    <NavBar :username="user.username" />
    <div class="content-container">
      <h1 class="title">My tasks</h1>
      <!-- Секция с дедлайнами -->
      <div class="deadline-wrapper">
        <button class="scroll-button scroll-left" @click="scrollLeft">◀</button>
        <div ref="deadlineList" class="deadline-list">
          <div v-for="(tasks, day) in allDaysWithTasks" :key="day" class="deadline-day">
            <h2 class="day-title">{{ formatDate(day) }}</h2>
            <div class="tasks">
              <div v-if="tasks.length === 0" class="empty-task-card">
                <p>No tasks for this day</p>
              </div>
              <div v-else v-for="task in tasks" :key="task.description" class="task-card">
                <p class="task-name">{{ task.description }}</p>
                <p class="task-time">{{ formatTime(task.deadline_time) }}</p>
                <div class="task-status">
                  <input type="radio" :name="`task-${day}`" />
                </div>
              </div>
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
    const deadlineListRef = ref(null); // Ссылка на список дедлайнов

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
        deadlines.value = response.data;
      } catch (error) {
        console.error("Error fetching deadlines:", error);
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
      const days = Array.from({ length: 7 }, (_, i) => {
        const date = new Date();
        date.setDate(date.getDate() + i);
        return date.toISOString().split("T")[0];
      });

      return days.reduce((result, day) => {
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

    return { user, allDaysWithTasks, formatDate, formatTime, scrollLeft, scrollRight, deadlineListRef };
  },
};
</script>

<style>
/* Основной контейнер */
.page-container {
  display: flex;
}

/* Контейнер контента */
.content-container {
  flex: 1;
  padding: 20px;
  background-color: #f9f9f9;
  overflow-y: auto;
}

.title {
  font-size: 36px; /* Увеличенный шрифт для заголовка */
  font-family: "Poppins", sans-serif; /* Красивый современный шрифт */
  font-weight: bold;
  margin-bottom: 30px;
  text-align: left;
  color: #2c3e50; /* Темно-синий цвет */
}

/* Обёртка для списка дедлайнов и кнопок */
.deadline-wrapper {
  display: flex;
  align-items: center;
  margin-top: 20px;
  position: relative;
}

/* Список дедлайнов */
.deadline-list {
  display: flex;
  gap: 20px;
  overflow: hidden;
  flex: 1;
}

/* Колонка для каждого дня */
.deadline-day {
  flex: 0 0 300px; /* Увеличенная ширина */
  background-color: #ffffff;
  border-radius: 12px; /* Более мягкие края */
  padding: 20px; /* Увеличенный внутренний отступ */
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
  height: 400px; /* Фиксированная высота */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.day-title {
  font-size: 20px; /* Увеличенный размер текста */
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

/* Карточка задачи */
.task-card {
  background-color: #f5f5f5;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.empty-task-card {
  background-color: #eef2f7;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  text-align: center;
  font-size: 14px;
  color: #7f8c8d;
}

/* Кнопки прокрутки */
.scroll-button {
  width: 40px;
  height: 40px;
  background-color: #ffffff; /* Бело-серая кнопка */
  border: 1px solid #ccc;
  border-radius: 50%;
  color: #2c3e50; /* Темно-синий цвет */
  font-size: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  margin: 0 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.scroll-button:hover {
  background-color: #f0f0f0;
  border-color: #b0b0b0;
}

.scroll-left {
  margin-right: -50px;
}

.scroll-right {
  margin-left: -50px;
}
</style>
