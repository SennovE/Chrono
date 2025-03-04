<template>
  <div class="navigation-container">
    <!-- Блок профиля: аватар и имя пользователя -->
    <div class="user-profile">
      <div class="avatar">
        <img src="../../../../public/logo.png" />
      </div>
      <div class="user-info">
        <p class="username">{{ username }}</p>
      </div>
    </div>

    <!-- Тонкая серая линия -->
    <!-- <div class="divider"></div> -->

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
      { path: "/settings", label: "Настройки", icon: "fa fa-cog" },
      { path: "/schedule", label: "Расписание", icon: "fa fa-calendar" },
      { path: "/deadlines", label: "Дедлайны", icon: "fa fa-clock" },
    ];

    return { navLinks };
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

/* Тонкая серая линия – увеличена ширина до 90% */
.divider {
  height: 1px;
  background-color: #ccc;
  width: 90%;
  margin-left: 0.75rem;
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
  border-radius: 0.25rem;
  transition: background-color 0.3s, color 0.3s;
  width: calc(100% + 2.5rem);
  margin-left: -1.25rem;
  box-sizing: border-box;
}

.nav-link:hover {
  background-color: #f0f0f0;
}

/* Анимация для иконок */
.nav-icon {
  margin-left: 0.5rem; /* Иконки отступают слева */
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
  color: #4da3ff;
}

/* Убираем отступ у текста, чтобы сдвиг производился только для иконки */
.nav-label {
  margin-left: 0;
}

/* Стили для ссылки "О нас" */
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
