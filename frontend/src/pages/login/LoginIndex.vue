<script setup>
import ChildComp from './components/LoginPage.vue'
</script>

<template>
    <div class="back">
        <ChildComp/>
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