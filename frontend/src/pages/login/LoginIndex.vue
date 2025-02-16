<script setup>
import mainContainer from "./components/LoginPage.vue"
import navPanel from "../../components/LoginNavPanel.vue"
import canvasPanel from "../../components/CanvasPanel.vue"
document.title = "Chrono login"
</script>

<template>
    <div class="grey-style">
        <mainContainer />
        <navPanel :style="{ 'position': 'fixed', 'z-index': '999' }"/>
        <canvasPanel />
    </div>
</template>

<style>
@import "./components/LoginContainer.css";
</style>