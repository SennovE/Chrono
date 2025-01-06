<template>
  <div id="app">
    <nav>
      <router-link to="/">Главная</router-link>
      <router-link to="/about">О нас</router-link>
      <router-link to="/settings">Настройки</router-link>
    </nav>
    <router-view></router-view> <!-- Здесь отображаются страницы -->
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* Добавьте стили, если нужно */
</style>