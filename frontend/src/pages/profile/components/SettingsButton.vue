<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <div class="get-started-container_kera">
    <ul>
      <li @click="router.push({ name: 'Login Page' })" class="get-started">
        <b>Сменить аккаунт</b>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.get-started-container_kera {
  position: absolute;
  top: 400px;
  left: 160px;
  display: flex;
  /* Начальное позиционирование для больших экранов */
}



.get-started-container_kera ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.get-started {
  background: linear-gradient(135deg, #1e1e2e, #2e2e42);
  color: #cdd6f4;
  border: 1px solid #302d41;
  padding: 15px 40px;
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
  background: linear-gradient(135deg, #89b4fa, #5a9bd4);
  color: #1e1e2e;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.7);
}

.get-started:active {
  background: #302d41;
  transform: translateY(0);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

/* Для маленьких экранов */
@media (max-width: 600px) {
  .get-started-container_kera {
    position: relative;       /* меняем на fixed */
    margin: 10px;        /* размещаем у низа экрана */
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
