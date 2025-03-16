<template>
    <div class="user-avatar">
      <img :src="user.avatarUrl" alt="Avatar" class="avatar-image" />
      <p class="user-name">{{ user.username}}</p>
    </div>
  </template>
  
  <script>
import axios from "axios";
import { ref,  onMounted } from "vue";

  export default {
    
    name: 'UserAvatar',
    setup() { 
        const user = ref({ 
  username: "Loading...", 
  avatarUrl: "https://via.placeholder.com/190" 
    });
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

    return {
      user,
    };
    }
  }
  
  </script>
  <style scoped>
.user-avatar {
  width: 190px;
  height: 190px;
  border-radius: 50%;
  background-color: #f9f9f9;
  margin: 70px 160px;
}

.user-name {
  margin: 200px 0px 10px -100px;  
  font-size: 1.3em;
  color: #ffffff;
  text-align: center; 
}

@media (max-width: 600px) {
  .user-avatar {
    width: 120px;
    height: 120px;
    margin: 60px 0px;
  }
  
  .user-name {
    font-size: 1em;
    margin: 110px 0px 10px -40px;  
  }
}
  </style>