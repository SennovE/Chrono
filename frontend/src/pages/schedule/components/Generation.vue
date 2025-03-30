<script setup>
import { ref, defineEmits } from "vue"
import { AIGeneration, SendAISchedule, AIGenerationFullDay } from "./ScheduleFunctions"

const emit = defineEmits(["closeModal"])

const aiInput = ref("")
const aiSchedule = ref("")
const isModalOpen = ref(0)
const isGenerating = ref(false)
const fullDay = ref(false)
const startDate = ref("")

function openModal() {
    isModalOpen.value = 1
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    startDate.value = `${year}-${month}-${day}`;
}

function closeGenModal() {
    isModalOpen.value = 0
    aiSchedule.value = ""
    aiInput.value = ""
    isGenerating.value = false
    emit("closeModal")
}

async function submitAI() {
    aiSchedule.value = ""
    isGenerating.value = true
    if (fullDay.value) {
        aiSchedule.value = await AIGenerationFullDay(aiInput.value, startDate.value)
    } else {
        aiSchedule.value = await AIGeneration(aiInput.value, startDate.value)
    }
    console.log(aiSchedule.value)
    if (typeof aiSchedule.value !== 'string') {
        isModalOpen.value = 2;
    } else {
        aiSchedule.value.forEach(task => {
            task.expanded = false;
        });
    }
    isGenerating.value = false
}

async function sendSchedule() {
    await SendAISchedule(aiSchedule.value);
    closeGenModal();
}

function toggleTask(index) {
    this.aiSchedule[index].expanded = !this.aiSchedule[index].expanded;
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
            <div
                v-if="isModalOpen == 1"
                class="modal-overlay"
                @click="closeGenModal"
            >
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h3>Создать расписание при помощи ИИ</h3>
                        <button class="close-button" @click="closeGenModal">&times;</button>
                    </div>
                    <textarea
                        placeholder="Введите запрос для генерации расписания"
                        v-model="aiInput"
                    ></textarea>
                    <div class="field-group">
                        <p>День события:</p>
                        <div class="input-wrapper">
                            <input
                                type="date"
                                v-model="startDate"
                                class="date"
                            />
                        </div>
                    </div>
                    <div class="field-group">
                        <p>На целый день:</p>
                        <label class="custom-checkbox">
                            <input
                                type="checkbox"
                                v-model="fullDay"
                                :true-value=true
                                :false-value=false
                            />
                            <span class="checkmark"></span>
                        </label>
                    </div>
                    <button
                        v-if="!isGenerating"
                        class="creation-button"
                        @click="submitAI"
                    >
                        Отправить
                    </button>
                    <h4
                        v-else class="error-msg"
                        :style="{ 'text-shadow': 'none' }"
                    >
                        Расписание генерируется, ожидайте
                    </h4>
                    <h4
                        v-if="typeof aiSchedule === 'string'"
                        class="error-msg"
                    >
                        {{ aiSchedule }}
                    </h4>
                </div>
            </div>
        </transition>
        <transition name="overlay-fade">
            <div v-if="isModalOpen == 2" class="modal-overlay" @click="closeGenModal">
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h3>Результат генерации</h3>
                        <button class="close-button" @click="closeGenModal">&times;</button>
                    </div>
                    <div class="result-content">
                        <ul>
                            <div v-for="(task, index) in aiSchedule" :key="task.id">
                                <li>
                                    <div class="field-group">
                                        <div class="input-wrapper">
                                            <input
                                                type="text"
                                                v-model="task.name"
                                                placeholder="Название задачи"
                                            />
                                        </div>
                                        <svg
                                            @click="toggleTask(index)"
                                            width="24"
                                            height="24"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="#3498db"
                                            stroke-width="2"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                            :style="{'padding-left': '1vw', 'cursor': 'pointer'}"
                                        >
                                            <path d="M12 20h9"></path>
                                            <path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                                        </svg>
                                    </div>
                                    <div v-if="task.expanded">
                                        <textarea
                                            placeholder="Добавьте описание"
                                            v-model="task.text"
                                        ></textarea>
                                        <div class="field-group">
                                            <p>Начало:</p>
                                            <div class="input-wrapper">
                                                <input type="datetime-local" v-model="task.start_time" class="date" />
                                            </div>
                                        </div>
                                        <div class="field-group">
                                            <p>Конец:</p>
                                            <div class="input-wrapper">
                                                <input type="datetime-local" v-model="task.end_time" class="date" />
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </div>
                        </ul>
                    </div>
                    <button class="creation-button" @click="sendSchedule">Отправить</button>
                    <button class="creation-button" @click="closeGenModal">Закрыть</button>
                </div>
            </div>
        </transition>
    </div>
</template>

<style scoped>
@import "./ScheduleMain.css";

.result-content {
    max-height: 50vh;
    overflow-y: auto;
    padding-right: 1vw;
}
</style>
