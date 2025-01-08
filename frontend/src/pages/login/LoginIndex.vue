<script setup>
import mainContainer from "./components/LoginPage.vue"
import navPanel from "./components/LoginNavPanel.vue"
</script>

<template>
    <div>
        <mainContainer />
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