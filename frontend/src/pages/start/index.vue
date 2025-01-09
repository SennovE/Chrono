<template>
  <div id="app">
    <nav class="navbar">
      <ul class="nav-links">
        <li><router-link to="/register">Регистрация</router-link></li>
        <li><router-link to="/login">Авторизация</router-link></li>
        <li><a href="#about">О нас</a></li>
        <li><a href="#services">Услуги</a></li>
        <li><a href="#contact">Контакты</a></li>
      </ul>
    </nav>
    <h1>Добро пожаловать в Chrono!</h1>
  </div>
</template>

<script>
export default {
  name: 'StartPage',
};
</script>

<style>

  
  #app {
    text-align: center;
    padding: 20px;
  }
  @import "./components/styel.css";

  
  
</style>