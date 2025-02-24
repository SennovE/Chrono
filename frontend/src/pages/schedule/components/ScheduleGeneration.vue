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
      <svg
        @click="openModal"
        class="svg-buttons"
        viewBox="0 0 80 80"
        xmlns="http://www.w3.org/2000/svg"
        :style="{ 'margin-left': 'auto'}"
      >
        <path d="
          M50 10
          Q50 30 70 30
          Q50 30 50 50
          Q50 30 30 30
          Q50 30 50 10
        " stroke="var(--color-bright-text)" stroke-width="4" fill="none"/>

        <path d="
          M20 30
          Q20 40 30 40
          Q20 40 20 50
          Q20 40 10 40
          Q20 40 20 30
        " stroke="var(--color-bright-text)" stroke-width="4" fill="none"/>

        <path d="
          M30 50
          Q30 60 40 60
          Q30 60 30 70
          Q30 60 20 60
          Q30 60 30 50
        " stroke="var(--color-bright-text)" stroke-width="4" fill="none"/>
      </svg>
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
</style>
