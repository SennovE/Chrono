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
        <div
          class="tasks"
          
        >
          <div
            class="task-card"
            v-for="task in visibleTasksList"
            :key="task.id">
            <div class="task-content">
              <h3>{{ task.description}}</h3>
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

    // Обработчик события колесика мыши
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

    // Функция форматирования времени из ISO-строки (HH:MM)
    const formatTime = (isoString) => isoString.slice(11, 16);

    const formattedToday = computed(() => {
      const today = new Date();
      return `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
    });

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
      formattedToday,
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
  border: 1px solid var(--color-dark-grey);
  padding: 2px;
  border-radius: 4px;
  width: 50%;
  background-color: var(--color-brighter-black);
  color: var(--color-black);
}

.task-carousel h2 {
  text-align: center;
  margin-bottom: 16px;
  color: var(--color-black);
}
.loading-indicator {
  text-align: center;
  font-size: 18px;
  color: var(--color-grey);
}

.carousel-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  position: relative;
}

.nav-button {
  background-color: var(--color-deep-purple);
  border: none;
  color: #ffffff;
  padding: 8px;
  cursor: pointer;
  border-radius: 50%;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  margin: 0 5px;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
}

.nav-button:disabled {
  background-color: var(--color-dark-grey);
  cursor: not-allowed;
  opacity: 0.6;
}

.nav-button:hover:not(:disabled) {
  background-color: #311d58;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(94, 12, 255, 0.3);
}

.tasks-wrapper {
  flex-grow: 1;
  height: 100%;
  width: 100%;
  margin: 0 16px;
}

.tasks {
  display: flex;
  flex-direction: column;
  transition: transform 0.5s ease-in-out;
}

.task-card {
  position: relative;
  background: var(--color-dark-grey);
  margin: 8px 0;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  box-sizing: border-box;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.task-card:hover {
  background-color: #f5f5f5;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.task-content {
  margin-bottom: 5px;
}

.task-content h3 {
  margin: 0 0 8px 0;
  color: var(--color-black);
}

.task-content p {
  margin: 0;
  color: var(--color-grey);
}

.task-time {
  font-size: 0.9em;
  margin-top: 4px;
  color: var(--color-grey);
}

.delete-button {
  
  background: transparent;
  border: none;
  color: var(--color-red);
  font-size: 20px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s, color 0.3s;
}

.task-card:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  color: #cc0000;
}

.edit-button {
  background: transparent;
  border: none;
  color: var(--color-blue, #007bff);
  font-size: 20px;
  cursor: pointer;
}

.edit-button:hover {
  color: darkblue;
}

.error {
  color: var(--color-red);
  text-align: center;
  margin-top: 16px;
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
  background-color: #fff;
  padding: 1.875rem; /* 30px */
  border-radius: 0.625rem; /* 10px */
  width: 25rem; /* 400px */
  max-width: 90%;
  box-shadow: 0 0.3125rem 0.9375rem rgba(0, 0, 0, 0.3);
  position: relative;
}

.modal-content h2 {
  margin-top: 0;
  text-align: center;
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  margin-bottom: 0.9375rem; /* 15px */
  font-size: 0.9em;
  color: #333;
}

.modal-content input[type="text"],
.modal-content input[type="time"],
.modal-content input[type="date"] {
  width: 100%;
  padding: 0.5rem; /* 8px */
  margin-top: 0.3125rem; /* 5px */
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 0.3125rem; /* 5px */
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 0.625rem; /* 10px */
  margin-top: 1rem;
}

.modal-buttons button {
  padding: 0.5rem 1rem; /* 8px 16px */
  border: none;
  border-radius: 0.3125rem; /* 5px */
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.modal-buttons button[type="button"] {
  background-color: #e74c3c;
  color: white;
}

.modal-buttons button[type="submit"] {
  background-color: #3498db;
  color: white;
}

.modal-buttons button:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .task-carousel {
    width: 85%;
    padding: 1px;
    margin: 23px auto;
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
