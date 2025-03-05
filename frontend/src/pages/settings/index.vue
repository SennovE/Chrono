<script setup>
import axios from "axios";
import { ref, onMounted, watch } from "vue";
import NavBar from "../../components/light_style/NavBar.vue";

document.body.style.overflowY = 'hidden';

const user = ref({ username: "Loading..." });
const settings = ref(null);

const editingText = ref(false);
const textInput = ref("");

const workingStart = ref("");
const workingEnd = ref("");

// Функция для получения токена
function getToken() {
  const token = localStorage.getItem("chronoJWTToken");
  if (!token) {
    throw new Error("Token is missing. Please log in.");
  }
  return token;
}

// Получение данных пользователя
async function fetchUser() {
  try {
    const token = getToken();
    const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/user/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    user.value = response.data;
  } catch (error) {
    console.error("Error fetching user:", error);
  }
}

// Получение настроек
async function fetchSettings() {
  try {
    const token = getToken();
    const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/settings/get_user_settings`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    settings.value = response.data;
  } catch (error) {
    console.error("Error fetching settings:", error)
  }
}

// Обновление локальных переменных при получении настроек
watch(settings, (newSettings) => {
  if(newSettings){
    textInput.value = newSettings.text_settings || "";
    workingStart.value = newSettings.start_working || "";
    workingEnd.value = newSettings.end_working || "";
  }
});

// Функция для отправки текстовых настроек с передачей введённого значения
async function setTextSettings(newText) {
  try {
    const token = getToken();
    await axios.post(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/settings/add_text_settings`, 
      { text: newText },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    await fetchSettings();
  } catch (error) {
    console.error("Error set text settings:", error)
  }
}

// Функция для отправки рабочего времени с передачей начала и конца
async function setWorkingHours(start, end) {
  try {
    const token = getToken();
    await axios.post(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/settings/set_working_hours`, 
      { start_working: start, end_working: end },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    await fetchSettings();
  } catch (error) {
    console.error("Error set working hours:", error)
  }
}

// Сохранение текстовых настроек
function saveTextSettings() {
  setTextSettings(textInput.value);
  editingText.value = false;
}

// Сохранение рабочего времени
function saveWorkingHours() {
  setWorkingHours(workingStart.value, workingEnd.value);
}

onMounted(async () => {
  await fetchUser();
  await fetchSettings();
});
</script>

<template>
  <div class="page-container">
    <NavBar :username="user.username" />

    <!-- Секция для текстовых настроек генерации -->
    <div class="text-settings">
      <h1>Текстовые настройки генерации</h1>
      <div v-if="settings">
        <div v-if="!editingText">
          <p class="text-display">{{ settings.text_settings || "Нет настроек" }}</p>
          <button class="btn" @click="editingText = true">Изменить</button>
        </div>
        <div v-else>
          <input type="text" v-model="textInput" class="text-input" placeholder="Введите текстовые настройки" />
          <button class="btn" @click="saveTextSettings">Сохранить</button>
          <button class="btn btn-cancel" @click="editingText = false">Отмена</button>
        </div>
      </div>
    </div>

    <!-- Секция для установки рабочего времени -->
    <div class="working-hours" v-if="settings">
      <h1>Рабочее время</h1>
      <div class="time-form">
        <label>
          Начало:
          <input type="time" v-model="workingStart" class="time-input" />
        </label>
        <label>
          Конец:
          <input type="time" v-model="workingEnd" class="time-input" />
        </label>
      </div>
      <button class="btn" @click="saveWorkingHours">Сохранить</button>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

.page-container {
  display: flex;
  background: #f7f9fc;
  font-family: 'Inter', sans-serif;
}

.text-settings,
.working-hours {
  background: #fff;
  margin: 20px;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  font-weight: 700;
}

.text-display {
  font-size: 18px;
  margin-bottom: 10px;
}

.text-input,
.time-input {
  width: calc(100% - 20px);
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.time-form {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.time-form label {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-size: 16px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #3498db;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.2s;
}

.btn:hover {
  background-color: #2980b9;
}

.btn-cancel {
  background-color: #e74c3c;
}

.btn-cancel:hover {
  background-color: #c0392b;
}
</style>
