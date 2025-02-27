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
    background: linear-gradient(to bottom, #f0f0f0, #ffffff);
    background-image: url('./../../assets/main 3.PNG');
    background-size: contain; /* Чтобы полностью вмещалось */
    background-repeat: no-repeat;
    background-position: center center;
    padding: 20px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .start-page h1 {
    font-size: 24px;
    text-align: center;
  }

  .start-page p {
    font-size: 16px;
    text-align: center;
  }
}
  
</style>