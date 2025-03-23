<script setup>
import { authUser } from "./components/ScheduleFunctions";
import { onMounted, ref } from "vue";
import navPanel from "../../components/LoginNavPanel.vue";
import schedulePage from "./components/Page.vue";
import invalidUserPanel from "../../components/NotRegistered.vue"

document.title = "Schedule"

const user = ref("")
const isNavOpen = ref(false)

async function authUserWrap() {
    user.value = await authUser()
}

onMounted(async () => {
    await authUserWrap()
})
</script>


<template>
    <div class="grey-style">
        <navPanel v-show="isNavOpen"/>
        <schedulePage
            :user="user"
            :style="{ 'padding-top': !isNavOpen ? '1%' : '0%' }"
            @openNav="() => { isNavOpen = !isNavOpen }"
        />
        <invalidUserPanel v-show="user == -1"/>
    </div>
</template>

<style>
@import "./components/ScheduleMain.css";
</style>