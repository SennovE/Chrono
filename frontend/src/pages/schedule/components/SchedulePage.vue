<script setup>
// import { defineProps } from "vue"
import modelWindow from "./ScheduleForm.vue"
import calendar from "./ScheduleField.vue"

// const props = defineProps({
//     user: String,
// })
</script>

<template>
    <div class="schedule-container">
        <div class="schedule-field">
            <calendar />
        </div>
        <modelWindow />
    </div>
</template>

<style>
.schedule-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    margin: 5% auto;
}
.schedule-container h1 {
    text-align: center;
}
.schedule-field {
    font-size: 16px;
    padding-top: 2%;
    width: 90%;
    height: 80%;
}
</style>
