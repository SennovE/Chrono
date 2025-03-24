<template>
  <div class="not-authorized-container-profile">
    <div class="modal-profile">
      <h2>Вы не зарегистрированы.</h2>
      <div class="buttons-auth">
        <button @click="redirectToLogin">Войти</button>
        <button @click="redirectToRegister">Зарегистрироваться</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const redirectToLogin = () => {
  router.push('/login');
};

const redirectToRegister = () => {
  router.push('/registration');
};
</script>

<style scoped>
.not-authorized-container-profile {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(30, 30, 46, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-profile {
  background-color: #1e1e2e;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  max-width: 400px;
  width: 90%;
  border: 1px solid #302d41;
}

.modal-profile h2 {
  margin-bottom: 20px;
  color: #f5e0dc;
}

.buttons-auth button {
  margin: 0 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s, transform 0.2s;
}

.buttons-auth button:first-child {
  background-color: #89b4fa;
  color: #1e1e2e;
}

.buttons-auth button:last-child {
  background-color: #a6e3a1;
  color: #1e1e2e;
}

.buttons-auth button:hover {
  transform: scale(1.05);
}
</style>
