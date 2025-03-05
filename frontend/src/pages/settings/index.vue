<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import NavBar from "../../components/light_style/NavBar.vue";

document.body.style.overflowY = 'hidden';

const user = ref({ username: "Loading..." });

const getToken = () => {
  const token = localStorage.getItem("chronoJWTToken");
  if (!token) {
    throw new Error("Token is missing. Please log in.");
  }
  return token;
};
  
const fetchUser = async () => {
  try {
    const token = getToken();
    const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/user/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    user.value = response.data;
  } catch (error) {
    console.error("Error fetching user:", error);
  }
};

onMounted(async () => {
  await fetchUser();
});

</script>

<template>
  <div class="page-container">
    <NavBar :username="user.username" />
    
  </div>

</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

</style>