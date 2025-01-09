<script setup>

import navPanel from "./components/NavPanel.vue"
import StartButton from "./components/StartButton.vue"
</script>
<template>
  <div id="app">
    <navPanel />
    <h1>Добро пожаловать в Chrono!</h1>
  </div>
  <div class="content">
    <StartButton />
  </div>
</template>



<style>

@import "../../components/Stiles.css";

  
  
</style>