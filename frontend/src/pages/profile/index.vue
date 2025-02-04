<script setup>
import navPanel from "./components/NavPad.vue";
import userAvatar from "./components/UserAvatar.vue";
import SettingsButton from "./components/SettingsButton.vue";
import TodayTasks from "./components/TodayTasks.vue";
import StatisticData from "./components/StatisticData.vue";
import UserSettings from "./components/UserSettings";
</script>


<template>
    <div>
        <navPanel />
    </div>
    <div>
        <userAvatar />
    </div>
    <div>
        <SettingsButton />
    </div>
    <div>
        <TodayTasks />
    </div>
    <div>
        <StatisticData />
    </div>
    <div>
        <UserSettings />
    </div>
</template>

<style>

@import "../../components/StyleWhite.css";

</style>