<script setup>
/* eslint-disable */
import { ref, defineEmits, watch } from "vue"
import { useRouter } from "vue-router"
import { deleteTask, updateTask } from "./ScheduleFunctions"

const emit = defineEmits(['taskUpdated', "closeModal", "clearUpdatingInfo"])
const router = useRouter()

const shortText = ref("")
const descriptionText = ref("")
const startDate = ref("")
const startDateString = ref("")
const startTime = ref("")
const endTime = ref("")
const recurring = ref(false)

const response = ref("")

const isModalUpdateOpen = ref(0)

const props = defineProps({
    tasks: Object,
    showTaskDay: String,
    showTaskId: String,
})

async function deleteTaskWrap() {
    await deleteTask(router, props.showTaskId)
    modalClose()
    emit('taskUpdated')
}

async function updateTaskWrap() {
    response.value = await updateTask(
        router,
        props.showTaskId,
        shortText.value,
        descriptionText.value,
        startDate.value,
        startTime.value,
        endTime.value,
        recurring.value
    )
    if (response.value == "") {
        modalClose()
        emit('taskUpdated')
    }
}

function modalClose() {
    response.value = ""
    isModalUpdateOpen.value = 0
    emit("clearUpdatingInfo")
}

function showTaskById() {
    if (props.showTaskId == -1) return
    const selectedTask = props.tasks[props.showTaskDay].find(task => task.id === props.showTaskId)
    shortText.value = selectedTask.name
    descriptionText.value = selectedTask.text
    startDate.value = `${selectedTask.year}-` +
                      (selectedTask.month < 10 ? '0' : '') + `${selectedTask.month}-` +
                      (selectedTask.day < 10 ? '0' : '') + `${selectedTask.day}`
    startDateString.value = (selectedTask.day < 10 ? '0' : '') + `${selectedTask.day}.` +
                      (selectedTask.month < 10 ? '0' : '') + `${selectedTask.month}.` +
                      `${selectedTask.year}`
    startTime.value = (selectedTask.start_hours < 10 ? '0' : '') +
                      `${selectedTask.start_hours}:` +
                      (selectedTask.start_minutes < 10 ? '0' : '') +
                      `${selectedTask.start_minutes}`
    endTime.value = (selectedTask.end_hours < 10 ? '0' : '') +
                    `${selectedTask.end_hours}:` +
                    (selectedTask.end_minutes < 10 ? '0' : '') +
                    `${selectedTask.end_minutes}`
    recurring.value = selectedTask.recurring
    isModalUpdateOpen.value = 1
}

watch(() => props.showTaskId, showTaskById)
</script>

<template>
    <div>
        <transition name="overlay-fade">
            <div 
                v-if="isModalUpdateOpen" 
                class="modal-overlay"
                @click="modalClose"
            >   
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h2 v-if="isModalUpdateOpen == 2">Изменить событие</h2>
                        <h2 v-else>{{ shortText }}</h2>
                        <div class="edit-button" @click="isModalUpdateOpen = 2">
                            <svg v-if="isModalUpdateOpen == 1" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 20h9"></path>
                                <path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                            </svg>
                        </div>
                        <button class="close-button" @click="modalClose">
                            &times;
                        </button>
                    </div>
                    <div v-if="isModalUpdateOpen == 2" class="input-wrapper">
                        <input placeholder="Название события" v-model="shortText" />
                    </div>
                    <p></p>
                    <textarea v-if="isModalUpdateOpen == 2" placeholder="Добавьте описание" v-model="descriptionText"></textarea>
                    <pre v-else class="task-text">{{ !descriptionText ? "Без описания" : descriptionText }}</pre>

                    <div class="field-group">
                        <p>День события:</p>
                        <div class="input-wrapper">
                            <input v-if="isModalUpdateOpen == 2" type="date" v-model="startDate" class="date" />
                            <pre v-else>{{ startDateString }}</pre>
                        </div>
                    </div>
                    
                    <div class="field-group">
                        <p>Начало:</p>
                        <div class="input-wrapper">
                            <input v-if="isModalUpdateOpen == 2" type="time" v-model="startTime" class="date" />
                            <pre v-else>{{ startTime }}</pre>
                        </div>
                    </div>

                    <div class="field-group">
                        <p>Конец:</p>
                        <div class="input-wrapper">
                            <input v-if="isModalUpdateOpen == 2" type="time" v-model="endTime" class="date" />
                            <pre v-else>{{ endTime }}</pre>
                        </div>
                    </div>

                    <div v-if="isModalUpdateOpen == 2" class="field-group">
                        <p>Повторяющееся:</p>
                        <label class="custom-checkbox">
                            <input
                                type="checkbox"
                                v-model="recurring"
                                :true-value=true
                                :false-value=false
                                :disabled="isModalUpdateOpen != 2"
                            />
                            <span class="checkmark"></span>
                        </label>
                    </div>
                    <button v-if="isModalUpdateOpen == 2" class="creation-button" @click="updateTaskWrap">Сохранить</button>
                    <p
                        v-if="isModalUpdateOpen == 2"
                        class="bottom-text"
                        @click="deleteTaskWrap"
                    >
                        Удалить
                    </p>
                    <h3 class="error-msg" v-show="response">{{ response }}</h3>
                </div>
            </div>
        </transition>
    </div>
</template>


<style>
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

.field-group {
    display: flex;
    align-items: center;
    margin-bottom: 1%;
    margin-top: 1%;
}

.field-group p {
    width: 50%;
    margin: 0;
    margin-top: 1%;
    text-align: left;
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