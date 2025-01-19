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
        const response = await axios.get("http://localhost:8080/api/v1/user/me", {
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
  import axios from "axios";
  import { ref, computed, onMounted } from "vue";
  <style scoped>
  .user-avatar {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 240px; /* Ширина контейнера */
    border-radius: 50%;
    background-color: #f9f9f9;
    position: absolute;
    top: 150px; /* Указание позиции отдельно */
    left: 150px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); 
    height: 190px;
    object-fit: cover;
  }
  
  
  .user-name {
  position: absolute; /* Абсолютное позиционирование текста */
  bottom: -50px; /* Отступ от нижнего края контейнера */
  left: 20px; /* Отступ от левого края контейнера */
  font-size: 1.3em;
  color: #000000;
  text-align: left; /* Текст выравнивается по левому краю */
  
}
  </style>
  