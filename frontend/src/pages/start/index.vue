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
  background-image: url('https://raw.githubusercontent.com/SennovE/Chrono/refs/heads/main/cf7f19d7-4d43-42e5-863f-9d003a3ac834.webp?token=GHSAT0AAAAAAC3XUAU6KMTNSTGG5A4CTP6KZ4NPQQQ'); /* Путь к изображению */
  background-size: cover; /* Масштабирование изображения */
  background-repeat: no-repeat; /* Отключение повторения */
  background-position: center; /* Центрирование изображения */
}

@import "../../components/StyleWhite.css";

  
  
</style>