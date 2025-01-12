<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<template>
  <div class="get-started-container">
    <ul>
      <li @click="router.push({ name: 'Registration' })" class="get-started">
        <b>Начать</b>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.get-started-container {
    display: flex; /* Включает flexbox */
  justify-content: center; /* Центрирование по горизонтали */
  align-items: center; /* Центрирование по вертикали */
  height: 70vh; /* Высота контейнера на весь экран */
  margin: 0; /* Убираем отступы */
  padding: 0; /* Убираем внутренние отступы */
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.get-started {
  background-color: #000000;
  color: #ffffff;
  border: none;
  padding: 30px 90px;
  font-size: 20px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
  display: inline-block;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.get-started:hover {
  background-color: #1a1a1a;
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.get-started:active {
  background-color: #333333;
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
