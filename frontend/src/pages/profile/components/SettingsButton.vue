<script setup>
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

const handleLogout = async () => {
  try {
    const response = await axios.post(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/user/logout`);
    console.log("Ответ сервера:", response.data);
    router.push({ name: "Login Page" });
  } catch (error) {
    console.error("Ошибка при выходе:", error);
  }
};
</script>

<template>
  <div class="get-started-container_kera">
    <ul>
      <li @click="handleLogout" class="get-started">
        <b>Сменить аккаунт</b>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.get-started-container_kera {
  position: relative;
  margin-left: 140px;
  margin-top: 1px;
}

.get-started {
  background: linear-gradient(135deg, #1e1e2e, #2e2e42);
  color: #cdd6f4;
  border: 1px solid #302d41;
  padding: 15px 10px;
  font-size: 14px;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
  display: inline-block;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);
}

.get-started:hover {
  color: #ffffff;
  box-shadow: 0 6px 12px rgba(44, 42, 42, 0.7);
}

/* Для маленьких экранов */
@media (max-width: 600px) {
  .get-started-container_kera {
    position: relative;
    margin: 10px;
    left: 45%;
    top: -5px;
    transform: translateX(-50%);
    width: auto;
  }
  .get-started {
    padding: 12px 30px;
    font-size: 12px;
  }
}
</style>
