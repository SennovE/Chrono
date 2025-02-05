<!-- UserSettings.vue -->
<template>
    <div class="settings-password">
      <h1>Смена пароля</h1>
      <form @submit.prevent="onSubmitPassword">
        <label for="oldPassword">Старый пароль:</label>
        <input
          type="password"
          id="oldPassword"
          v-model="oldPassword"
          placeholder="Введите старый пароль"
          required
        />
  
        <label for="newPassword">Новый пароль:</label>
        <input
          type="password"
          id="newPassword"
          v-model="newPassword"
          placeholder="Введите новый пароль"
          required
        />
  
        <label for="confirmPassword">Подтвердите новый пароль:</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="confirmPassword"
          placeholder="Повторите новый пароль"
          required
        />
  
        <button type="submit">Сохранить</button>
      </form>
    </div>
  
    <div class="settings-email">
      <h2>Смена почты</h2>
      <form @submit.prevent="onSubmitEmail">
        <label for="email">Новая почта:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Введите новую почту"
          required
        />
        <button type="submit">Сохранить</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue"
  // Импортируйте ваши функции
  import { get_old_password, change_password } from "./ProfileFunctions.js"
  
  // Поля (реактивные)
  const oldPassword = ref("")
  const newPassword = ref("")
  const confirmPassword = ref("")
  const email = ref("")
  
  // Форма для смены пароля
  async function onSubmitPassword() {
    // 1. Проверить, что новый пароль совпадает с подтверждением
    if (newPassword.value !== confirmPassword.value) {
      alert("Новый пароль и подтверждение не совпадают!")
      return
    }
  
    // 2. Проверяем, что старый пароль введён верно (пример).
    //    Логика может отличаться, смотрите как устроен ваш бэкенд.
    const realOldPassword = await get_old_password()
    if (realOldPassword === -1) {
      alert("Ошибка проверки старого пароля или пользователь не авторизован.")
      return
    }
    if (oldPassword.value !== realOldPassword) {
      alert("Старый пароль введён неверно!")
      return
    }
  
    // 3. Меняем пароль
    const errorMsg = await change_password(newPassword.value)
    if (errorMsg) {
      alert(errorMsg)
    } else {
      alert("Пароль успешно изменён!")
      oldPassword.value = ""
      newPassword.value = ""
      confirmPassword.value = ""
    }
  }
  
  // Форма для смены почты (пример)
  function onSubmitEmail() {
    alert(`Email «${email.value}» отправлен на сервер (пример).`)
    email.value = ""
  }
  </script>
  
  <style scoped>

  .settings-password, .settings-email {
    width: 300px;
    position: relative;
    top: 450px; /* лучше использовать margin, но для примера оставим так */
    left: 150px;
  }
  
  form {
    display: flex;
    flex-direction: column;
  }
  
  label {
    margin-top: 8px;
  }
  
  input {
    margin-bottom: 8px;
    padding: 8px;
  }
  
  button {
    padding: 4px 8px;
    cursor: pointer;
  }
  </style>
  