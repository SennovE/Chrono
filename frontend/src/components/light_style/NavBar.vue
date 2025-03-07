<template>
  <div class="navigation-container">
    <!-- Блок профиля: аватар и имя пользователя -->
    <div class="user-profile">
      <div class="avatar">
        <img src="../../../public/default_profile.jpg" />
      </div>
      <div class="user-info">
        <p class="username">{{ username }}</p>
      </div>
    </div>

    <!-- Блок статистики задач за день -->
    <div class="daily-stats">
      <div class="stat-item">
        <span class="stat-text">{{ completedCount }} Выполнено</span>
      </div>
      <div class="stat-item">
        <span class="stat-text">{{ incompleteCount }} Невыполнено</span>
      </div>
      <div class="stat-item">
        <span class="stat-text">{{ missedCount }} Пропущено</span>
      </div>
    </div>

    <!-- Группы навигационных ссылок -->
    <nav class="nav-links">
      <router-link
        v-for="link in navLinks"
        :key="link.path"
        :to="link.path"
        class="nav-link"
        active-class="active-link"
      >
        <i :class="link.icon" class="nav-icon"></i>
        <span class="nav-label">{{ link.label }}</span>
      </router-link>
    </nav>

    <!-- Ссылка "О нас" -->
    <div class="about">
      <router-link to="/about" class="about-link">О нас</router-link>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';

export default {
  name: "NavBar",
  props: {
    username: {
      type: String,
      required: true,
    },
  },
  setup() {
    const navLinks = [
      { path: "/profile", label: "Профиль", icon: "fa fa-user" },
      { path: "/settings", label: "Настройки ИИ", icon: "fa fa-cog" },
      { path: "/schedule", label: "Расписание", icon: "fa fa-calendar" },
      { path: "/deadlines", label: "Дедлайны", icon: "fa fa-clock" },
    ];

    const deadlines = ref([]);
    let intervalId = null;

    const getToken = () => {
      const token = localStorage.getItem("chronoJWTToken");
      if (!token) {
        throw new Error("Token is missing. Please log in.");
      }
      return token;
    };
    
    const fetchDeadlines = async () => {
      try {
        const token = getToken();
        const response = await axios.get(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/get_tasks/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        // Преобразуем время дедлайна в ISO-формат
        deadlines.value = response.data.map(task => ({
          ...task,
          deadline_time: new Date(task.deadline_time).toISOString(),
        }));
      } catch (error) {
        console.error("Error fetching deadlines:", error);
      }
    };

    onMounted(() => {
      // Первый вызов сразу при загрузке
      fetchDeadlines();

      // Периодический опрос каждые 30 секунд
      intervalId = setInterval(() => {
        fetchDeadlines();
      }, 30000);
    });

    // Очищаем интервал при размонтировании компонента (во избежание утечек памяти)
    onBeforeUnmount(() => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    });

    // Проверка, что две даты принадлежат одному дню
    const isSameDay = (date1, date2) => {
      return (
        date1.getFullYear() === date2.getFullYear() &&
        date1.getMonth() === date2.getMonth() &&
        date1.getDate() === date2.getDate()
      );
    };

    // Задачи, дедлайн которых сегодня
    const todayDeadlines = computed(() => {
      return deadlines.value.filter(task => {
        const taskDate = new Date(task.deadline_time);
        return isSameDay(taskDate, new Date());
      });
    });

    // Задача выполнена (status === 1)
    const completedCount = computed(() => {
      return todayDeadlines.value.filter(task => task.status === 1).length;
    });

    // Задача невыполнена (status === 0) и дедлайн еще не наступил
    const incompleteCount = computed(() => {
      return todayDeadlines.value.filter(
        task => task.status === 0 && new Date(task.deadline_time) > new Date()
      ).length;
    });

    // Задача пропущена (status === 0) и дедлайн уже прошел
    const missedCount = computed(() => {
      return todayDeadlines.value.filter(
        task => task.status === 0 && new Date(task.deadline_time) <= new Date()
      ).length;
    });

    return {
      navLinks,
      completedCount,
      incompleteCount,
      missedCount,
    };
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

.navigation-container {
  width: 11rem;
  height: 100vh;
  padding: 1.25rem;
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  color: #000;
}

/* Блок профиля с аватаром и ником */
.user-profile {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.avatar {
  margin-right: 0.75rem;
  margin-left: 0.5rem;
}

.avatar img {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  display: flex;
  align-items: center;
}

.username {
  font-size: 1.125rem;
  margin: 0;
}

/* Блок статистики задач за день */
.daily-stats {
  text-align: left;
  font-size: 1.3rem; /* Используем тот же размер, что и у остального текста */
  margin-left: -1.25rem;
}

.stat-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.7rem 1.25rem;
  margin-left: -1.25rem;
  font-size: 0.96rem;
}


.daily-stats .stat-item:nth-child(1) {
  background-color: #dbe3f1;
}

.daily-stats .stat-item:nth-child(2) {
  background-color: #e3e9f3; 
}

.daily-stats .stat-item:nth-child(3) {
  background-color: #f0f4f7;
}

.stat-text {
  margin-left: 2rem;
}

.stat-icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
  color: currentColor;
  -webkit-text-fill-color: transparent;
  -webkit-text-stroke: 1px currentColor;
  margin-left: 0.5rem;
}

/* Группы навигационных ссылок */
.nav-links {
  margin-top: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  font-size: 0.96rem;
  color: #000;
  padding: 0.7rem 1.25rem;
  border: 0.0625rem solid transparent;
  transition: background-color 0.3s, color 0.3s;
  width: calc(100% + 2.5rem);
  margin-left: -1.25rem;
  box-sizing: border-box;
}

.nav-link:hover {
  background-color: #f0f0f0;
}

.nav-icon {
  margin-left: 0.5rem;
  margin-right: 0.625rem;
  font-size: 1rem;
  background: none;
  transition: transform 0.3s;
  -webkit-text-fill-color: transparent;
  -webkit-text-stroke: 1px currentColor;
}

.nav-link:hover .nav-icon {
  transform: scale(1.1);
}

/* Для активной ссылки убираем фон и границы, текст подсвечивается синим */
.active-link {
  background-color: transparent;
  border-color: transparent;
  color: #278fff;
}

.nav-label {
  margin-left: 0;
}

.about {
  text-align: center;
  margin-top: auto;
  margin-bottom: 2rem;
}

.about-link {
  text-decoration: none;
  font-size: 0.875rem;
  color: #555;
  padding: 0.3125rem;
  transition: color 0.3s;
}

.about-link:hover {
  color: #000;
}
</style>
