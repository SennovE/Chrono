<template>
  <div class="top-nav">
      <ul>
          <li @click="router.push({name: 'Registation'})"><b>Регистрация</b></li>
          <li @click="router.push({name: 'Login Page'})"><b>Авторизация</b></li>
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
.top-nav {
  width: 100%;
  background: linear-gradient(to left, var(--color-brighter-black), var(--color-dark-grey));
  position: fixed;
  top: 0;
  left: 0;
  box-shadow: 
      0px 2px 4px rgba(0, 0, 0, 0.1),
      0px 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 999;
  padding: 0 20px; /* Добавлен внутренний отступ */
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
  padding: 15px 20px;
  text-decoration: none;
  border-radius: 5px;    
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  cursor: pointer;
  color: var(--color-black); /* Темно-серый текст */
  font-weight: bold;
}

.top-nav li:hover {
  background-color: var(--color-dark-grey); /* Светло-серый фон при наведении */
  color: var(--color-deep-purple); /* Пурпурный текст при наведении */
  box-shadow: 0px 4px 8px rgba(136, 0, 255, 0.2); /* Пурпурная тень при наведении */
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
