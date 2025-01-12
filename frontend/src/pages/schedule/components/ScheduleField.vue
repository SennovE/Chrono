<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import { getMonthName, makeTime, makeWeekDates } from "./ScheduleFunctions"

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

const currentRow = ref(null)
let interval = null

onMounted(() => {
    if (currentRow.value) {
        currentRow.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
    interval = setInterval(updateTime, 6000)
})

onUnmounted(() => {
    if (interval) {
        clearInterval(interval)
    }
})
</script>

<template>
    <div class="calendar-container">
        <h3>{{ currentMonthName }} {{ currentYear }}</h3>
        <div class="row calendar-header">
            <div class="column time-column header-row">
            </div>
            <div
                class="column header-row"
                v-for="(day, date) in weekdays"
                :key="day"
            >
                <b
                    :class="[isActive ? 'active-class' : '', hasError ? 'error-class' : '']"
                >
                    {{ weekdates[date] }} {{ day }}
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
                        v-for="day in weekdays"
                        :key="day"
                    >
                    <div
                        v-show="day === currentDayName && time === currentTimeString"
                        class="current-line"
                        :style="{ top: currentMinute }"
                    >
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
    scrollbar-gutter: stable;
}
.row {
    display: flex;
    width: 100%;
}
.column {
    flex: 1;
    display: flex;
    align-items: center;
    padding-top: 2%;
    padding-bottom: 2%;
    justify-content: center;
    position: relative;
}
.time-column {
    flex: 0.3;
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
</style>