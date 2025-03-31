<script setup>
import { authUser } from "../schedule/components/ScheduleFunctions";
import invalidUserPanelAuth from './components/NotAuthorized.vue';
import navPanel from "./components/NavPad.vue";
import userAvatar from "./components/UserAvatar.vue";
import SettingsButton from "./components/SettingsButton.vue";
import TodayTasks from "./components/TodayTasks.vue";
import StatisticData from "./components/StatisticData.vue";
//import UserSettings from "./components/UserSettings.vue";
import { onMounted, ref } from "vue";


const user = ref("")

async function authUserWrap() {
    user.value = await authUser()
}

onMounted(async () => {
    await authUserWrap()
})
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
    <invalidUserPanelAuth v-show="user == -1"/>
  </div>
</template>

<style scoped>
.profile-page {
  background-color: #1e1e2e;
  color: #cdd6f4;         
  font-family: "Roboto", sans-serif;  
  height: 100vh;
  overflow-y: auto;
  padding: 20px;
}

@media (max-width: 768px) {
  .profile-page {
    background-size: cover;
    background-position: center;
  }
}
</style>
