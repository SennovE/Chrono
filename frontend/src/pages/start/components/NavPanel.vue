<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const navigateTo = (routeName) => {
  router.push({ name: routeName });
};
</script>

<template>
  <div class="top-nav">
    <!-- Левое меню -->
    <ul class="nav-left">
      <li @click="navigateTo('Register')"><b>Регистрация</b></li>
      <li @click="navigateTo('Login Page')"><b>Авторизация</b></li>
    </ul>

    <!-- Центральный текст -->
    <div class="center-text">
      <b>Добро пожаловать в Chrono!</b>
    </div>

    <!-- Правое меню -->
    <ul class="nav-right">
      <li @click="navigateTo('Profile Page')"><b>Профиль</b></li>
    </ul>
  </div>
</template>

<style scoped>
.top-nav {
  width: 100%;
  background: linear-gradient(to left, var(--color-briter-black), var(--color-black));
  position: fixed;
  top: 0;
  left: 0;
  box-shadow: 0px 0px 20px var(--color-deep-purple);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px; /* Отступы по бокам */
  height: 60px; /* Фиксированная высота панели */
}

/* Левое и правое меню */
.nav-left,
.nav-right {
  display: flex;
  list-style-type: none;
  margin: 0;
  padding: 0;
}

.nav-left li,
.nav-right li {
  padding: 15px 20px;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s, text-shadow 0.3s;
  cursor: pointer;
  color: white; /* Цвет текста */
}

.nav-left li:hover,
.nav-right li:hover {
  background-color: rgba(255, 255, 255, 0.1); /* Легкий эффект при наведении */
  text-shadow: 0px 0px 5px var(--color-deep-purple);
}

/* Центральный текст */
.center-text {
  position: absolute; /* Абсолютное позиционирование относительно .top-nav */
  left: 50%;
  transform: translateX(-50%);
  color: var(--color-grey-purple);
  font-size: 18px;
  font-weight: bold;
  text-shadow: 0px 0px 5px var(--color-deep-purple);
  pointer-events: none; /* Чтобы клики проходили сквозь текст, если нужно */
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .top-nav {
    flex-direction: column;
    align-items: flex-start;
    height: auto;
    padding: 10px;
  }

  .nav-left,
  .nav-right {
    flex-direction: column;
    width: 100%;
  }

  .nav-left li,
  .nav-right li {
    width: 100%;
    text-align: center;
  }

  .center-text {
    position: static;
    transform: none;
    margin: 10px 0;
    text-align: center;
  }
}
</style>
