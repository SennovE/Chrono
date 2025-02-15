<script setup>
import { ref, defineEmits, watch } from "vue"
import { useRouter } from "vue-router"
import { addScheduleTask } from "./ScheduleFunctions"

const emit = defineEmits(['task-added', 'closeModal', 'openModal'])
const router = useRouter()

const shortText = ref("")
const descriptionText = ref("")
const startDate = ref("")
const startTime = ref("")
const endTime = ref("")
const recurring = ref(false)

const response = ref("")

const props = defineProps({
    isModalOpen: Boolean,
    selectedParams: Object,
})

async function addScheduleTaskWrap() {
    response.value = await addScheduleTask(
        router,
        shortText.value,
        descriptionText.value,
        startDate.value,
        startTime.value,
        endTime.value,
        recurring.value
    )
    if (response.value === "") {
        emit('task-added')
        modalClose()
        shortText.value = ""
        descriptionText.value = ""
        startDate.value = ""
        startTime.value = ""
        endTime.value = ""
        recurring.value = false
    }
}

function modalOpen() {
    startTime.value = (props.selectedParams.startHours < 10 ? '0' : '') +
                      `${props.selectedParams.startHours}:` +
                      (props.selectedParams.startMinutes < 10 ? '0' : '') +
                      `${props.selectedParams.startMinutes}`
    endTime.value = (props.selectedParams.endHours < 10 ? '0' : '') +
                    `${props.selectedParams.endHours}:` +
                    (props.selectedParams.endMinutes < 10 ? '0' : '') +
                    `${props.selectedParams.endMinutes}`
    console.log(startTime.value, endTime.value)
    console.log(props.selectedParams)
}

function modalClose() {
    response.value = ""
    emit('closeModal')
}

watch(() => props.isModalOpen, modalOpen)
</script>

<template>
    <div>
        <button
            @click="emit('openModal')"
            class="form-button"
        >
            Добавить событие
        </button>
        <transition name="overlay-fade">
            <div 
                v-if="isModalOpen" 
                class="modal-overlay"
                @click="modalClose"
            >   
                <div class="modal-content" @click.stop>
                    <div class="modal-header">
                        <h2>Добавить новое событие</h2>
                        <button class="close-button" @click="modalClose">
                            &times;
                        </button>
                    </div>
                    <div class="input-wrapper">
                        <input placeholder="Название события" v-model="shortText" />
                    </div>
                    <p></p>
                    <textarea placeholder="Добавьте описание" v-model="descriptionText"></textarea>

                    <div class="field-group">
                        <p>День события:</p>
                        <div class="input-wrapper">
                            <input type="date" v-model="startDate" class="date" />
                        </div>
                    </div>
                    
                    <div class="field-group">
                        <p>Начало:</p>
                        <div class="input-wrapper">
                            <input type="time" v-model="startTime" class="date" />
                        </div>
                    </div>

                    <div class="field-group">
                        <p>Конец:</p>
                        <div class="input-wrapper">
                            <input type="time" v-model="endTime" class="date" />
                        </div>
                    </div>

                    <div class="field-group">
                        <p>Повторяющееся:</p>
                        <label class="custom-checkbox">
                            <input type="checkbox" v-model="recurring" />
                            <span class="checkmark"></span>
                        </label>
                    </div>

                    <button class="creation-button" @click="addScheduleTaskWrap">Создать</button>
                    <h3 class="error-msg" v-show="response">{{ response }}</h3>
                </div>
            </div>
        </transition>
    </div>
</template>


<style>
.creation-button {
    margin-top: 5%;
    margin-bottom: 0;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1%;
}

.field-group {
    display: flex;
    align-items: center;
    margin-bottom: 1%;
    margin-top: 1%;
}

.field-group p {
    width: 50%;
    margin: 0;
    margin-top: 1%;
    text-align: left;
}

.modal-overlay textarea {
    height: 200px;
    resize: none;
    overflow: auto;
    font-size: large;
}

.overlay-fade-enter-from,
.overlay-fade-leave-to {
  opacity: 0;
}
.overlay-fade-enter-active,
.overlay-fade-leave-active {
  transition: opacity 0.3s ease;
}
</style>