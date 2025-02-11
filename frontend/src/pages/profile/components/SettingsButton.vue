<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<template>
  <div class="get-started-container_kera">
    <ul>
      <li @click="router.push({ name: 'Profile Page' })" class="get-started">
        <b>Настройки</b>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.get-started-container_kera {
    display: flex; /* Включает flexbox */
    position: absolute;
    top: 400px; /* Указание позиции отдельно */
    left: 160px;

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
  background-color: #ffffff;
  color: #000000;
  border: none;
  padding: 20px 80px;
  font-size: 10px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
  display: inline-block;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.get-started:hover {
  background-color: #e0e0e0;
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.get-started:active {
  background-color: #333333;
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
