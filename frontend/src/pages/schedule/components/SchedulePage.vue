<script setup>
import calendar from "./ScheduleField.vue"

</script>

<template>
    <div class="schedule-container">
        <div class="schedule-field">
            <calendar />
        </div>
    </div>
</template>

<style>
.schedule-container {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    margin: 4% auto;
}
.schedule-container h1 {
    text-align: center;
}
.schedule-field {
    font-size: 16px;
    width: 90%;
    height: 90%;
}
</style>
