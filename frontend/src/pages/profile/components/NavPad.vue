<template>
  <div class="top-nav-start">
      <ul>
          <li @click="router.push({name: 'Welcome'})"><b>Главная</b></li>
          <li @click="router.push({name: 'Schedule Page'})"><b>Календарь</b></li>
          <li @click="router.push({name: 'Deadlines Page'})"><b>Дедлайны</b></li>
      </ul>
  </div>
</template>


<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<style scoped>
:root {
  --color-pastel-pink: #ffc1e3;
  --color-pastel-purple: #d1c4e9;
  --color-light-purple: #b39ddb;
  --color-pastel-yellow: #fff9c4;
  --color-soft-grey: #f5f5f5;
}


.top-nav-start {
  width: 100%;
  background: linear-gradient(to right, var(--color-pastel-pink), var(--color-pastel-purple));
  position: fixed;
  top: 0;
  left: 0;
  box-shadow: 
      0px 4px 8px rgba(0, 0, 0, 0.1),
      0px 6px 10px rgba(0, 0, 0, 0.1);
  z-index: 999;
  padding: 10px 20px;
  border-bottom: 3px solid var(--color-light-purple);
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
  transition: background-color 0.3s ease-in-out, color 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  cursor: pointer;
  color: #6a1b9a;
  font-weight: bold;
  background-color: var(--color-soft-grey);
}


.top-nav-start li:hover {
  background-color: var(--color-light-purple); 
  color: #4a148c; 
  box-shadow: 0px 4px 12px rgba(106, 27, 154, 0.3); 
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
    display: flex;
    gap: 2px;
  }
  .top-nav-start li {
    padding: 4px 10px;
    font-size: 14px;
    margin: 2px 0;
  }
}
</style>
