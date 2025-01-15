<script setup>
import navPanel from "../../components/LoginNavPanel.vue";
import userAvatar from "./components/UserAvatar.vue";
import SettingsButton from "./components/SettingsButton.vue";
</script>


<template>
    <div>
        <navPanel />
    </div>
    <div>
        <userAvatar />
    </div>
    <div>
        <settingsButton />
    </div>
</template>

<style>

@import "../../components/Stiles.css";

</style>