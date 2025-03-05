<script setup>
import navPanel from "./components/NavPad.vue";
import userAvatar from "./components/UserAvatar.vue";
//import SettingsButton from "./components/SettingsButton.vue";
import TodayTasks from "./components/TodayTasks.vue";
//import StatisticData from "./components/StatisticData.vue";
//import UserSettings from "./components/UserSettings";
</script>


<template>
    <div class = "profile-page">
        <navPanel />
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
    </div>
</template>

<style>
body {
  overflow-y: hidden;
  
}
html, body {
  overflow-x: hidden;
}
.profile-page {
    overflow-y: hidden;
    font-family: "Roboto", sans-serif;    
    background-image: url('./../../assets/finalmain.PNG');
    height: 100vh;
    
}
@media (max-width: 768px) {
    .profile-page {
    background-size: cover;
    background-position: center;
  }
}
</style>