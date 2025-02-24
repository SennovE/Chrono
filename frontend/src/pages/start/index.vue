<script setup>

import navPanel from "./components/NavPanel.vue"
import StartButton from "./components/StartButton.vue"
</script>
<template>

  <div class="start-page">
    <navPanel />
    <div class="content">
      <StartButton />
    </div>

  </div>
</template>



<style>

.start-page {
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: 100;
  background: linear-gradient(to right, #f0f0f0, #ffffff);
  font-family: "Roboto", sans-serif;    
  color: #333333;

  background-image: url('./../../assets/main2.PNG'); /* Путь к изображению */
  background-size: cover; /* Масштабирование изображения */
  background-repeat: no-repeat; /* Отключение повторения */
  background-position: center; /* Центрирование изображения */
}

@import "../../components/StyleWhite.css";

@media (max-width: 768px) {
  .start-page {
    /* Можно изменить направление градиента или отступы, если потребуется */
    background: linear-gradient(to bottom, #f0f0f0, #ffffff);
    background-image: url('./../../assets/main2.PNG'); /* Используем то же изображение */
    background-size: cover;
    background-position: center;
    padding: 20px;
    box-sizing: border-box;
  }
}
  
</style>