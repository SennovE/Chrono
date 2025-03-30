<template>
  <div class="user-avatar" @mouseenter="hover = true" @mouseleave="hover = false">
    <img :src="avatarUrl" alt="Avatar" class="avatar-image" @click="triggerFileInput" />
    <input type="file" ref="fileInput" style="display: none" @change="handleFileChange" />
    <div v-if="hover" class="overlay" @click="triggerFileInput">
      <span class="change-text">Изменить аватарку</span>
    </div>
    <p class="user-name">{{ user.username }}</p>
  </div>

  <!-- Модальное окно для обрезки изображения -->
  <div v-if="showCropper" class="cropper-modal">
    <div class="cropper-container">
      <img ref="cropperImage" :src="selectedImageUrl" alt="Selected Image" />
      <div class="cropper-controls">
        <label>Width:
          <input v-model.number="cropWidth" type="number" min="50" />
        </label>
        <label>Height:
          <input v-model.number="cropHeight" type="number" min="50" />
        </label>
      </div>
      <button @click="cropImage">Crop and Save</button>
      <button @click="cancelCrop">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, onMounted, nextTick } from "vue";
import Cropper from "cropperjs";
import "cropperjs/dist/cropper.css";

export default {
  name: "UserAvatar",
  setup() {
    const defaultAvatar = "";
    const user = ref({ username: "Loading..." });
    const avatarUrl = ref(defaultAvatar);
    const hover = ref(false);
    const fileInput = ref(null);
    const showCropper = ref(false);
    const selectedImageUrl = ref("");
    const cropperInstance = ref(null);
    const cropperImage = ref(null);
    const cropWidth = ref(190);
    const cropHeight = ref(190);

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
      selectedImageUrl.value = URL.createObjectURL(file);
      showCropper.value = true;
      await nextTick();
      if (cropperInstance.value) {
        cropperInstance.value.destroy();
      }
      cropperInstance.value = new Cropper(cropperImage.value, {
        aspectRatio: 1,
        viewMode: 1,
      });
    };

    const cropImage = async () => {
      if (!cropperInstance.value) return;
      const canvas = cropperInstance.value.getCroppedCanvas({
        width: cropWidth.value,
        height: cropHeight.value,
      });
      canvas.toBlob(async (blob) => {
        if (!blob) return;
        try {
          const token = getToken();
          const formData = new FormData();
          const newFile = new File([blob], "avatar.jpg", { type: blob.type });
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
        } finally {

          showCropper.value = false;
          cropperInstance.value.destroy();
          cropperInstance.value = null;
          URL.revokeObjectURL(selectedImageUrl.value);
          selectedImageUrl.value = "";
        }
      }, "image/jpeg");
    };

    const cancelCrop = () => {
      if (cropperInstance.value) {
        cropperInstance.value.destroy();
        cropperInstance.value = null;
      }
      showCropper.value = false;
      URL.revokeObjectURL(selectedImageUrl.value);
      selectedImageUrl.value = "";
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
      showCropper,
      selectedImageUrl,
      cropperImage,
      cropWidth,
      cropHeight,
      cropImage,
      cancelCrop,
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

/* Обновлённый стиль для отображения ника */
.user-name {
  margin-top: 10px;
  font-size: 1.3em;
  color: #000000;
  text-align: center;
}

/* Стили для модального окна обрезки */
.cropper-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.cropper-container {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.cropper-controls {
  margin: 10px 0;
}

.cropper-controls label {
  margin: 0 10px;
}

@media (max-width: 600px) {
  .user-avatar {
    width: 120px;
    height: 120px;
    margin: 60px 0px;
  }
  
  .user-name {
    font-size: 1em;
    margin-top: 5px;
  }
}
</style>
