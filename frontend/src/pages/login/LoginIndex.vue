<script setup>
import mainContainer from './components/LoginPage.vue'
import navPanel from './components/LoginNavPanel.vue'
import { ref } from 'vue'

const message = ref('')

</script>

<template>
    <div>
        <div v-if='message' class='flash-message'>
            {{ message }}
        </div>
        <mainContainer />
        <navPanel />
    </div>
</template>

<style>
.flash-message {
    padding: 10px;
    margin: 100px 0;
    color: #fff;
    background-color: #5c6bc0;
    border-radius: 4px;
}
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