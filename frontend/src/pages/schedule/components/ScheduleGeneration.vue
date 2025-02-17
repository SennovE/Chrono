<script setup>
import { ref, defineEmits } from "vue"
import { AIGeneration, SendAISchedule } from "./ScheduleFunctions"

const emit = defineEmits(['resultGenerated'])
const aiInput = ref("")
const aiSchedule = ref("")
const isModalOpen = ref(false)
const isResultModalOpen = ref(false)

function openModal() {
    isModalOpen.value = true
}
function closeModal() {
    isModalOpen.value = false
    aiSchedule.value = ""
    aiInput.value = ""
}
async function submitAI() {
    aiSchedule.value = await AIGeneration(aiInput.value)
    if (aiSchedule.value !== "") {
        emit('resultGenerated', aiSchedule.value)
        isModalOpen.value = false
        isResultModalOpen.value = true
    }
}
function closeResultModal() {
    isResultModalOpen.value = false
    aiSchedule.value = ""
}

async function sendSchedule() {
    await SendAISchedule(aiSchedule.value);
    closeResultModal();
}

</script>

<template>
    <div>
      <button @click="openModal" class="form-button">
        Создать расписание
      </button>
      <transition name="overlay-fade">
        <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
           <div class="modal-content" @click.stop>
             <div class="modal-header">
                <h2>Создать расписание</h2>
                <button class="close-button" @click="closeModal">&times;</button>
             </div>
             <div class="input-wrapper">
                <input type="text" v-model="aiInput" placeholder="Введите запрос" required/>
             </div>
             <button class="creation-button" @click="submitAI">Отправить</button>
           </div>
        </div>
      </transition>
      <transition name="overlay-fade">
        <div v-if="isResultModalOpen" class="modal-overlay" @click="closeResultModal">
           <div class="modal-content" @click.stop>
             <div class="modal-header">
                <h2>Результат генерации</h2>
                <button class="close-button" @click="closeResultModal">&times;</button>
             </div>
             <div class="result-content">
                <div v-for="task in aiSchedule" :key="task.id">
                  {{ task.name }}
                  {{ task.start_time }}
                </div>
             </div>
             <button class="creation-button" @click="sendSchedule">Отправить</button>
             <button class="creation-button" @click="closeResultModal">Закрыть</button>
           </div>
        </div>
      </transition>
    </div>
  </template>
  
  <style>
  .overlay-fade-enter-from,
  .overlay-fade-leave-to {
    opacity: 0;
  }
  .overlay-fade-enter-active,
  .overlay-fade-leave-active {
    transition: opacity 0.3s ease;
  }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
  }
  .modal-content {
    background: var(--color-container);
    padding: 20px;
    border-radius: 8px;
    width: 300px;
    text-align: center;
  }
  .input-wrapper input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  .creation-button {
    margin-top: 5%;
    margin-bottom: 0;
  }
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1%;
  }
  .close-button {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
  }
  </style>
