<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import { getMonthName, makeTime, makeWeekDates, getScheduleTasks } from "./ScheduleFunctions"
import scheduleForm from "./ScheduleForm.vue"
import scheduleUpdateForm from "./ScheduleUpdateForm.vue"
import { useRouter } from "vue-router"

const weekdays = ref(["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"])
const ampm = ref(false)
const times = ref(makeTime(ampm))

const currentMinute = ref("")
const currentHour = ref("")
const currentDayName = ref("")
const weekdates = ref("")
const currentMonthName = ref("")
const currentYear = ref("")
const currentTimeString = computed(() => {
    if (ampm.value) {
        const rawHour = currentHour.value % 12 || 12
        const suffix = currentHour.value < 12 ? "am" : "pm"
        return `${rawHour}:00 ${suffix}`
    } else {
        return `${currentHour.value}:00`
    }
});

function updateTime() {
    const now = new Date()
    weekdates.value = makeWeekDates()
    currentMinute.value = `${now.getMinutes() / 60 * 100}%`
    currentHour.value = now.getHours()
    currentDayName.value = weekdays.value[(now.getDay() + 6) % 7]
    currentMonthName.value = getMonthName(now.getMonth())
    currentYear.value = now.getFullYear()
}

const selectedParams = ref({
    day: "",
    time: "",
    startHours: 0,
    startMinutes: 0,
    endHours: 0,
    endMinutes: 0,
    top: "0%",
    bottom: "0%",
})
const isDragging = ref(false)
const isModalOpen = ref(false)
function closeModal() {
    isModalOpen.value = false
    isDragging.value = false
}
function openModal() {
    isModalOpen.value = true
}

const showTaskDay = ref("")
const showTaskId = ref("")
function showTask(dayIndex, taskId) {
    showTaskDay.value = dayIndex
    showTaskId.value = taskId
}
function clearUpdatingInfo() {
    showTaskDay.value = 0
    showTaskId.value = -1
}

function handleMouseDown(day, time, event) {
    isDragging.value = true
    const cellRect = event.currentTarget.getBoundingClientRect()
    const clickY = event.clientY - cellRect.top;
    let minutes = Math.max(Math.round(Math.floor((clickY / cellRect.height) * 60) / 5) * 5, 0)
    const hours = parseInt(time.split(":")[0], 10) + Math.floor(minutes / 60)
    minutes %= 60
    selectedParams.value = {
        day: day,
        time: `${hours}:00`,
        startHours: Math.max(hours, 0) | 0,
        startMinutes: Math.max(minutes, 0) | 0,
        endHours: Math.max(hours, 0) | 0,
        endMinutes: Math.max(minutes, 0) | 0,
        top: `${(Math.max(minutes, 0) | 0) / 60 * 100}%`,
        bottom: `${100 - (Math.max(minutes, 0) | 0) / 60 * 100}%`,
    }
}

function handleMouseUp() {
    if (!isDragging.value) return
    openModal()
}

function handleCellMove(time, event) {
    if (!isDragging.value) return;
    const cellRect = event.currentTarget.getBoundingClientRect()
    const clickY = event.clientY - cellRect.top;
    let minutes = Math.max(Math.floor((clickY / cellRect.height) * 60), 0)
    const hours = parseInt(time.split(":")[0], 10) + Math.floor(minutes / 60)
    minutes %= 60
    selectedParams.value.endHours = Math.max(hours, 0) | 0
    selectedParams.value.endMinutes = Math.max(minutes, 0) | 0
    if (selectedParams.value.endHours < selectedParams.value.startHours) {
        selectedParams.value.endHours = selectedParams.value.startHours
        selectedParams.value.endMinutes = selectedParams.value.startMinutes
    } else if (selectedParams.value.endHours == selectedParams.value.startHours) {
        selectedParams.value.endMinutes = Math.max(
            selectedParams.value.endMinutes,
            selectedParams.value.startMinutes
        )
    }
    selectedParams.value.bottom = `${(
        selectedParams.value.endHours - selectedParams.value.startHours - 1 + selectedParams.value.endMinutes / 60
    ) * -100}%`
}

updateTime()

const tasks = ref({
    "0": [],
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": []
})

async function fetchTasks() {
    tasks.value = await getScheduleTasks(useRouter)
}

const currentRow = ref(null)
let interval = null

onMounted(async () => {
    fetchTasks()
    if (currentRow.value) {
        currentRow.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
    interval = setInterval(updateTime, 10000)
})

onUnmounted(() => {
    if (interval) {
        clearInterval(interval)
    }
})
</script>

<template>
    <div class="calendar-container">
        <scheduleUpdateForm
            :tasks="tasks"
            :showTaskDay="showTaskDay"
            :showTaskId="showTaskId"
            @taskUpdated="fetchTasks"
            @clearUpdatingInfo="clearUpdatingInfo"
        />
        <div class="head-line">
            <h3>{{ currentMonthName }} {{ currentYear }}</h3>
            <svg width="30" height="40" xmlns="http://www.w3.org/2000/svg">
                <polyline 
                    points="20,10 10,20 20,30" 
                    fill="none" 
                    stroke="var(--color-bright-text)" 
                    stroke-width="3" 
                    stroke-linejoin="round" />
            </svg>
            <svg width="30" height="40" xmlns="http://www.w3.org/2000/svg">
                <polyline 
                    points="10,10 20,20 10,30" 
                    fill="none" 
                    stroke="var(--color-bright-text)" 
                    stroke-width="3" 
                    stroke-linejoin="round" />
            </svg>
            <scheduleForm
                class="header-line-left"
                @taskAdded="fetchTasks"
                :isModalOpen="isModalOpen"
                @closeModal="closeModal"
                @openModal="openModal"
                :selectedParams="selectedParams"
            />
        </div>
        <p></p>
        <div class="row calendar-header">
            <div class="column time-column header-row">
            </div>
            <div
                class="column header-row"
                v-for="(day, index) in weekdays"
                :key="day"
            >
                <b v-if="day === currentDayName" :style="{ 'border-bottom': '2px solid var(--color-bright-text)' }">
                    {{ weekdates[index] }} | {{ day }}
                </b>
                <b v-else>
                    {{ weekdates[index] }} | {{ day }}
                </b>
            </div>
        </div>
        <div class="calendar-body" @mouseleave="handleMouseUp">
            <div
                class="row"
                v-for="time in times"
                :key="time"
                :ref="time === currentTimeString ? (row) => {currentRow = row} : null"
            >
                <div class="column time-column"><span v-show="time != '0:00'">{{ time }}</span></div>
                <div
                    class="column"
                    v-for="(day, index) in weekdays"
                    :key="(day, index)"
                    @mousedown="handleMouseDown(day, time, $event)"
                    @mousemove="handleCellMove(time, $event)"
                    @mouseup="handleMouseUp"
                >
                    <div
                        v-show="day === currentDayName && time === currentTimeString"
                        class="current-line"
                        :style="{ top: currentMinute }"
                    ></div>
                    <div
                        v-if="day === selectedParams.day &&
                              (time === selectedParams.time) && isDragging"
                        class="selected-field"
                        :style="{ top: selectedParams.top, bottom: selectedParams.bottom }"
                    >
                        <div class="selected-context">
                            <div class="new-task-text">Новое событие</div>
                            <div class="new-task-text">
                                C {{ selectedParams.startHours }}:{{
                                    (selectedParams.startMinutes < 10 ? '0' : '') + `${selectedParams.startMinutes}`
                                }}    
                            </div>
                            <div class="new-task-text">
                                До {{ selectedParams.endHours }}:{{
                                    (selectedParams.endMinutes < 10 ? '0' : '') + `${selectedParams.endMinutes}`
                                }}
                            </div>
                        </div>
                    </div>
                    <div
                        class="task"
                        v-for="task in tasks[String(index)].filter((t) => `${t.start_hours}:00` == time)"
                        :key="task.id"
                        :style="{
                            top: `${task.start_minutes / 60 * 100}%`,
                            bottom: `${(task.end_hours - task.start_hours - 1 + task.end_minutes / 60) * -100}%`
                        }"
                        @mousedown.stop
                        @click="showTask(index, task.id)"
                    >
                        <div class="task-content">
                            {{ task.name }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
@import "./ScheduleMain.css";

.selected-field {
    width: 96%;
    border: 2px solid var(--color-container);
    border-radius: 8px;
    position: absolute;
    width: 96%;
    z-index: 11;
}
.selected-context {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 0;
}
.new-task-text {
    padding-left: 10%;
    margin: auto;
}
.head-line {
    display: flex;
    align-items: center;
}
.head-line h3 {
    padding-right: 1%;
}
.header-line-left {
    margin-left: auto;
}
.calendar-container {
    height: 90vh;
    display: flex;
    flex-direction: column;
    color: var(--color-bright-text);
}
.calendar-body {
    font-size: 1vw;
    flex-grow: 1;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-gutter: stable;
    user-select: none;
}
.row {
    display: flex;
    width: 100%;
}
.column {
    flex: 1;
    min-width: 20px;
    display: flex;
    align-items: center;
    padding-top: 2%;
    padding-bottom: 2%;
    justify-content: center;
    position: relative;
}
.time-column {
    flex: 0.3;
    min-width: 40px;
    justify-content: flex-end;
    align-items: flex-start;
    padding: 0 1% 0 0;
    user-select: text;
}
.calendar-header {
    font-size: 1vw;
    flex-shrink: 0;
    scrollbar-gutter: stable;
    overflow: hidden;
}
.column::before {
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    content: "";
    position: absolute;
    border-right: 1px solid var(--color-bright-text);
    border-bottom: 1px solid var(--color-bright-text);
    opacity: 0.1;
    pointer-events: none;
}
.time-column::before {
    border-bottom: none;
}
.time-column span {
    display: inline-block;
    transform: translateY(-50%);
}
.header-row {
    padding-top: 0%;
    padding-bottom: 1%;
}

.current-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    background-color: var(--color-grey-text);
    border-radius: 8px;
    pointer-events: none;
    box-shadow:
        0 0 10px var(--color-bright-text),
        0 0 10px var(--color-bright-text),
        0 0 20px var(--color-bright-text);
    z-index: 49;
}
.task {
    position: absolute;
    width: 90%;
    border-radius: 8px;
    text-align: center;
    z-index: 10;
    transition: background-color 0.5s ease, color 0.5s ease;
    box-shadow:
        inset 0 0 0 1px var(--color-background),
        inset 0 0 1vw var(--color-container);
}
.task:hover {
    background-color: var(--color-container);
    color: var(--color-dark-text);
    opacity: 0.9;
    z-index: 50;
}
.task::after {
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    content: "";
    position: absolute;
    background: var(--color-container);
    border-radius: 8px;
    opacity: 0.2;
}
.task-content {
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding: 0% 5% 0% 5%;
    box-sizing: border-box;
}

</style>