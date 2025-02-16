<script setup>
import { authUser } from "./components/ScheduleFunctions";
import { onMounted, ref } from "vue";
import navPanel from "../../components/LoginNavPanel.vue";
import schedulePage from "./components/SchedulePage.vue";
import invalidUserPanel from "../../components/NotRegistered.vue"

const user = ref("")

async function authUserWrap() {
    user.value = await authUser()
}

onMounted(async () => {
    await authUserWrap()
})
</script>


<template>
    <div class="grey-style">
        <navPanel />
        <schedulePage :user="user"/>
        <invalidUserPanel v-show="user == -1"/>
    </div>
</template>

<style>
@import "./components/ScheduleMain.css";
</style>