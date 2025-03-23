<script setup>
import { defineEmits } from "vue"
import calendar from "./Field.vue"

const emit = defineEmits("openNav")

</script>

<template>
    <div class="schedule-container">
        <div class="schedule-field">
            <calendar @openNav="emit('openNav')"/>
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
