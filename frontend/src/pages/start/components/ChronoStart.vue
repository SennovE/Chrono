<template>
    <div class="container2">
      <h1 class="title">Chrono</h1>
      <p class="subtitle">Планируй. Действуй. Побеждай!</p>
    </div>
  </template>
  
  <script>
  </script>
  
  <style scoped>
  .container2 {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #e5e9ec;
  }
  
  .title {
    font-size: 6rem;
    font-weight: bold;
    color: #111;
  }
  
  .subtitle {
    font-size: 1.5rem;
    color: #111;
    margin-top: 0.5rem;
  }
  @media (max-width: 768px) {
  .container2 {
    padding: 90px;
    height: 23%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .title {
    font-size: 3rem;
    text-align: center;
    margin-top: -1300px;
  }
  
  .subtitle {
    font-size: 1rem;
    text-align: center;
    margin: 0.5rem 0;
  }
}
  </style>
  