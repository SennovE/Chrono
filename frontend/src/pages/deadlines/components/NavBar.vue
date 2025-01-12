<template>
    <div class="navigation-container">
      <!-- Имя пользователя -->
      <div class="user-info">
        <p class="username">{{ username }}</p>
      </div>
  
      <!-- Навигационные ссылки -->
      <nav class="nav-links">
        <router-link
          v-for="link in navLinks"
          :key="link.path"
          :to="link.path"
          class="nav-link"
          active-class="active-link"
        >
          {{ link.label }}
        </router-link>
      </nav>
  
      <!-- Ссылка "О нас" -->
      <div class="about">
        <router-link to="/about" class="about-link">О нас</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "NavBar",
    props: {
      username: {
        type: String,
        required: true, // Передаем имя пользователя через props
      },
    },
    setup() {
      const navLinks = [
        { path: "/profile", label: "Профиль" },
        { path: "/settings", label: "Настройки" },
        { path: "/schedule", label: "Расписание" },
        { path: "/deadlines", label: "Дедлайны" },
      ];
  
      return { navLinks };
    },
  };
  </script>
  
  <style>
  .navigation-container {
    width: 250px;
    height: 100vh;
    background-color: #2c3e50; /* Мягкий темно-синий */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
    color: #ecf0f1; /* Светлый текст */
  }
  
  /* Имя пользователя */
  .user-info {
    text-align: center;
    margin-bottom: 40px;
  }
  
  .username {
    font-size: 18px;
    font-weight: bold;
    color: #ecf0f1;
  }
  
  /* Стили для навигационных ссылок */
  .nav-links {
    flex: 1; /* Центрируем ссылки в колонке */
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 15px;
  }
  
  .nav-link {
    text-decoration: none;
    font-size: 16px;
    color: #ecf0f1; /* Светлый текст */
    padding: 10px 15px;
    border-radius: 5px;
    transition: background-color 0.3s, color 0.3s;
  }
  
  .nav-link:hover {
    background-color: #34495e; /* Подсветка при наведении */
    color: #1abc9c; /* Акцентный цвет */
  }
  
  .active-link {
    background-color: #1abc9c; /* Активный цвет */
    color: #2c3e50; /* Темный текст */
  }
  
  /* Ссылка "О нас" */
  .about {
    margin-bottom: 20px; /* Поднимаем чуть выше нижнего края */
    text-align: center;
  }
  
  .about-link {
    text-decoration: none;
    font-size: 14px;
    color: #bdc3c7; /* Светлый серый */
    padding: 5px;
    transition: color 0.3s;
  }
  
  .about-link:hover {
    color: #1abc9c; /* Акцентный цвет */
  }
  </style>
  