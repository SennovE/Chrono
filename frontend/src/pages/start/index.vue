<script setup>

import navPanel from "./components/NavPanel.vue"
import StartButton from "./components/StartButton.vue"
</script>
<template>
  <div id="app">
    <navPanel />
  </div>
  <div class="content">
    <StartButton />
  </div>
</template>



<style>

body {
  background-image: url('./../../assets/main.webp'); /* Путь к изображению */
  background-size: cover; /* Масштабирование изображения */
  background-repeat: no-repeat; /* Отключение повторения */
  background-position: center; /* Центрирование изображения */
}

@import "../../components/StyleWhite.css";

  
  
</style>