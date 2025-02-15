<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import { getMonthName, makeTime, makeWeekDates, getScheduleTasks } from "./ScheduleFunctions"
import scheduleForm from "./ScheduleForm.vue"
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
    isDragging.value = false;
}
function openModal() {
    isModalOpen.value = true
}

function handleMouseDown(day, time, event) {
    isDragging.value = true
    const cellRect = event.currentTarget.getBoundingClientRect()
    const clickY = event.clientY - cellRect.top;
    let minutes = Math.floor((clickY / cellRect.height) * 60)
    const hours = parseInt(time.split(":")[0], 10) + Math.floor(minutes / 60)
    minutes %= 60
    selectedParams.value = {
        day: day,
        time: time,
        startHours: hours,
        startMinutes: minutes,
        endHours: hours,
        endMinutes: minutes,
        top: `${minutes / 60 * 100}%`,
        bottom: `${minutes / 60 * 100}%`,
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
    let minutes = Math.floor((clickY / cellRect.height) * 60)
    const hours = parseInt(time.split(":")[0], 10) + Math.floor(minutes / 60)
    minutes %= 60
    selectedParams.value.endHours = hours
    selectedParams.value.endMinutes = minutes
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
        <div class="head-line">
            <h3>{{ currentMonthName }} {{ currentYear }}</h3>
            <scheduleForm
                class="header-line-left"
                @task-added="fetchTasks"
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
                <div class="column time-column"><span>{{ time }}</span></div>
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
                        v-if="day === selectedParams.day && time === selectedParams.time && isDragging"
                        class="selected-field"
                        :style="{ top: selectedParams.top, bottom: selectedParams.bottom }"
                    ></div>
                    <div
                        class="task"
                        v-for="task in tasks[String(index)].filter((t) => `${t.start_hours}:00` == time)"
                        :key="task.id"
                        :style="{
                            top: `${task.start_minutes / 60 * 100}%`,
                            bottom: `-${(task.end_hours - task.start_hours - 1 + task.end_minutes / 60) * 100}%`
                        }"
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
.head-line {
    display: flex;
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
.modal-content {
    color: var(--color-dark-text);
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
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background-color: var(--color-bright-text);
    border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover {
    border: 1px solid var(--color-container);
}
.current-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
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

</style>