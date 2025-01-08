<script setup>
import { defineProps } from "vue"
import modelWindow from "./ScheduleTaskSheet.vue"

const props = defineProps({
    user: String,
})
</script>

<template>
    <div class="scheduleContainer">
        <div class="columnSchedule">
            <h1>
                {{ props.user }}
            </h1>
        </div>
        <modelWindow />
    </div>
</template>

<style>
.scheduleContainer {
    display: flex;
    overflow: hidden;
    align-items: flex-start;
    flex-direction: row;

    width: 95%;
    margin: 5% auto;
}
.columnAddTask, .columnSchedule {
    overflow: auto;
    height: 100%;
    box-sizing: border-box;
    padding: 0 20px;
}
.columnAddTask {
    width: 30%;
}
.columnSchedule {
    width: 70%;
}
h1 {
    text-align: center;
}
textarea {
    height: 200px;
    resize: none;
    overflow: auto;
    font-size: large;
}
</style>
