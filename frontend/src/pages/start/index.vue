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

  
body {
    overflow: hidden;
    background: linear-gradient(to right, var(--color-briter-black), var(--color-black));
    font-family: "Roboto", sans-serif;    
    color: var(--color-grey);
}
::selection {
    color: var(--color-deep-purple);
    background: rgba(128, 128, 128, 0.087);
    border-radius: 5px;
}
  @import "./components/styel.css";

  
  
</style>