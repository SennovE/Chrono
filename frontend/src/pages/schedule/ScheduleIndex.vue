<script setup>
import { useRouter } from "vue-router"
import { authUser } from "./components/ScheduleFunctions";
import { onMounted, ref } from "vue";
import navPanel from "../login/components/LoginNavPanel.vue";
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
body {
    overflow: hidden;
    background: linear-gradient(to right, var(--color-briter-black), var(--color-black));
    font-family: "Roboto", sans-serif;
    color: var(--color-grey);
}
::selection {
    color: var(--color-deep-purple);
    background: rgba(128, 128, 128, 0.087);
    border-radius: 5px;
}
</style>