<script setup>
import { defineProps } from "vue"
import modelWindow from "./ScheduleTaskSheet.vue"

const props = defineProps({
    user: String,
})
</script>

<template>
    <div class="schedule-container">
        <div class="column-schedule">
            <h1>
                {{ props.user }}
            </h1>
        </div>
        <modelWindow />
    </div>
</template>

<style>
.schedule-container {
    display: flex;
    overflow: hidden;
    align-items: flex-start;
    flex-direction: row;

    width: 95%;
    margin: 5% auto;
}
/* .column-add-task, .column-schedule {
    overflow: auto;
    height: 100%;
    box-sizing: border-box;
    padding: 0 20px;
}
.column-add-task {
    width: 30%;
}
.column-schedule {
    width: 70%;
} */
.schedule-container h1 {
    text-align: center;
}
</style>
