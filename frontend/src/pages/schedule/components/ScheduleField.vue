<script setup>
import { ref, computed, onMounted, onUnmounted, watch, defineEmits } from "vue"
import { getMonthName, makeTime, makeWeekDates, getScheduleTasks } from "./ScheduleFunctions"
import scheduleForm from "./ScheduleForm.vue"
import scheduleUpdateForm from "./ScheduleUpdateForm.vue"
import { useRouter } from "vue-router"

const emit = defineEmits(['openNav'])
const isMobile = ref(window.innerWidth < 768)

const daysOnField = ref(isMobile.value ? 1 : 7)
const daysShift = ref(daysOnField.value == 7 ? 0 : (new Date()).getDay() - 1)
const dayIndexes = ref([])
function makeDayIndexes() {
    dayIndexes.value = []
    const tmp = (daysShift.value % 7 + 7) % 7
    for (let i = tmp; i < tmp + daysOnField.value; i++) {
        dayIndexes.value.push(i % 7);
    }
}
const weekdays = ref(["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"])
const am_pm = ref(false)
const times = ref(makeTime(am_pm))

const currentMinute = ref("")
const currentHour = ref("")
const currentDayName = ref("")
const currentDate = ref("")
const weekdates = ref("")
const currentMonthName = ref("")
const currentYear = ref("")
const currentTimeString = computed(() => {
    if (am_pm.value) {
        const rawHour = currentHour.value % 12 || 12
        const suffix = currentHour.value < 12 ? "am" : "pm"
        return `${rawHour}:00 ${suffix}`
    } else {
        return `${currentHour.value}:00`
    }
});

function updateTime() {
    currentDate.value = new Date()
    currentDate.value.setHours(0, 0, 0, 0)
    const day = new Date()
    const now = new Date(day.getTime() + Math.floor(daysShift.value / 7) * 7 * 24 * 60 * 60 * 1000)
    weekdates.value = makeWeekDates(now, 7)
    currentMinute.value = `${now.getMinutes() / 60 * 100}%`
    currentHour.value = now.getHours()
    currentDayName.value = weekdays.value[(now.getDay() + 6) % 7]
    currentMonthName.value = getMonthName(
        daysOnField.value == 7 ?
        now.getMonth() :
        (new Date(day.getTime() + (daysShift.value - (new Date()).getDay() + 1) * 24 * 60 * 60 * 1000)).getMonth()
    )
    currentYear.value = now.getFullYear()
}

const selectedParams = ref({
    date: "",
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

const showTaskDay = ref(0)
const showTaskId = ref("")
function showTask(dayIndex, taskId) {
    showTaskDay.value = dayIndex
    showTaskId.value = taskId
}
function clearUpdatingInfo() {
    showTaskDay.value = 0
    showTaskId.value = ""
}

function handleMouseDown(day, time, event, date) {
    isDragging.value = true
    const cellRect = event.currentTarget.getBoundingClientRect()
    const clickY = event.clientY - cellRect.top;
    let minutes = Math.max(Math.round(Math.floor((clickY / cellRect.height) * 60) / 5) * 5, 0)
    const hours = parseInt(time.split(":")[0], 10) + Math.floor(minutes / 60)
    minutes %= 60
    selectedParams.value = {
        date: date,
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

makeDayIndexes()
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

watch(daysShift, updateTime)
watch(daysShift, makeDayIndexes)
watch(daysOnField, makeDayIndexes)
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
            <svg
                @click="daysShift -= daysOnField"
                class="arrow-buttons"
                viewBox="0 0 30 40"
                xmlns="http://www.w3.org/2000/svg"
            >
                <polyline 
                    points="20,10 10,20 20,30"
                    fill="none"
                    stroke="var(--color-bright-text)"
                    stroke-width="2"
                    stroke-linejoin="round" />
            </svg>
            <h3>{{ currentMonthName }} {{ currentYear }}</h3>
            <svg
                @click="daysShift += daysOnField"
                class="arrow-buttons"
                viewBox="0 0 30 40"
                xmlns="http://www.w3.org/2000/svg"
            >
                <polyline 
                    points="10,10 20,20 10,30"
                    fill="none"
                    stroke="var(--color-bright-text)"
                    stroke-width="2"
                    stroke-linejoin="round" />
            </svg>
            <scheduleForm
                class="header-line-left"
                :style="{ 'padding-right': '2%' }"
                @taskAdded="fetchTasks"
                :isModalOpen="isModalOpen"
                @closeModal="closeModal"
                @openModal="openModal"
                :selectedParams="selectedParams"
            />
            <svg
                @click="emit('openNav')"
                class="arrow-buttons"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <rect y="4" width="24" height="2" fill="currentColor" />
                <rect y="11" width="24" height="2" fill="currentColor" />
                <rect y="18" width="24" height="2" fill="currentColor" />
            </svg>
        </div>
        <div class="row calendar-header" :style="{ 'font-size': isMobile ? '16px' : 'auto' }">
            <div class="column time-column header-row">
            </div>
            <div
                class="column header-row"
                v-for="index in dayIndexes"
                :key="index"
            >
                <b
                    v-if="weekdates[index].getTime() == currentDate.getTime()"
                    :style="{ 'border-bottom': '2px solid var(--color-bright-text)' }"
                >
                    {{ weekdates[index].getDate() }} | {{ weekdays[index] }}
                </b>
                <b v-else>
                    {{ weekdates[index].getDate() }} | {{ weekdays[index] }}
                </b>
            </div>
        </div>
        <div
            class="calendar-body"
            @mouseleave="handleMouseUp"
            :style="{ 'font-size': isMobile ? '16px' : 'auto' }"
        >
            <div
                class="row"
                :style="{ height: isMobile ? '20%' : 'auto' }"
                v-for="time in times"
                :key="time"
                :ref="time === currentTimeString ? (row) => {currentRow = row} : null"
            >
                <div class="column time-column"><span v-show="time != '0:00'">{{ time }}</span></div>
                <div
                    class="column"
                    v-for="index in dayIndexes"
                    :key="(weekdays[index], index)"
                    @mousedown="handleMouseDown(weekdays[index], time, $event, weekdates[index])"
                    @mousemove="handleCellMove(time, $event)"
                    @mouseup="handleMouseUp"
                >
                    <div
                        v-show="weekdates[index].getTime() == currentDate.getTime() && time === currentTimeString"
                        class="current-line"
                        :style="{ top: currentMinute }"
                    ></div>
                    <div
                        v-if="weekdays[index] === selectedParams.day &&
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

.arrow-buttons {
    width: 4vh;
    height: auto;
    transform: scale(1);
    display: inline-block;
    transform-origin: center;
    transition: transform 0.2s ease;
    user-select: none;
}
.arrow-buttons:hover {
    transform: scale(0.875);
}

.selected-field {
    width: 96%;
    border: 2px solid var(--color-container);
    border-radius: 8px;
    position: absolute;
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
    padding-bottom: 1%;
}
.head-line h3 {
    padding-right: 1%;
    padding-left: 1%;
    font-size: min(2vh, 2vw);
    width: 10vw;
    text-align: center;
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
    max-width: 80px;
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
    height: 2.5vh;
    padding-top: 0%;
    padding-bottom: 1%;
}

.current-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 0.2vh;
    background-color: var(--color-bright-text);
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

/* @media (max-aspect-ratio: 3/2), (max-width: 700px) {
    .calendar-container {
        height: 85vh;
    }
} */

</style>