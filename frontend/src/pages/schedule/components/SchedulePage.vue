<script setup>
import { defineProps, ref } from 'vue'

const props = defineProps({
    user: String,
})

const shortText = ref('')
const descriptionText = ref('')
const startDate = ref('')
const endDate = ref('')
</script>

<template>
    <div class='scheduleContainer'>
        <div class='columnAddTask'>
            <h1>
                Добавить новое задание:
            </h1>
            <input placeholder="Название события" v-model="shortText" />
            <textarea placeholder="Добавьте описание" v-model="descriptionText"></textarea>
            <p>Начало события:</p>
            <input type="datetime-local" v-model="startDate" />
            <p>Конец события:</p>
            <input type="datetime-local" v-model="endDate" />
        </div>        
        <div class='columnSchedule'>
            <h1>
                {{ props.user }}
            </h1>
        </div>
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
