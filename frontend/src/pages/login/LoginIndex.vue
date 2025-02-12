<script setup>
import mainContainer from "./components/LoginPage.vue"
import navPanel from "../../components/LoginNavPanel.vue"
import canvasPanel from "../../components/CanvasPanel.vue"
document.title = "Chrono login"
</script>

<template>
    <div class="login-page">
        <mainContainer />
        <navPanel />
        <canvasPanel />
    </div>
</template>

<style>
@import "../../components/grey_style/LoginContainer.css";
</style>