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
  display: flex;
  justify-content: center;
  align-items: center;
  height: 70vh;
  margin: 0;
  padding: 0;
  position: absolute;
    top: 220px; /* Указание позиции отдельно */
    left: 900px;
}

.get-started-container::ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.get-started {
  background-color: #ffc1e3; /* Светло-розовый цвет */
  color: #6a1b9a; /* Темно-фиолетовый для контраста */
  border: 2px solid #f48fb1; /* Акцент на границу */
  padding: 20px 70px;
  font-size: 18px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 25px; /* Закругленные края */
  transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
  display: inline-block;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Мягкая тень */
}

.get-started:hover {
  background-color: #f48fb1; /* Более насыщенный розовый */
  transform: translateY(-3px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
}

.get-started:active {
  background-color: #f06292; /* Насыщенный оттенок при нажатии */
  transform: translateY(0);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
