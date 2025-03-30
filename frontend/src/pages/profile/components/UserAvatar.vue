<template>
  <div class="user-avatar" @mouseenter="hover = true" @mouseleave="hover = false">
    <img :src="avatarUrl" alt="Avatar" class="avatar-image" @click="triggerFileInput" />
    <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" />
    <div v-if="hover" class="overlay" @click="triggerFileInput">
      <span class="change-text">Изменить аватарку</span>
    </div>
    <p class="user-name">{{ user.username }}</p>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";

export default {
  name: "UserAvatar",
  setup() {
    const defaultAvatar = "https://via.placeholder.com/190";
    const user = ref({ username: "Loading..." });
    const avatarUrl = ref(defaultAvatar);
    const hover = ref(false);
    const fileInput = ref(null);

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
          headers: { Authorization: `Bearer ${token}` },
        });
        user.value = response.data;
      } catch (error) {
        console.error("Error fetching user:", error);
        user.value = { username: "Unknown" };
      }
    };

    const fetchAvatar = async () => {
      try {
        const token = getToken();
        const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/file/get`, {
          headers: { Authorization: `Bearer ${token}` },
          responseType: "blob",
        });
        const blob = response.data;
        avatarUrl.value = URL.createObjectURL(blob);
      } catch (error) {
        console.error("Error fetching avatar:", error);
        avatarUrl.value = defaultAvatar;
      }
    };

    const triggerFileInput = () => {
      if (fileInput.value) {
        fileInput.value.click();
      }
    };

    const handleFileChange = async (event) => {
      const file = event.target.files[0];
      if (!file) return;
      try {
        const newFile = new File([file], "avatar.jpg", { type: file.type });
        const token = getToken();
        const formData = new FormData();
        formData.append("file", newFile);
        await axios.post(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/file/upload`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
        await fetchAvatar();
      } catch (error) {
        console.error("Error uploading avatar:", error);
      }
    };

    onMounted(async () => {
      await fetchUser();
      await fetchAvatar();
    });

    return {
      user,
      avatarUrl,
      hover,
      fileInput,
      triggerFileInput,
      handleFileChange,
    };
  },
};
</script>

<style scoped>
.user-avatar {
  position: relative;
  width: 190px;
  height: 190px;
  border-radius: 50%;
  background-color: #f9f9f9;
  margin: 70px 160px;
  overflow: hidden;
  cursor: pointer;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
}

.change-text {
  font-size: 1.2em;
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
