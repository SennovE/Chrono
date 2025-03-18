<script setup>
import { useRouter } from "vue-router"

const router = useRouter()
</script>

<template>
    <div class="modal-overlay">
        <div
            class="modal-content"
            :style="{ 'text-align': 'center' }">
            <h1>Для использования надо войти в аккаунт</h1>
            <button @click="router.push({ name: 'Registration' })">Зарегистрироваться</button>
            <button @click="router.push({ name: 'Login Page' })">Войти</button>
        </div>
    </div>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #ffffff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal-content h1 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #333;
}

.modal-content button {
  display: inline-block;
  width: 200px;
  height: 50px;
  margin: 0.5rem;
  border: 2px solid #87CEEB;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  background: #ffffff;
  background-origin: border-box;
  background-clip: border-box;
}

/* При наведении кнопка немного приподнимается и появляется тень */
.modal-content button:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>