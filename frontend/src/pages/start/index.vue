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
  
  /* Убрано overflow: hidden для разрешения прокрутки */
  /* Изменен фон на светлый градиент */
  background: linear-gradient(to right, #f0f0f0, #ffffff);
  font-family: "Roboto", sans-serif;    
  /* Изменен цвет текста на темно-серый */
  color: #333333;

  background-image: url('./../../assets/main.webp'); /* Путь к изображению */
  background-size: cover; /* Масштабирование изображения */
  background-repeat: no-repeat; /* Отключение повторения */
  background-position: center; /* Центрирование изображения */
}

@import "../../components/StyleWhite.css";

  
  
</style>