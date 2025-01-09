<template>
  <div id="app">
    <nav class="navbar">
      <ul class="nav-links">
        <li><a href="#home">Главная</a></li>
        <li><a href="#about">О нас</a></li>
        <li><a href="#services">Услуги</a></li>
        <li><a href="#contact">Контакты</a></li>
      </ul>
    </nav>
    <h1>Добро пожаловать в Chrono!</h1>
  </div>
</template>
  <script>
  export    default {
    name: 'StartPage',
  };
  </script>
  
  <style>
  @import "./style.css"; /* Убедитесь, что путь правильный */
  
  #app {
    text-align: center;
    padding: 20px;
  }
  
  .navbar {
    background-color: #3498db;
    padding: 10px 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .nav-links {
    list-style: none;
    display: flex;
    justify-content: center;
    margin: 0;
    padding: 0;
  }
  
  .nav-links li {
    margin: 0 15px;
  }
  
  .nav-links a {
    text-decoration: none;
    color: #333;
    font-family: Arial, sans-serif;
    font-size: 16px;
    transition: color 0.3s;
  }
  
  .nav-links a:hover {
    color: #007BFF;
  }
  
  h1 {
    color: #333;
    font-family: Arial, sans-serif;
    margin-top: 20px;
  }
  </style>