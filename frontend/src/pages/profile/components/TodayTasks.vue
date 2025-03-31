<template>
  <div class="task-carousel">
    <h2>Задания на сегодня</h2>
    
    <div v-if="loading" class="loading-indicator">
      Загрузка заданий...
    </div>
    
    <div
      class="carousel-container"
      v-else-if="tasks.length > 0"
      ref="carouselContainer"
    >
      <button
        class="nav-button up"
        @click="prev"
        :disabled="currentIndex === 0"
        title="Предыдущие задания"
      >
        <i class="fas fa-chevron-up"></i>
      </button>
      
      <div class="tasks-wrapper">
        <div class="tasks">
          <div
            class="task-card"
            v-for="task in visibleTasksList"
            :key="task.id"
          >
            <div class="task-content">
              <h3>{{ task.description }}</h3>
              <p class="task-time">{{ formatTime(task.deadline_time) }}</p>
            </div>
            <button
              class="edit-button"
              @click.stop="openEditModal(task)"
              title="Редактировать задачу"
            >
              ✎
            </button>
            <button
              class="delete-button"
              @click.stop="markTaskAsComplete(task.id)"
              title="Отметить как выполненную"
            >
              &times;
            </button>
          </div>
        </div>
      </div>
      
      <button
        class="nav-button down"
        @click="next"
        :disabled="isLastPage"
        title="Следующие задания"
      >
        <i class="fas fa-chevron-down"></i>
      </button>
    </div>
    
    <p v-else-if="!error">Нет заданий на сегодня.</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>

  <div v-if="isModalOpen" class="modal-overlay" @click.self="closeEditModal">
    <div class="modal-content">
      <h2>Редактировать задачу</h2>
      <form @submit.prevent="submitEdit">
        <label>
          Описание:
          <input type="text" v-model="editTask.description" required />
        </label>
        <label>
          Дата дедлайна:
          <input type="date" v-model="editTask.date" required />
        </label>
        <label>
          Время дедлайна:
          <input type="time" v-model="editTask.time" required />
        </label>
        <div class="modal-buttons">
          <button type="button" @click="closeEditModal">Отмена</button>
          <button type="submit">Сохранить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted, computed, onBeforeUnmount } from 'vue';

export default {
  name: 'TaskCarousel',
  setup() {
    const user = ref({ 
      username: "Loading...", 
      avatarUrl: "https://via.placeholder.com/190" 
    });
    const tasks = ref([]);
    const allTasks = ref([]); 
    const currentIndex = ref(0);
    const visibleTasksCount = ref(3); 
    const error = ref(null);
    const loading = ref(true);
    const isModalOpen = ref(false);
    const editTask = ref({
      id: null,
      description: '',
      date: '',
      time: ''
    });
    const carouselContainer = ref(null);

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
      } catch (err) {
        console.error("Error fetching user:", err);
        error.value = "Не удалось загрузить данные пользователя.";
      }
    };

    const fetchDeadlines = async () => {
      try {
        loading.value = true;
        const token = getToken();
        const response = await axios.get(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/get_tasks/`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        allTasks.value = response.data.map(task => ({
          ...task,
          deadline_time: new Date(task.deadline_time),
        }));
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        let todaysTasks = allTasks.value.filter(task => {
          const deadline = task.deadline_time;
          return deadline >= today && deadline < tomorrow && task.status == 0;
        });
        todaysTasks.sort((a, b) => a.deadline_time - b.deadline_time);
        tasks.value = todaysTasks.map(task => ({
          ...task,
          deadline_time: task.deadline_time.toISOString(),
        }));
        currentIndex.value = 0;
      } catch (err) {
        console.error("Error fetching deadlines:", err);
        error.value = "Не удалось загрузить задания.";
      } finally {
        loading.value = false;
      }
    };

    const markTaskAsComplete = async (taskId) => {
      const confirmDelete = confirm("Вы уверены, что хотите отметить эту задачу как выполненную?");
      if (!confirmDelete) return;
      try {
        const token = getToken();
        await axios.post(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/complete_task`,
          { id: taskId },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        await fetchDeadlines();
      } catch (err) {
        console.error("Error completing task:", err);
        alert("Не удалось отметить задачу как выполненную.");
      }
    };

    const prev = () => { if (currentIndex.value > 0) currentIndex.value--; };
    const next = () => {
      if (((currentIndex.value + 1) * visibleTasksCount.value) < tasks.value.length) {
        currentIndex.value++;
      }
    };
    const handleWheel = (event) => {
      event.preventDefault();
      if (event.deltaY > 0) {
        next();
      } else if (event.deltaY < 0) {
        prev();
      }
    };

    const openEditModal = (task) => {
      editTask.value = {
        id: task.id,
        description: task.description,
        date: task.deadline_time.slice(0, 10),
        time: task.deadline_time.slice(11, 16)
      };
      isModalOpen.value = true;
    };
    const closeEditModal = () => { isModalOpen.value = false; };

    const submitEdit = async () => {
      try {
        const token = getToken();
        const { id, description, date, time } = editTask.value;
        const [year, month, day] = date.split("-");
        const [hours, minutes] = time.split(":");
        const deadlineDate = new Date(year, month - 1, day, hours, minutes);
        const deadline_time = deadlineDate.toISOString();

        await axios.put(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/update_task`,
          { id, description, deadline_time },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        await fetchDeadlines();
        closeEditModal();
      } catch (error) {
        console.error("Error updating task:", error);
      }
    };

    const formatTime = (isoString) => isoString.slice(11, 16);

    const isLastPage = computed(() => ((currentIndex.value + 1) * visibleTasksCount.value) >= tasks.value.length);

    const visibleTasksList = computed(() => 
      tasks.value.slice(currentIndex.value, currentIndex.value + visibleTasksCount.value)
    );

    const updateVisibleTasksCount = () => {
      visibleTasksCount.value = 3;
      currentIndex.value = 0;
    };

    onMounted(() => {
      fetchUser();
      fetchDeadlines();
      updateVisibleTasksCount();
      window.addEventListener('resize', updateVisibleTasksCount);
      if (carouselContainer.value) {
        carouselContainer.value.addEventListener('wheel', handleWheel, { passive: false });
      }
    });
    onBeforeUnmount(() => {
      window.removeEventListener('resize', updateVisibleTasksCount);
      if (carouselContainer.value) {
        carouselContainer.value.removeEventListener('wheel', handleWheel);
      }
    });

    return {
      user,
      tasks,
      currentIndex,
      visibleTasksCount,
      isLastPage,
      visibleTasksList,
      prev,
      next,
      markTaskAsComplete,
      error,
      loading,
      isModalOpen,
      editTask,
      openEditModal,
      closeEditModal,
      submitEdit,
      formatTime,
      carouselContainer,
    };
  },
};
</script>

<style scoped>
.task-carousel {
  background-color: #1e1e2e; /* Тёмный фон Mocha */
  border: 1px solid #302d41;
  padding: 20px;
  border-radius: 8px;
  width: 45%;
  margin-top: 0px;
  overflow: hidden;
  /* Позиция не изменяется – панель остаётся там, где была */
  color: #cdd6f4;
}

.task-carousel h2 {
  text-align: center;
  margin-bottom: 16px;
  color: #89b4fa;
  font-size: 24px;
}

.loading-indicator {
  text-align: center;
  font-size: 18px;
  color: #a6adc8;
}

.carousel-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
}

.nav-button {
  background-color: #2e2e42;
  border: none;
  color: #cdd6f4;
  padding: 8px;
  cursor: pointer;
  border-radius: 50%;
  font-size: 14px;
  width: 35px;
  height: 35px;
  margin: 0 5px;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
}

.nav-button:disabled {
  background-color: #494d64;
  cursor: not-allowed;
  opacity: 0.6;
}

.nav-button:hover:not(:disabled) {
  background-color: #311d58;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(137, 180, 250, 0.3);
}

.tasks-wrapper {
  flex-grow: 1;
  height: 100%;
  width: 100%;
  margin: 0 16px;
}

.tasks {
  flex-direction: column;
  transition: transform 0.5s ease-in-out;
}

.task-card {
  background: #24273A;
  margin: 8px 0;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  box-sizing: border-box;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.task-card:hover {
  background-color: #343a52;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.task-content {
  margin-bottom: 5px;
}

.task-content h3 {
  margin: 0 0 8px 0;
  color: #cdd6f4;
}

.task-content p {
  margin: 0;
  color: #a6adc8;
}

.task-time {
  font-size: 0.9em;
  margin-top: 4px;
  color: #a6adc8;
}

.delete-button {
  background: transparent;
  border: none;
  color: #fab387;
  font-size: 20px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s, color 0.3s;
}

.task-card:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  color: #f7c59f;
}

.edit-button {
  background: transparent;
  border: none;
  color: #89b4fa;
  font-size: 20px;
  cursor: pointer;
}

.edit-button:hover {
  color: #a6e3a1;
}

.error {
  color: #fab387;
  text-align: center;
  margin-top: 16px;
  font-size: 16px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #1e1e2e;
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  color: #cdd6f4;
  position: relative;
}

.modal-content h2 {
  margin-top: 0;
  text-align: center;
  color: #89b4fa;
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  margin-bottom: 15px;
  font-size: 0.9em;
  color: #cdd6f4;
}

.modal-content input[type="text"],
.modal-content input[type="time"],
.modal-content input[type="date"] {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  box-sizing: border-box;
  border: 1px solid #494d64;
  border-radius: 5px;
  background-color: #24273A;
  color: #cdd6f4;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 1rem;
}

.modal-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.modal-buttons button[type="button"] {
  background-color: #fab387;
  color: #1e1e2e;
}

.modal-buttons button[type="submit"] {
  background-color: #89b4fa;
  color: #1e1e2e;
}

.modal-buttons button:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .task-carousel {
    width: 85%;
    padding: 10px;
  }
  .task-card {
    padding: 8px;
  }
  .nav-button {
    padding: 4px;
    font-size: 16px;
    width: 35px;
    height: 35px;
  }
}
</style>
