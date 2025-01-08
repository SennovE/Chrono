<script setup>
import { useRouter } from 'vue-router'
import { getToken } from './components/ScheduleFunctions';

const router = useRouter()

function getTokenWrap() {
    getToken(router)
}
</script>


<template>
    <div>
        <h1 @click='getTokenWrap'>123</h1>
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