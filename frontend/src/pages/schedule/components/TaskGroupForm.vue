<script setup>
import { ref, defineProps, defineEmits, watch } from "vue"
import { deleteTasksGroup, addTasksGroup, updateTasksGroup, addTasksGroupByCode } from "./ScheduleFunctions"
import { useRouter } from "vue-router"

const emit = defineEmits([
    "closeGroupForm",
    "modalUpdateClose",
    "setNewGroup",
    "fetchGroups",
])
const router = useRouter()

const props = defineProps({
    isMakingTaskGroup: Number,
    taskGroups: Object,
    selectedTaskGroup: Object,
})

const responseNew = ref("")
const responseExisting = ref("")
const nameText = ref("")
const colorText = ref("#c8c8c8")
const codeText = ref("")

function clearFields() {
    responseNew.value = ""
    responseExisting.value = ""
    nameText.value = ""
    colorText.value = "#c8c8c8"
    codeText.value = ""
}

function closeModal() {
    clearFields()
    emit("closeGroupForm")
    emit("fetchGroups")
}

function modalOpen() {
    clearFields()
    if (props.isMakingTaskGroup == 2) {
        if (props.selectedTaskGroup.name === undefined) {
            emit("setNewGroup")
            return
        }
        nameText.value = props.selectedTaskGroup.name
        colorText.value = props.selectedTaskGroup.color
        codeText.value = props.selectedTaskGroup.code
    }
}

async function deleteGroupWrap() {
    await deleteTasksGroup(router, props.selectedTaskGroup.id)
    closeModal()
}

async function addGroupWrap() {
    responseNew.value = await addTasksGroup(router, nameText.value, colorText.value)
    if (responseNew.value == "") {
        closeModal()
    }
}

async function updateGroupWrap() {
    responseNew.value = await updateTasksGroup(
        router,
        props.selectedTaskGroup.id,
        nameText.value,
        colorText.value
    )
    if (responseNew.value == "") {
        closeModal()
    }
}

async function addTasksGroupByCodeWrap() {
    responseExisting.value = await addTasksGroupByCode(router, codeText.value)
    if (responseExisting.value == "") {
        closeModal()
    }
}


watch(() => props.isMakingTaskGroup, modalOpen)
</script>

<template>
    <div
        v-if="props.isMakingTaskGroup != 0" 
        class="modal-overlay"
        :style="{ 'z-index': 10000 }"
        @click="closeModal"
    >
        <div
            class="modal-content"
            @click.stop
        >
            <div class="modal-header">
                <h2 v-if="props.isMakingTaskGroup == 1">Добавить группу</h2>
                <h2 v-if="props.isMakingTaskGroup == 2">Изменить группу</h2>
                <button class="close-button" @click="closeModal">
                    &times;
                </button>
            </div>
            <div class="field-group">
                <p>Название:</p>
                <div class="input-wrapper">
                    <input placeholder="Название группы" v-model="nameText" />
                </div>
            </div>
            <div class="field-group">
                <p>Цвет:</p>
                <input type="color" v-model="colorText" class="color-picker"/>
            </div>
            <div
                v-if="props.isMakingTaskGroup == 2"
                class="field-group"
            >
                <p>Код для добавления:</p>
                {{ codeText }}
            </div>
            <button
                v-if="props.isMakingTaskGroup == 1"
                class="creation-button"
                @click="addGroupWrap"
            >
                Добавить новую
            </button>
            <button
                v-else
                class="creation-button"
                @click="updateGroupWrap"
            >
                Сохранить
            </button>
            <p
                v-if="props.isMakingTaskGroup == 2"
                class="bottom-text"
                @click="deleteGroupWrap"
            >
                Удалить
            </p>
            <h3 class="error-msg" v-show="responseNew">{{ responseNew }}</h3>
            <div v-if="props.isMakingTaskGroup == 1">
                <p :style="{ 'padding-bottom': '1vh' }"></p>
                <div class="field-group">
                    <p>Код:</p>
                    <div class="input-wrapper">
                        <input placeholder="Секретный код" v-model="codeText" />
                    </div>
                </div>
                <button
                    class="creation-button"
                    @click="addTasksGroupByCodeWrap"
                >
                    Присоединиться
                </button>
                <h3 class="error-msg" v-show="responseExisting">{{ responseExisting }}</h3>
            </div>
        </div>
    </div>
</template>


<style scoped>
@import "./ScheduleMain.css";

.color-picker {
    border: none;
    border-color: transparent;
    padding: 0;
    width: 40px;
    height: 40px;
    cursor: pointer;
}
</style>