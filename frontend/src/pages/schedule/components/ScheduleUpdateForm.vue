<script setup>
import { ref, defineProps, defineEmits, watch } from "vue"
import { useRouter } from "vue-router"
import { deleteTask, updateTask, addScheduleTask } from "./ScheduleFunctions"

const emit = defineEmits(["closeModal"])
const router = useRouter()

const shortText = ref("")
const descriptionText = ref("")
const startDate = ref("")
const startDateString = ref("")
const startTime = ref("")
const endTime = ref("")
const recurring = ref(false)
const selectedOptionWeekDay = ref("Понедельник")
const selectedTaskGroup = ref("-")
const taskColor = ref("")

const response = ref("")

const isModalUpdateOpen = ref(0)

const props = defineProps({
    tasks: Object,
    showTaskDay: Number,
    showTaskId: String,
    weekdays: Object,
    isModalOpen: String,
    selectedParams: Object,
    taskGroups: Object,
})

async function deleteTaskWrap() {
    await deleteTask(router, props.showTaskId)
    modalClose()
}

async function addScheduleTaskWrap() {
    response.value = await addScheduleTask(
        router,
        shortText.value,
        descriptionText.value,
        startDate.value,
        startTime.value,
        endTime.value,
        recurring.value,
        taskColor.value,
    )
    if (response.value == "") {
        modalClose()
    }
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
        recurring.value,
        taskColor.value,
    )
    if (response.value == "") {
        modalClose()
    }
}

function modalClose() {
    shortText.value = ""
    descriptionText.value = ""
    startDate.value = ""
    startTime.value = ""
    endTime.value = ""
    recurring.value = false
    response.value = ""
    taskColor.value = ""
    isModalUpdateOpen.value = 0
    emit("closeModal")
}

function modalOpen() {
    if (props.isModalOpen === "update") {
        showTaskById()
    } else if (props.isModalOpen === "new") {
        modalNewTaskOpen()
    }
}

function modalNewTaskOpen() {
    isModalUpdateOpen.value = 3
    if (props.selectedParams.date == "") return
    startTime.value = String(props.selectedParams.startHours).padStart(2, '0') + ':' +
                      String(props.selectedParams.startMinutes).padStart(2, '0')
    endTime.value = String(props.selectedParams.endHours).padStart(2, '0') + ':' +
                    String(props.selectedParams.endMinutes).padStart(2, '0')
    const year = props.selectedParams.date.getFullYear()
    const month = String(props.selectedParams.date.getMonth() + 1).padStart(2, '0')
    const day = String(props.selectedParams.date.getDate()).padStart(2, '0')
    startDate.value = `${year}-${month}-${day}`
    const tmp = new Date(startDate.value)
    selectedOptionWeekDay.value = props.weekdays[(tmp.getDay() + 6) % 7]
}

function showTaskById() {
    if (props.showTaskId == "") return
    const selectedTask = props.tasks[props.showTaskDay].find(task => task.id == props.showTaskId)
    shortText.value = selectedTask.name
    descriptionText.value = selectedTask.text
    startDate.value = String(selectedTask.year) + '-' +
                      String(selectedTask.month).padStart(2, '0') + '-' +
                      String(selectedTask.day).padStart(2, '0')
    startDateString.value = String(selectedTask.day).padStart(2, '0') + '.' +
                            String(selectedTask.month).padStart(2, '0') + '.' +
                            String(selectedTask.year)
    startTime.value = String(selectedTask.start_hours).padStart(2, '0') + ':' +
                      String(selectedTask.start_minutes).padStart(2, '0')
    endTime.value = String(selectedTask.end_hours).padStart(2, '0') + ':' +
                    String(selectedTask.end_minutes).padStart(2, '0')
    recurring.value = selectedTask.recurring
    taskColor.value = selectedTask.taskColor
    isModalUpdateOpen.value = 1
    const tmp = new Date(startDate.value)
    selectedOptionWeekDay.value = props.weekdays[(tmp.getDay() + 6) % 7]
}

function changeRecurring() {
    if (!recurring.value) {
        const currDay = props.weekdays.indexOf(selectedOptionWeekDay.value)
        const tmp = new Date()
        tmp.setDate(tmp.getDate() - (tmp.getDay() + 6) % 7 + currDay)
        const year = tmp.getFullYear()
        const month = String(tmp.getMonth() + 1).padStart(2, '0')
        const day = String(tmp.getDate()).padStart(2, '0')
        startDate.value = `${year}-${month}-${day}`
    } else {
        const tmp = new Date(startDate.value)
        selectedOptionWeekDay.value = props.weekdays[(tmp.getDay() + 6) % 7]
    }
}

watch(() => props.isModalOpen, modalOpen)
watch(() => recurring.value, changeRecurring)
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
                        <h2 v-else-if="isModalUpdateOpen == 3">Добавить событие</h2>
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
                    <div v-if="isModalUpdateOpen == 2 || isModalUpdateOpen == 3" class="input-wrapper">
                        <input placeholder="Название события" v-model="shortText" />
                    </div>
                    <p></p>
                    <textarea
                        v-if="isModalUpdateOpen == 2 || isModalUpdateOpen == 3"
                        placeholder="Добавьте описание"
                        v-model="descriptionText"
                    ></textarea>
                    <pre v-else class="task-text">{{ !descriptionText ? "Без описания" : descriptionText }}</pre>

                    <div class="field-group">
                        <p>День события:</p>
                        <div class="input-wrapper">
                            <input
                                v-if="(isModalUpdateOpen == 2 || isModalUpdateOpen == 3) && !recurring"
                                type="date"
                                v-model="startDate"
                                class="date"
                            />
                            <div
                                v-else-if="isModalUpdateOpen == 2  || isModalUpdateOpen == 3"
                                class="custom-select"
                            >
                                <select v-model="selectedTaskGroup">
                                    <option v-for="option in props.weekdays" :key="option">
                                        {{ option }}
                                    </option>
                                </select>
                            </div>
                            <pre v-else>{{ startDateString }}</pre>
                        </div>
                    </div>
                    
                    <div class="field-group">
                        <p>Начало:</p>
                        <div class="input-wrapper">
                            <input
                                v-if="isModalUpdateOpen == 2 || isModalUpdateOpen == 3"
                                type="time"
                                v-model="startTime"
                                class="date"
                            />
                            <pre v-else>{{ startTime }}</pre>
                        </div>
                    </div>

                    <div class="field-group">
                        <p>Конец:</p>
                        <div class="input-wrapper">
                            <input
                                v-if="isModalUpdateOpen == 2 || isModalUpdateOpen == 3"
                                type="time"
                                v-model="endTime"
                                class="date"
                            />
                            <pre v-else>{{ endTime }}</pre>
                        </div>
                    </div>
                    <div class="field-group">
                        <p>Группа:</p>
                        <div class="input-wrapper">
                            <div
                                class="custom-select"
                            >
                                <select v-model="selectedOptionWeekDay">
                                    <option v-for="option in props.weekdays" :key="option">
                                        {{ option }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div v-if="isModalUpdateOpen == 2 || isModalUpdateOpen == 3" class="field-group">
                        <p>Повторяющееся:</p>
                        <label class="custom-checkbox">
                            <input
                                type="checkbox"
                                v-model="recurring"
                                :true-value=true
                                :false-value=false
                                :disabled="isModalUpdateOpen == 1"
                            />
                            <span class="checkmark"></span>
                        </label>
                    </div>
                    <button
                        v-if="isModalUpdateOpen == 2"
                        class="creation-button"
                        @click="updateTaskWrap"
                    >
                        Сохранить
                    </button>
                    <button
                        v-if="isModalUpdateOpen == 3"
                        class="creation-button"
                        @click="addScheduleTaskWrap"
                    >
                        Добавить
                    </button>
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
.modal-header h2 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 70%;
}

.field-group {
    display: flex;
    align-items: center;
    margin-bottom: 1%;
    margin-top: 1%;
}

.field-group p {
    width: 50%;
    min-width: 150px;
    margin: 0;
    margin-top: 1%;
    padding-right: 2%;
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