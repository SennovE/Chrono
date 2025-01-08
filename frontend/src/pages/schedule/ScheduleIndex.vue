<script setup>
import { useRouter } from 'vue-router'
import { authUser } from './components/ScheduleFunctions';
import { onMounted, ref } from 'vue';
import navPanel from '../login/components/LoginNavPanel.vue';
import schedulePage from './components/SchedulePage.vue';

const router = useRouter()
const user = ref('')

async function authUserWrap() {
    user.value = await authUser(router)
}

onMounted(() => {
    authUserWrap()
})
</script>


<template>
    <div>
        <schedulePage :user='user'/>
        <navPanel />
    </div>
</template>

<style>
body {
    overflow: hidden;
    background: linear-gradient(to right, #d7ccc8, #a1887f);
    font-family: 'Roboto', sans-serif;
}
::selection {
    color: #2e2e2ea0;
    background: #cebeb8;
    border-radius: 5px;
}
</style>