<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { addScheduleTask } from "./ScheduleFunctions"

const router = useRouter()

const shortText = ref("")
const descriptionText = ref("")
const startDate = ref("")
const endDate = ref("")
const recurring = ref(false)

const response = ref("")

const isModalOpen = ref(false)

// TODO: добавить shortText в backend

async function addScheduleTaskWrap() {
    response.value = await addScheduleTask(
        router,
        descriptionText.value,
        startDate.value,
        endDate.value,
        recurring.value
    )
}

function modalClose() {
    response.value = ""
    isModalOpen.value = false
}
</script>

<template>
    <div>
        <button @click="isModalOpen=true">Добавить событие</button>
        <transition name="overlay-fade">
            <div 
                v-if="isModalOpen" 
                class="modal-overlay"
                @click="modalClose"
            >   
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h2>Добавить новое событие</h2>
                        <button class="close-button" @click="modalClose">
                            &times;
                        </button>
                    </div>
                    <input placeholder="Название события" v-model="shortText" />
                    <textarea placeholder="Добавьте описание" v-model="descriptionText"></textarea>
                    
                    <div class="field-group">
                        <p>Начало:</p>
                        <input type="datetime-local" v-model="startDate" class="date" />
                    </div>

                    <div class="field-group">
                        <p>Конец:</p>
                        <input type="datetime-local" v-model="endDate" class="date" />
                    </div>

                    <div class="field-group">
                        <p>Повторяющееся:</p>
                        <label class="custom-checkbox">
                            <input type="checkbox" v-model="recurring" />
                            <span class="checkmark"></span>
                        </label>
                    </div>

                    <button class="creation-button" @click="addScheduleTaskWrap">Создать</button>
                    <h3 class="error-msg" v-show="response">{{ response }}</h3>
                </div>
            </div>
        </transition>
    </div>
</template>


<style>
.date {
    color: var(--color-grey);
}

.creation-button {
    margin-top: 2%;
    margin-bottom: 0;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1%;
}

.schedule-container .close-button {
    font-size: 24px;
    cursor: pointer;
    margin: 0;
    padding: 0;
    width: 10%;
    z-index: 999;
}

.field-group {
    display: flex;
    align-items: center;
    margin-bottom: 1%;
}

.field-group p {
    width: 25%;
    margin: 0;
    text-align: left;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #00000045;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.modal-content {
    background: linear-gradient(to left, var(--color-briter-black), var(--color-black));
    padding: 20px;
    border-radius: 8px;
    box-sizing: border-box;
    border: 1px solid var(--color-black);
    box-shadow: 0 0 10px var(--color-deep-purple);
}
.modal-overlay textarea {
    height: 200px;
    resize: none;
    overflow: auto;
    font-size: large;
}

.overlay-fade-enter-from,
.overlay-fade-leave-to {
  opacity: 0;
}
.overlay-fade-enter-active,
.overlay-fade-leave-active {
  transition: opacity 0.3s ease;
}
</style>