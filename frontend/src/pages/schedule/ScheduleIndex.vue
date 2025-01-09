<script setup>
import { useRouter } from "vue-router"
import { authUser } from "./components/ScheduleFunctions";
import { onMounted, ref } from "vue";
import navPanel from "../../components/LoginNavPanel.vue";
import schedulePage from "./components/SchedulePage.vue";

const router = useRouter()
const user = ref("")

async function authUserWrap() {
    user.value = await authUser(router)
}

onMounted(() => {
    authUserWrap()
})
</script>


<template>
    <div>
        <schedulePage :user="user"/>
        <navPanel />
    </div>
</template>

<style>
@import "../../components/Stiles.css";
</style>