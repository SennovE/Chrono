<script setup>

import navPanel from "./components/NavPanel.vue"
import StartButton from "./components/StartButton.vue"
import ChronoStart from "./components/ChronoStart.vue";
</script>
<template>

  <div class="start-page">
    <navPanel />
    <div class="content">
      <StartButton />
    </div>
    <div>
        <ChronoStart />
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

  background-image: url('./../../assets/main 3.PNG');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

@import "../../components/StyleWhite.css";

@media (max-width: 768px) {
  .start-page {
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    min-height: 100vh;
    background-size: cover;
    background-position: center;
  }
}
</style>