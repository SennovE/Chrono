<template>
  <div class="top-nav-start">
    <ul>
      <li @click="router.push({ name: 'Welcome' })"><b>Главная</b></li>
      <li @click="router.push({ name: 'Schedule Page' })"><b>Календарь</b></li>
      <li @click="router.push({ name: 'Deadlines Page' })"><b>Дедлайны</b></li>
      <li class="right-button" @click="router.push({ name: 'Payment Page' })"><b>Оплата</b></li>
    </ul>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();
</script>

<style scoped>
:root {
  --mocha-bg: #1e1e2e;
  --mocha-border: #302d41;
  --mocha-text: #cdd6f4;
  --mocha-hover: #89b4fa;
  --mocha-li-bg: #2e2e42;
}

.top-nav-start {
  overflow: hidden;
  width: 100%;
  background: var(--mocha-bg);
  position: fixed;
  top: 0;
  left: 0;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
  z-index: 999;
  padding: 10px 20px;
  border-bottom: 3px solid var(--mocha-border);
}

.top-nav-start ul {
  display: flex;
  list-style-type: none;
  justify-content: flex-start;
  align-items: center;
  margin: 0;
  padding: 0;
}

.top-nav-start li {
  display: block;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 25px;
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
  color: var(--mocha-text);
  font-weight: bold;
  background-color: var(--mocha-li-bg);
}

.top-nav-start li:hover {
  background-color: var(--mocha-hover);
  color: var(--mocha-bg);
  box-shadow: 0px 4px 12px rgba(137, 180, 250, 0.3);
}

.right-button {
  margin-left: auto;
  margin-right: 2%;
}

@media (max-width: 650px) {
  .top-nav-start {
    padding: 8px 2px;
  }
  .top-nav-start ul {
    gap: 2px;
  }
  .top-nav-start li {
    padding: 4px 10px;
    font-size: 14px;
    margin: 2px 0;
  }
}
</style>
