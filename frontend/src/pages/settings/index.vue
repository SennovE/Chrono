<script setup>
import { ref } from 'vue'
const isRecordingStarted = ref(false);
const RerodingStateFuntion = () => {
  if (!isRecordingStarted.value) {
    isRecordingStarted.value = true;
  } else {
    isRecordingStarted.value = false;
  }
};
</script>

<template>
  <div class="record-interface">
    <ul>
      <li @click="RerodingStateFuntion" class="Record-Button">
        <b>{{ isRecordingStarted ? 'Остановить запись' : 'Начать запись' }}</b>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.record-interface {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  padding: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.record-interface ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.Record-Button {
  margin: 100px 0 0;
  background-color: #2d2d2d; 
  color: #ffffff; 
  border: 2px solid #444444; 
  padding: 18px 60px;
  font-size: 18px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 30px; /* Закругленные края */
  transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
  display: inline-block;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Мягкая тень */
}

.Record-Button:hover {
  background-color: #444444; /* Более насыщенный оттенок */
  transform: translateY(-3px);
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25);
}

.Record-Button:active {
  background-color: #555555;
  transform: translateY(0);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* Мобильная версия */
@media (max-width: 768px) {
  .get-started-container {
    position: relative;
    top: 0;
    left: 0;
    transform: none;
    margin: 0;
    padding: 30px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  

  .get-started {
    width: 120%;
    margin: 30px auto;
    padding: 12px 0;
    font-size: 14px;
    text-align: center;
    border-radius: 30px;
    margin: -10px 10px 10px -55%; 
  }
}
</style>