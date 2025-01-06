<template>
  <div id="app">
    <h1 class="title">Debug</h1>
    <UserDebugComponent />
  </div>
</template>

<script>
import UserDebugComponent from './components/UserDebugComponent.vue'

export default {
  components: { UserDebugComponent },
  name: 'DebugPage',
};
</script>

<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #d7ccc8, #a1887f); /* Приятный градиент */
  font-family: 'Arial', sans-serif;
  color: #4e342e; /* Тёмно-коричневый цвет */
}

/* Заголовок "Debug" */
.title {
  font-size: 48px;
  font-weight: bold;
  color: #3e2723; /* Очень тёмно-коричневый */
  text-transform: uppercase;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Лёгкая тень */
}
</style>