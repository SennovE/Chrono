<template>
    <div class="top-nav">
        <ul>
            <li @click="router.push({name: 'Welcome'})"><b>Главная</b></li>
            <li @click="router.push({name: 'Schedule Page'})"><b>Расписание</b></li>
            <li @click="router.push({name: 'Deadlines Page'})"><b>Дедлайны</b></li>
            <li
                class="right-button"
                @click="router.push({name: 'Profile Page'})"
            ><b>Профиль</b></li>
        </ul>
    </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<style scoped>
:root {
  --color-pastel-pink: #ffc1e3;
  --color-pastel-purple: #d1c4e9;
  --color-light-purple: #b39ddb;
  --color-pastel-yellow: #fff9c4;
  --color-soft-grey: #f5f5f5;
}

.top-nav {
  width: 100%;
  background: linear-gradient(to right, var(--color-pastel-pink), var(--color-pastel-purple));
  position: fixed;
  top: 0;
  left: 0;
  box-shadow: 
      0px 4px 8px rgba(0, 0, 0, 0.1),
      0px 6px 10px rgba(0, 0, 0, 0.1);
  z-index: 999;
  padding: 10px 20px; /* Добавлен внутренний отступ */
  border-bottom: 3px solid var(--color-light-purple); /* Мягкий акцент */
}

.top-nav ul {
  display: flex;
  list-style-type: none;
  justify-content: flex-start;
  align-items: center;
  margin: 0;
  padding: 0;
}

.top-nav li {
  display: block;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 25px; /* Закругленные края */
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  cursor: pointer;
  color: #6a1b9a; /* Нежный фиолетовый */
  font-weight: bold;
  background-color: var(--color-soft-grey); /* Нежный светлый фон */
}

.top-nav li:hover {
  background-color: var(--color-light-purple); /* Светло-фиолетовый фон при наведении */
  color: #4a148c; /* Глубокий фиолетовый текст при наведении */
  box-shadow: 0px 4px 12px rgba(106, 27, 154, 0.3); /* Фиолетовая тень при наведении */
}

.right-button {
  margin-left: auto;
  margin-right: 2%;
}

@media (max-width: 768px) {
  .top-nav ul {
      flex-direction: column;
      align-items: flex-start;
  }

  .right-button {
      margin-left: 0;
      margin-top: 10px;
  }

  .top-nav li {
      padding: 10px 15px;
  }
}
</style>
