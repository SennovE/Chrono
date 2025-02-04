<template>
  <div class="page-container">
    <NavBar :username="user.username" />
    <div class="content-container">
      <!-- Header Section with Title and Add Task Easier & Add Task Buttons -->
      <div class="header">
        <h1 class="title">My tasks</h1>
        <div class="header-buttons">
          <button
            class="add-easier-button"
            @click="openAIModal"
            aria-label="Add Task Easier"
          >
            Add task easier
          </button>
          <button
            class="add-task-button"
            @click="openAddTaskModal"
            aria-label="Add Task"
          >
            + Add task
          </button>
        </div>
      </div>

      <div class="deadline-wrapper">
        <button class="scroll-button scroll-left" @click="scrollLeft" aria-label="Scroll Left">
          <!-- SVG Icon -->
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="#7f8c8d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <div ref="deadlineListRef" class="deadline-list">
          <!-- Deadline List -->
          <div v-for="(tasks, day) in allDaysWithTasks" :key="day" class="deadline-day-wrapper">
            <div class="day-header">
              <h2 class="day-title">{{ formatDate(day) }}</h2>
            </div>
            <div class="deadline-day">
              <div class="filter-buttons">
                <button v-if="dayFilters[day] === 0" class="filter-button" @click="setFilterCompleted(day)">
                  Завершенные
                </button>
                <button v-else class="filter-button" @click="setFilterCurrent(day)">
                  Актуальные
                </button>
              </div>
              <div class="tasks">
                <div v-if="tasks.length === 0" class="empty-task-card">
                  <p v-if="dayFilters[day] === 0">Все задачи завершены!</p>
                  <p v-else>Нет актуальных задач.</p>
                </div>
                <!-- Tasks List -->
                <div
                  v-else
                  v-for="task in tasks"
                  :key="task.id"
                  class="task-card"
                  @mouseenter="hoveredTask = task.id"
                  @mouseleave="hoveredTask = null"
                  @click="dayFilters[day] === 0 ? openEditModal(task) : null"
                >
                  <div class="task-status">
                    <input
                      type="radio"
                      @change="markTaskAsComplete(task.id)"
                      @click.stop
                      :checked="task.status === 1"
                    />
                  </div>
                  <div class="task-details">
                    <p class="task-name" :class="{ completed: dayFilters[day] === 1 }">
                      {{ task.description }}
                    </p>
                    <div class="task-time-container">
                      <svg class="time-icon" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"></path>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                      </svg>
                      <!-- Динамически применяем класс в зависимости от оставшегося времени -->
                      <p class="task-time" :class="getDeadlineTimeClass(task)">
                        {{ formatTime(task.deadline_time) }}
                      </p>
                    </div>
                  </div>
                  <!-- Edit and Delete/Return Buttons -->
                  <div
                    v-if="dayFilters[day] === 0 && hoveredTask === task.id"
                    class="action-buttons"
                  >
                    <button
                      class="edit-button"
                      @click.stop="openEditModal(task)"
                      aria-label="Edit Task"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 20h9"></path>
                        <path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                      </svg>
                    </button>
                  </div>
                  <div
                    v-else-if="dayFilters[day] === 1 && hoveredTask === task.id"
                    class="action-buttons"
                  >
                    <button
                      class="return-button"
                      @click.stop="returnToActive(task.id)"
                      aria-label="Вернуть дедлайн"
                      title="Вернуть дедлайн"
                    >
                      Вернуть дедлайн
                    </button>
                    <button
                      class="delete-button"
                      @click.stop="deleteTask(task.id)"
                      aria-label="Delete Task"
                      title="Удалить задачу"
                    >
                      <!-- Красная иконка корзины -->
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#e74c3c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6L17 18.5C16.89 19.33 16.22 20 15.38 20H8.63C7.79 20 7.11 19.33 7.01 18.5L5 6Z" />
                        <path d="M14 10V16" />
                        <path d="M10 10V16" />
                        <path d="M15 4V6H9V4C9 3.47 9.21 2.96 9.59 2.59C9.96 2.21 10.47 2 11 2H13C13.53 2 14.04 2.21 14.41 2.59C14.79 2.96 15 3.47 15 4Z" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <div class="new-task-form">
                <input v-model="newTask[day].description" class="new-task-input" type="text" placeholder="Add task" />
                <input v-model="newTask[day].time" class="new-task-time" type="time" />
                <button class="create-task-button" @click="createTask(day)" title="Add Task">↑</button>
              </div>
            </div>
          </div>
        </div>
        <button class="scroll-button scroll-right" @click="scrollRight" aria-label="Scroll Right">
          <!-- SVG Icon -->
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="#7f8c8d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Existing Edit Modal -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-content">
        <h2>Редактировать задачу</h2>
        <form @submit.prevent="submitEdit">
          <label>
            Описание:
            <input type="text" v-model="editTask.description" required />
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

    <!-- Existing AI Generation Modal -->
    <div v-if="isAIModalOpen" class="modal-overlay" @click.self="closeAIModal">
      <div class="modal-content">
        <h2>Add Task Easier</h2>
        <form @submit.prevent="submitAI">
          <label>
            Enter Task Description:
            <input type="text" v-model="aiInput" required placeholder="Describe your task here" />
          </label>
          <div class="modal-buttons">
            <button type="button" @click="closeAIModal">Cancel</button>
            <button type="submit">Отправить</button>
          </div>
        </form>
      </div>
    </div>

    <!-- New Add Task Modal -->
    <div v-if="isAddTaskModalOpen" class="modal-overlay" @click.self="closeAddTaskModal">
      <div class="modal-content">
        <h2>Add New Task</h2>
        <form @submit.prevent="submitAddTask">
          <label>
            Description:
            <input type="text" v-model="newTaskData.description" required placeholder="Task description" />
          </label>
          <label>
            Date:
            <input type="date" v-model="newTaskData.date" required />
          </label>
          <label>
            Time:
            <input type="time" v-model="newTaskData.time" required />
          </label>
          <div class="modal-buttons">
            <button type="button" @click="closeAddTaskModal">Cancel</button>
            <button type="submit">Add Task</button>
          </div>
        </form>
      </div>
    </div>

    <!-- New AI Deadlines Result Modal -->
    <div v-if="isAIResultModalOpen" class="modal-overlay" @click.self="closeAIResultModal">
      <div class="modal-content">
        <h2>AI Generated Deadlines</h2>
        <div class="ai-deadlines-list">
          <div v-for="task in aiDeadlines" :key="task.id" class="ai-task">
            <p><strong>Description:</strong> {{ task.description }}</p>
            <p>
              <strong>Deadline:</strong>
              {{ formatDate(task.deadline_time.split('T')[0]) }}, {{ formatTime(task.deadline_time) }}
            </p>
          </div>
        </div>
        <div class="modal-buttons">
          <button type="button" @click="closeAIResultModal">Close</button>
          <!-- Кнопка для отправки задач на /submit_ai_generation -->
          <button type="button" @click="submitAIGeneratedTasks">Отправить</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";
import NavBar from "./components/NavBar.vue";

export default {
  name: "DeadlinePage",
  components: { NavBar },
  setup() {
    const user = ref({ username: "Loading..." });
    const deadlines = ref([]);
    const deadlineListRef = ref(null);

    const newTask = ref({});
    const isModalOpen = ref(false);
    const editTask = ref({
      id: null,
      description: "",
      date: "",
      time: "",
    });
    const hoveredTask = ref(null);
    const dayFilters = ref({}); // 0 = актуальные, 1 = завершённые

    const isAIModalOpen = ref(false);
    const aiInput = ref("");

    // New Add Task Modal State
    const isAddTaskModalOpen = ref(false);
    const newTaskData = ref({
      description: "",
      date: "",
      time: "",
    });

    // New AI Deadlines Result Modal State
    const isAIResultModalOpen = ref(false);
    const aiDeadlines = ref([]);

    /**
     * Получение токена (JWT) из localStorage.
     */
    const getToken = () => {
      const token = localStorage.getItem("chronoJWTToken");
      if (!token) {
        throw new Error("Token is missing. Please log in.");
      }
      return token;
    };

    /**
     * Запрос данных пользователя.
     */
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

    /**
     * Запрос всех задач (дедлайнов).
     */
    const fetchDeadlines = async () => {
      try {
        const token = getToken();
        const response = await axios.get(
          "http://localhost:8080/api/v1/deadline_task/get_tasks/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        // Предполагается, что сервер отправляет время в формате ISO
        deadlines.value = response.data.map(task => ({
          ...task,
          deadline_time: new Date(task.deadline_time).toISOString(),
        }));
      } catch (error) {
        console.error("Error fetching deadlines:", error);
      }
    };

    /**
     * Создание новой задачи в конкретный день.
     */
    const createTask = async (day) => {
      if (!newTask.value[day]) {
        newTask.value[day] = { description: "", time: "" };
      }
      try {
        const token = getToken();
        const [year, month, date] = day.split("-");
        const [hours, minutes] = newTask.value[day].time.split(":");
        const deadlineDate = new Date(year, month - 1, date, hours, minutes);
        const deadline_time = deadlineDate.toISOString();
        const description = newTask.value[day].description;

        await axios.post(
          "http://localhost:8080/api/v1/deadline_task/create_deadline_task",
          { description, deadline_time },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        // Очистить форму
        newTask.value[day] = { description: "", time: "" };
        await fetchDeadlines();
      } catch (error) {
        console.error("Error creating task:", error);
      }
    };

    /**
     * Пометить задачу как завершённую.
     */
    const markTaskAsComplete = async (taskId) => {
      try {
        const token = getToken();
        await axios.post(
          "http://localhost:8080/api/v1/deadline_task/complete_task",
          { id: taskId },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        await fetchDeadlines();
      } catch (error) {
        console.error("Error completing task:", error);
      }
    };

    /**
     * Удаление задачи.
     */
    const deleteTask = async (taskId) => {
      try {
        const token = getToken();
        await axios.post(
          "http://localhost:8080/api/v1/deadline_task/delete_task",
          { id: taskId },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        await fetchDeadlines();
      } catch (error) {
        console.error("Error deleting task:", error);
      }
    };

    /**
     * Возврат задачи в активные.
     */
    const returnToActive = async (taskId) => {
      try {
        const token = getToken();
        await axios.post(
          "http://localhost:8080/api/v1/deadline_task/return_to_active",
          { id: taskId },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        await fetchDeadlines();
      } catch (error) {
        console.error("Error returning task to active:", error);
      }
    };

    /**
     * Отправить запрос на AI генерацию задач.
     */
    const AIGeneration = async (user_text) => {
      try {
        const token = getToken();
        const response = await axios.post(
          "http://localhost:8080/api/v1/deadline_task/ai_generation",
          { text: user_text },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        // Предполагается, что response.data - список задач (DeadlineTask)
        aiDeadlines.value = response.data;
        isAIResultModalOpen.value = true;
      } catch (error) {
        console.error("Error AI generation", error);
      }
    };

    /**
     * Метод для отправки списка сгенерированных задач на /submit_ai_generation
     */
    const submitAIGeneratedTasks = async () => {
      try {
        const token = getToken();
        
        const tasksPayload = aiDeadlines.value.map(task => ({
          description: task.description,
          deadline_time: new Date(task.deadline_time).toISOString()
        }));

        await axios.post(
          "http://localhost:8080/api/v1/deadline_task/submit_ai_generation",
          tasksPayload,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );

        await fetchDeadlines();
        closeAIResultModal();
      } catch (error) {
        console.error("Error submitting AI tasks:", error);
      }
    };

    /**
     * Группировка задач по дате.
     */
    const groupedDeadlines = computed(() => {
      return deadlines.value.reduce((groups, task) => {
        const dateKey = task.deadline_time.split("T")[0];
        if (!groups[dateKey]) {
          groups[dateKey] = [];
        }
        groups[dateKey].push(task);
        return groups;
      }, {});
    });

    /**
     * Формирование списка ближайших 30 дней (пример) с фильтрацией задач (0=актуальные,1=завершённые).
     */
    const allDaysWithTasks = computed(() => {
      const days = Array.from({ length: 30 }, (_, i) => {
        const date = new Date();
        date.setDate(date.getDate() + i);
        return date.toISOString().split("T")[0];
      });

      return days.reduce((result, day) => {
        if (!newTask.value[day]) {
          newTask.value[day] = { description: "", time: "" };
        }
        // Инициализируем фильтр, если ещё не задан
        if (dayFilters.value[day] === undefined) {
          dayFilters.value[day] = 0; // по умолчанию актуальные
        }
        // Фильтруем задачи по текущему фильтру (0 или 1)
        result[day] = groupedDeadlines.value[day]
          ? groupedDeadlines.value[day].filter(task => task.status === dayFilters.value[day])
          : [];
        return result;
      }, {});
    });

    /**
     * Форматирование даты.
     */
    const formatDate = (dateString) => {
      const today = new Date();
      const tomorrow = new Date();
      tomorrow.setDate(today.getDate() + 1);

      const date = new Date(dateString);

      if (date.toDateString() === today.toDateString()) {
        return `Today, ${date.toLocaleDateString("en-US", { month: "long", day: "numeric" })}`;
      }

      if (date.toDateString() === tomorrow.toDateString()) {
        return `Tomorrow, ${date.toLocaleDateString("en-US", { month: "long", day: "numeric" })}`;
      }

      return date.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric",
      });
    };

    /**
     * Форматирование времени.
     */
    const formatTime = (datetime) => {
      const time = new Date(datetime);
      return time.toLocaleTimeString("ru-RU", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      });
    };

    /**
     * Скролл влево.
     */
    const scrollLeft = () => {
      const deadlineList = deadlineListRef.value;
      if (deadlineList) {
        deadlineList.scrollBy({ left: -500, behavior: "smooth" });
      }
    };

    /**
     * Скролл вправо.
     */
    const scrollRight = () => {
      const deadlineList = deadlineListRef.value;
      if (deadlineList) {
        deadlineList.scrollBy({ left: 500, behavior: "smooth" });
      }
    };

    /**
     * Открыть модалку редактирования.
     */
    const openEditModal = (task) => {
      const deadlineDate = new Date(task.deadline_time);
      const year = deadlineDate.getFullYear();
      const month = String(deadlineDate.getMonth() + 1).padStart(2, "0");
      const day = String(deadlineDate.getDate()).padStart(2, "0");
      const hours = String(deadlineDate.getHours()).padStart(2, "0");
      const minutes = String(deadlineDate.getMinutes()).padStart(2, "0");

      editTask.value = {
        id: task.id,
        description: task.description,
        date: `${year}-${month}-${day}`,
        time: `${hours}:${minutes}`,
      };

      isModalOpen.value = true;
    };

    /**
     * Закрыть модалку редактирования.
     */
    const closeEditModal = () => {
      isModalOpen.value = false;
      editTask.value = { id: null, description: "", date: "", time: "" };
    };

    /**
     * Сохранить изменения задачи.
     */
    const submitEdit = async () => {
      try {
        const token = getToken();
        const { id, description, date, time } = editTask.value;
        // Формируем новый Date
        const [year, month, day] = date.split("-");
        const [hours, minutes] = time.split(":");
        const deadlineDate = new Date(year, month - 1, day, hours, minutes);
        const deadline_time = deadlineDate.toISOString();

        await axios.put(
          "http://localhost:8080/api/v1/deadline_task/update_task",
          { id, description, deadline_time },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        await fetchDeadlines();
        closeEditModal();
      } catch (error) {
        console.error("Error updating task:", error);
      }
    };

    /**
     * Открыть модалку AI генерации задач.
     */
    const openAIModal = () => {
      isAIModalOpen.value = true;
    };

    /**
     * Закрыть модалку AI генерации задач.
     */
    const closeAIModal = () => {
      isAIModalOpen.value = false;
      aiInput.value = "";
    };

    /**
     * Отправить запрос для генерации задач (AI).
     */
    const submitAI = async () => {
      if (aiInput.value.trim() === "") {
        alert("Please enter a task description.");
        return;
      }
      try {
        await AIGeneration(aiInput.value.trim());
        closeAIModal();
      } catch (error) {
        console.error("Error submitting AI task:", error);
      }
    };

    /**
     * Открыть модалку добавления новой задачи вручную.
     */
    const openAddTaskModal = () => {
      isAddTaskModalOpen.value = true;
    };

    /**
     * Закрыть модалку добавления новой задачи.
     */
    const closeAddTaskModal = () => {
      isAddTaskModalOpen.value = false;
      newTaskData.value = { description: "", date: "", time: "" };
    };

    /**
     * Отправить форму добавления новой задачи.
     */
    const submitAddTask = async () => {
      const { description, date, time } = newTaskData.value;

      if (!description.trim() || !date || !time) {
        alert("Please fill in all fields.");
        return;
      }

      try {
        const token = getToken();
        const deadlineDate = new Date(`${date}T${time}`);
        const deadline_time = deadlineDate.toISOString();

        await axios.post(
          "http://localhost:8080/api/v1/deadline_task/create_deadline_task",
          { description: description.trim(), deadline_time },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        // Сброс формы и обновление списка
        newTaskData.value = { description: "", date: "", time: "" };
        await fetchDeadlines();
        closeAddTaskModal();
      } catch (error) {
        console.error("Error adding new task:", error);
      }
    };

    /**
     * Установить фильтр (завершённые задачи).
     */
    const setFilterCompleted = (day) => {
      dayFilters.value[day] = 1;
    };

    /**
     * Установить фильтр (актуальные задачи).
     */
    const setFilterCurrent = (day) => {
      dayFilters.value[day] = 0;
    };

    /**
     * Закрыть модалку с результатами AI генерации.
     */
    const closeAIResultModal = () => {
      isAIResultModalOpen.value = false;
    };

    /**
     * Метод для динамического назначения CSS-класса для времени дедлайна.
     * Если до дедлайна <= 2 часа – класс 'deadline-bg-red'
     * от 2 до 6 часов – 'deadline-bg-yellow'
     * от 6 до 12 часов – 'deadline-bg-purple'
     */
    const getDeadlineTimeClass = (task) => {
      const deadlineTime = new Date(task.deadline_time);
      const now = new Date();
      const diffMs = deadlineTime - now; // разница в миллисекундах
      const diffHours = diffMs / (1000 * 60 * 60); // переводим в часы

      // Если дедлайн уже прошёл, фон не меняем
      if (diffHours < 0) return '';

      if (diffHours <= 2) {
        return 'deadline-bg-red';
      } else if (diffHours <= 6) {
        return 'deadline-bg-yellow';
      } else if (diffHours <= 12) {
        return 'deadline-bg-purple';
      }
      return '';
    };

    onMounted(async () => {
      await fetchUser();
      await fetchDeadlines();
    });

    return {
      user,
      allDaysWithTasks,
      formatDate,
      formatTime,
      scrollLeft,
      scrollRight,
      deadlineListRef,
      newTask,
      createTask,
      markTaskAsComplete,
      deleteTask,
      returnToActive,
      isModalOpen,
      editTask,
      openEditModal,
      closeEditModal,
      submitEdit,
      hoveredTask,
      setFilterCompleted,
      setFilterCurrent,
      dayFilters,
      isAIModalOpen,
      aiInput,
      openAIModal,
      closeAIModal,
      submitAI,
      // New Add Task Modal
      isAddTaskModalOpen,
      openAddTaskModal,
      closeAddTaskModal,
      submitAddTask,
      newTaskData,
      // AI Deadlines Result Modal
      isAIResultModalOpen,
      aiDeadlines,
      closeAIResultModal,
      submitAIGeneratedTasks,
      // Метод для установки класса для дедлайна
      getDeadlineTimeClass,
    };
  },
};
</script>

<style scoped>
.page-container {
  display: flex;
  min-height: 100vh;
  box-sizing: border-box;
}

.content-container {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
  background-color: #f8f9fa;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  margin: 0;
  font-size: 4.5rem; /* Увеличено в 3 раза от предыдущего размера */
}

/* Container for Header Buttons */
.header-buttons {
  display: flex;
  gap: 10px;
}

/* Add Task Easier Button */
.add-easier-button {
  background: linear-gradient(45deg, #3498db, #e67e22);
  color: white;
  border: none;
  width: 150px;
  height: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 8px;
  transition: background 0.3s, transform 0.3s, box-shadow 0.3s;
  margin-left: -20%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.add-easier-button:hover {
  background: linear-gradient(45deg, #2980b9, #d35400);
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.add-easier-button:active {
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* New Add Task Button */
.add-task-button {
  background-color: white;
  color: #7f8c8d;
  border: 1px solid #bdc3c7;
  width: 150px;
  height: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s, border-color 0.3s, transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.add-task-button:hover {
  background-color: #f0f0f0;
  border-color: #a0a0a0;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.add-task-button:active {
  background-color: #e0e0e0;
  border-color: #909090;
  transform: translateY(0);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.deadline-wrapper {
  display: flex;
  position: relative;
}

.scroll-button {
  position: fixed;
  width: 40px;
  height: 40px;
  background-color: white;
  border: 2px solid #bdc3c7;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
  z-index: 10;
}

.scroll-button.scroll-left {
  left: 310px;
  top: 24%;
  transform: translateY(-50%);
}

.scroll-button.scroll-right {
  right: 35px;
  top: 24%;
  transform: translateY(-50%);
}

.scroll-button:hover {
  background-color: #ecf0f1;
  transform: translateY(-50%) scale(1.05);
}

.scroll-button:active {
  transform: translateY(-50%) scale(0.95);
}

.scroll-left {
  left: 10px;
}

.scroll-right {
  right: 10px;
}

.deadline-list {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  flex-wrap: nowrap;
  width: 100%;
  margin: 0 60px;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.deadline-list::-webkit-scrollbar {
  display: none;
}

.deadline-day-wrapper {
  display: flex;
  flex-direction: column;
  margin-right: 20px;
  position: relative;
}

.deadline-day {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffffff;
  border-radius: 20px;
  padding: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.day-title {
  font-size: 1.5rem;
  color: #333;
  text-align: center;
  margin: 0 auto;
}

.filter-buttons {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
  z-index: 10;
}

.filter-button {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 15px;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background-color 0.3s, transform 0.2s;
}

.filter-button:hover {
  background-color: #2980b9;
  transform: scale(1.05);
}

.filter-button:active {
  transform: scale(0.95);
}

.tasks {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 50px;
  width: 100%;
}

.empty-task-card {
  color: #9e9e9e;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50px;
}

.task-card {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  border: 1px solid #ebebeb;
  border-radius: 5px;
  padding: 10px;
  background-color: #fafafa;
  gap: 10px;
  flex-direction: row;
  position: relative;
  transition: background-color 0.3s;
}

.task-card:hover {
  background-color: #f0f8ff;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
}

.task-status {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.task-status input {
  width: 15px;
  height: 15px;
  cursor: pointer;
}

.task-details {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-wrap: break-word;
  word-break: break-word;
}

.task-name {
  font-weight: bold;
  margin: 0;
  white-space: normal;
  overflow: hidden;
}

.task-name.completed {
  text-decoration: line-through;
  color: #7f8c8d;
}

.task-time-container {
  display: flex;
  align-items: center;
  gap: 5px;
}

.time-icon {
  width: 12px;
  height: 12px;
  color: #555;
  flex-shrink: 0;
}

.task-time {
  font-size: 0.9rem;
  margin: 0;
  line-height: 1;
}

/* Стили для фонов дедлайна */
.deadline-bg-red {
  background-color: #ffcccc;
  padding: 2px 6px;
  border-radius: 15px;
}

.deadline-bg-yellow {
  background-color: #ffffcc;
  padding: 2px 6px;
  border-radius: 15px;
}

.deadline-bg-purple {
  background-color: #e6ccff;
  padding: 2px 6px;
  border-radius: 15px;
}

.new-task-form {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.new-task-input {
  flex: 2;
  padding: 5px;
  height: 35px;
  border: 2px solid #ccc;
  border-radius: 50px;
  font-size: 0.9rem;
  color: #555;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.new-task-input:focus {
  border-color: #3498db;
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5);
}

.new-task-time {
  flex: 1;
  padding: 5px;
  height: 35px;
  border: 2px solid #ccc;
  border-radius: 50px;
  font-size: 0.9rem;
  text-align: center;
  color: #555;
  appearance: none;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.new-task-time:focus {
  border-color: #3498db;
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5);
}

.new-task-time::placeholder {
  color: #aaa;
  font-style: italic;
}

.new-task-time::-webkit-calendar-picker-indicator {
  display: none;
}

.create-task-button {
  width: 40px;
  height: 40px;
  color: gray;
  font-size: 1.2rem;
  border: none;
  background-color: transparent;
  cursor: pointer;
  transition: transform 0.2s;
}

.create-task-button:hover {
  transform: scale(1.1);
}

/* Кнопки редактирования, удаления и возврата */
.action-buttons {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.edit-button,
.delete-button,
.return-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
  font-size: 0.8rem;
  white-space: nowrap;
}

.return-button {
  background-color: #2ecc71;
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-weight: bold;
  transition: background-color 0.3s, transform 0.2s;
}

.return-button:hover {
  background-color: #27ae60;
  transform: scale(1.05);
}

.delete-button:hover {
  background-color: rgba(231, 76, 60, 0.1);
}

.edit-button:hover {
  background-color: rgba(52, 152, 219, 0.1);
}

/* Модальные окна */
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
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  position: relative;
}

.modal-content h2 {
  margin-top: 0;
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  margin-bottom: 15px;
}

.modal-content input[type="text"],
.modal-content input[type="time"],
.modal-content input[type="date"] {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.modal-buttons button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
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

/* Новые стили для AI Deadlines Result Modal */
.ai-deadlines-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.ai-task {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.ai-task:last-child {
  border-bottom: none;
}

.ai-task p {
  margin: 5px 0;
}
</style>
