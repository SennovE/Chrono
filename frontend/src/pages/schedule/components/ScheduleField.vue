<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import { getMonthName, makeTime, makeWeekDates, getScheduleTasks } from "./ScheduleFunctions"
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

const currentRow = ref(null)
let interval = null

onMounted(async () => {
    tasks.value = {
        "0": [],
        "1": [
            {
                id: "123",
                name: "123",
                text: "123",
                start_hours: 13,
                start_minutes: 10,
                end_hours: 13,
                end_minutes: 10,
            }
        ],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": []
    }
    tasks.value = await getScheduleTasks(useRouter())
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
        <div>{{ tasks }}</div>
        <h3>{{ currentMonthName }} {{ currentYear }}</h3>
        <div class="row calendar-header">
            <div class="column time-column header-row">
            </div>
            <div
                class="column header-row"
                v-for="(day, index) in weekdays"
                :key="day"
            >
                <b
                    :class="[isActive ? 'active-class' : '', hasError ? 'error-class' : '']"
                >
                    {{ weekdates[index] }} | {{ day }}
                </b>
            </div>
        </div>
        <div class="calendar-body">
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
                    >
                    <div
                        v-show="day === currentDayName && time === currentTimeString"
                        class="current-line"
                        :style="{ top: currentMinute }"
                    >
                    </div>
                    <div
                        class="task"
                        v-for="task in tasks[String(index)].filter((t) => t.time === time)"
                        :key="task.id"
                        :style="{
                            top: `${task.startMins / 60 * 100}%`,
                            bottom: `-${(task.endHours - task.startHours - 1 + task.endMins / 60) * 100}%`
                        }"
                    >
                        {{ task.title }}
                    </div>
                </div>
            </div>
            <p class="calendr-bottom"></p>
        </div>
    </div>
</template>

<style>
.calendar-container {
    height: 80vh;
    display: flex;
    flex-direction: column;
}
.calendar-body {
    flex-grow: 1;
    overflow-y: auto;
    overflow-x: hidden;
    scrollbar-gutter: stable;
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
}
.calendar-header {
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
    border-right: 1px solid var(--color-grey);
    border-bottom: 1px solid var(--color-grey);
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
.calendr-bottom {
    padding-bottom: 1%;
}
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background-color: var(--color-grey);
    border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover {
    border: 1px solid var(--color-deep-purple);
}
.current-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 2px;
    background-color: var(--color-deep-purple);
    border-radius: 8px;
    pointer-events: none;
    box-shadow:
        0 0 10px var(--color-deep-purple),
        0 0 10px var(--color-deep-purple),
        0 0 20px var(--color-deep-purple);
}
.task {
    position: absolute;
    width: 90%;
    border: 1px solid #ccc;
    border-radius: 8px;
    text-align: center;
    z-index: 10;
    pointer-events: none;
}
.task::after {
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    content: "";
    position: absolute;
    background: var(--color-deep-purple);
    opacity: 0.05;
    pointer-events: none;
}
</style>