<script setup>
import navPanel from "./components/NavPad.vue";
import userAvatar from "./components/UserAvatar.vue";
import SettingsButton from "./components/SettingsButton.vue";
import TodayTasks from "./components/TodayTasks.vue";
import StatisticData from "./components/StatisticData.vue";
//import UserSettings from "./components/UserSettings";
</script>

<template>
  <div class="profile-page">
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
.profile-page {
  background-color: #1e1e2e; /* Тёмный фон в стиле Mocha */
  color: #cdd6f4;          /* Светлый текст */
  font-family: "Roboto", sans-serif;  
  height: 100vh;
  overflow-y: auto;
  padding: 20px;
}

/* При необходимости можно добавить дополнительные медиа-запросы для адаптивности */
@media (max-width: 768px) {
  .profile-page {
    background-size: cover;
    background-position: center;
  }
}
</style>
