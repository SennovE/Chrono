<template>
  <div class="page-wrapper">
  <div class="background-layer"></div>
  <div class="page-container">
    <NavBar :username="user.username" />
    <div class="content-container">
      <invalidUserPanel v-show="user == -1"/>
      <!-- Header Section with Title and Add Task Easier & Add Task Buttons -->
      <div class="header">
        <div class="title-container">
          <h1 class="title">My tasks</h1>
          <div class="toggle-switch deadline-view-switch">
            <div class="toggle-slider" :class="{ all: deadlineViewMode === 'all' }"></div>
            <div class="toggle-option" @click="deadlineViewMode = 'byDays'">By days</div>
            <div class="toggle-option" @click="deadlineViewMode = 'all'">All</div>
          </div>
        </div>
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

      <div v-if="deadlineViewMode === 'byDays'" class="deadline-wrapper">
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
                  Active tasks
                </button>
                <button v-else class="filter-button" @click="setFilterCurrent(day)">
                  Completed tasks
                </button>
              </div>
              <div class="tasks">
                <div v-if="tasks.length === 0" class="empty-task-card">
                  <p v-if="dayFilters[day] === 0">All tasks are completed!</p>
                  <p v-else>No completed tasks</p>
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
                      <!-- Применяем класс в зависимости от оставшегося времени -->
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
                <button class="arrow-button" @click="createTask(day)">
                  <svg
                    width="40"
                    height="40"
                    viewBox="0 0 100 100"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <circle cx="50" cy="50" r="38" stroke="#87CEEB" stroke-width="6" fill="none" />
                    <path d="M34 58 L50 38 L66 58" stroke="#87CEEB" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
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

    <!-- Режим "All": теперь три карточки будут располагаться в ряд -->
    <div v-else class="all-deadlines-wrapper">
      <!-- Upcoming Deadlines -->
      <div class="all-deadline-card">
        <div class="card-header">
          <h2>Upcoming</h2>
        </div>
        <div class="card-content">
          <div v-if="upcomingDeadlines.length === 0" class="empty-task-card">
            <p>No upcoming deadlines</p>
          </div>
          <div
            v-for="task in upcomingDeadlines"
            :key="task.id"
            class="task-card"
            @click="openEditModal(task)"
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
              <p class="task-name" :class="{ completed: task.status === 1 }">
                {{ task.description }}
              </p>
              <div class="task-time-container">
                <svg
                  class="time-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"></path>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
                <p class="task-time" :class="getDeadlineTimeClass(task)">
                  {{ formatTime(task.deadline_time) }}
                </p>
                <span class="deadline-date">
                  {{ formatDate(task.deadline_time.split('T')[0]) }}
                </span>
              </div>
            </div>
            <div class="action-buttons">
              <button
                class="edit-button"
                @click.stop="openEditModal(task)"
                aria-label="Edit Task"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#3498db"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M12 20h9"></path>
                  <path
                    d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Indefinite Deadlines -->
      <div class="all-deadline-card">
        <div class="card-header">
          <h2>Indefinite</h2>
        </div>
        <div class="card-content">
          <div v-if="indefiniteDeadlines.length === 0" class="empty-task-card">
            <p>No indefinite deadlines</p>
          </div>
          <div
            v-for="task in indefiniteDeadlines"
            :key="task.id"
            class="task-card"
            @click="openEditModal(task)"
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
              <p class="task-name" :class="{ completed: task.status === 1 }">
                {{ task.description }}
              </p>
            </div>
            <div class="action-buttons">
              <button
                class="edit-button"
                @click.stop="openEditModal(task)"
                aria-label="Edit Task"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#3498db"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M12 20h9"></path>
                  <path
                    d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Overdue Deadlines -->
      <div class="all-deadline-card">
        <div class="card-header">
          <h2>Overdue</h2>
        </div>
        <div class="card-content">
          <div v-if="overdueDeadlines.length === 0" class="empty-task-card">
            <p>No overdue deadlines</p>
          </div>
          <div
            v-for="task in overdueDeadlines"
            :key="task.id"
            class="task-card"
            @click="openEditModal(task)"
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
              <p class="task-name" :class="{ completed: task.status === 1 }">
                {{ task.description }}
              </p>
              <div class="task-time-container">
                <svg
                  class="time-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"></path>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
                <p class="task-time" :class="getDeadlineTimeClass(task)">
                  {{ formatTime(task.deadline_time) }}
                </p>
                <span class="deadline-date">
                  {{ formatDate(task.deadline_time.split('T')[0]) }}
                </span>
              </div>
            </div>
            <div class="action-buttons">
              <button
                class="edit-button"
                @click.stop="openEditModal(task)"
                aria-label="Edit Task"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#3498db"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M12 20h9"></path>
                  <path
                    d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

    
    <!-- Редактирование существующей задачи -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-content fixed-form-size">
        <h2>Edit Task</h2>
        <div class="form-container">
          <form class="manual-add-task-form" @submit.prevent="submitEdit">
            <h3>Description</h3>
            <input style="border-radius: 0.5rem; margin-bottom: 0.5rem;" type="text" v-model="editTask.description" required class="description-input"/>
            <h3>Date</h3>
            <input style="border-radius: 0.5rem; margin-bottom: 0.5rem;" type="date" v-model="editTask.date" required />
            <h3>Time</h3>
            <input style="border-radius: 0.5rem; margin-bottom: 0.5rem;" type="time" v-model="editTask.time" required />
            <div class="modal-buttons">
              <button type="button" @click="closeEditModal">Cancel</button>
              <button type="submit">Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Existing AI Generation Modal with Loading Spinner -->
    <div v-if="isAIModalOpen" class="modal-overlay" @click.self="closeAIModal">
      <div class="modal-content">
        <template v-if="!aiLoading">
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
        </template>
        <template v-else>
          <div class="loading-spinner">
            <svg class="spinner" viewBox="0 0 50 50">
              <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
          </div>
        </template>
      </div>
    </div>

    <!-- New Add Task Modal -->
    <div v-if="isAddTaskModalOpen" class="modal-overlay" @click.self="closeAddTaskModal">
      <div class="modal-content fixed-form-size">
        <!-- Переключатель режимов ввода -->
        <div class="toggle-switch">
          <div class="toggle-slider" :class="{ manual: taskInputMode === 'manual' }"></div>
          <div class="toggle-option" @click="taskInputMode = 'text'">By text</div>
          <div class="toggle-option" @click="taskInputMode = 'manual'">Manually</div>
        </div>

        <!-- Обёртка для форм с фиксированными размерами -->
        <div class="form-container">
          <!-- Форма для ввода задач текстом -->
          <template v-if="taskInputMode === 'text'">
            <h3>Description</h3>
            <form @submit.prevent="submitAI">
              <textarea
                v-model="aiInput"
                class="text-box description-input"
              ></textarea>
              <div class="modal-buttons">
                <button type="button" @click="closeAddTaskModal">Cancel</button>
                <button type="submit">Submit</button>
              </div>
            </form>
          </template>
          <!-- Форма для ручного ввода задач -->
          <template v-else>
            <form class="manual-add-task-form" @submit.prevent="submitAddTask">
              <h3>Description</h3>
              <input style="border-radius: 0.5rem; margin-bottom: 0.5rem;" type="text" 
                    v-model="newTaskData.description" required
                    class="description-input"/>
              
              <div class="priority-block">
                <h3>Priority</h3>
                <div class="priority-slider-container">
                  <input
                    type="range"
                    min="0"
                    max="3"
                    step="1"
                    v-model.number="newTaskData.priority"
                    class="priority-slider"
                  />
                  <!-- Черточки расположены поверх ползунка -->
                  <div class="slider-ticks">
                    <div class="tick" style="left: 0%;"></div>
                    <div class="tick" style="left: 33.33%;"></div>
                    <div class="tick" style="left: 66.66%;"></div>
                    <div class="tick" style="left: 100%;"></div>
                  </div>
                  <!-- Надписи под черточками -->
                  <div class="priority-labels">
                    <span class="tick-label">обычный</span>
                    <span class="tick-label">очень важный</span>
                  </div>
                </div>
              </div>
              
              <!-- Переключатель Бессрочный дедлайн -->
              <div class="infinite-deadline-toggle" @click="isInfiniteDeadline = !isInfiniteDeadline">
                <div class="custom-toggle" :class="{ active: isInfiniteDeadline }">
                  <div class="toggle-circle"></div>
                </div>
                <span class="toggle-label">Indefinite deadline</span>
              </div>

              <!-- Если переключатель выключен, отображаются поля даты и времени -->
              <template v-if="!isInfiniteDeadline">
                <h3>Date</h3>
                <input style="border-radius: 0.5rem; margin-bottom: 0.5rem;" type="date" v-model="newTaskData.date" required />
                <h3>Time</h3>
                <input style="border-radius: 0.5rem; margin-bottom: 0.5rem;" type="time" v-model="newTaskData.time" required />
              </template>

              <div class="modal-buttons">
                <button type="button" @click="closeAddTaskModal">Cancel</button>
                <button type="submit">Submit</button>
              </div>
            </form>
          </template>

        </div>
      </div>
    </div>



    <!-- New AI Deadlines Result Modal -->
    <div v-if="isAIResultModalOpen" class="modal-overlay" @click.self="closeAIResultModal">
      <div class="modal-content">
        <h2>AI Generated Deadlines</h2>
        <div class="ai-deadlines-list">
          <div v-for="task in aiDeadlines" :key="task.id" class="ai-task">
            <div class="ai-task-header">
              <p><strong>Description:</strong> {{ task.description }}</p>
              <!-- Кнопка редактирования AI задания -->
              <button class="edit-button" @click.stop="openAIEditModal(task)" aria-label="Edit AI Task">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3498db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 1 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
              </button>
            </div>
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

    <!-- AI Task Edit Modal -->
    <div v-if="isAIEditModalOpen" class="modal-overlay" @click.self="closeAIEditModal">
      <div class="modal-content">
        <h2>Edit AI Deadline Task</h2>
        <form @submit.prevent="submitAIEdit">
          <label>
            Description:
            <input type="text" v-model="editAITask.description" required />
          </label>
          <label>
            Deadline Date:
            <input type="date" v-model="editAITaskDate" required />
          </label>
          <label>
            Deadline Time:
            <input type="time" v-model="editAITaskTime" required />
          </label>
          <div class="modal-buttons">
            <button type="button" @click="closeAIEditModal">Cancel</button>
            <button type="submit">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref, computed, onMounted } from "vue";
import NavBar from "../../components/light_style/NavBar.vue";
import invalidUserPanel from "../../components/NotRegisteredLight.vue"

export default {
  name: "DeadlinePage",
  components: { NavBar, invalidUserPanel },
  setup() {
    const user = ref({ username: "Loading..." });
    const deadlines = ref([]);

    const usual_deadlines = computed(() => {
      return deadlines.value.filter(task => task.deadline_time);
    });

    const indefiniteDeadlines = computed(() => {
      return deadlines.value.filter(task => !task.deadline_time && task.status == 0);
    });

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
    const aiLoading = ref(false); // состояние загрузки в AI модалке

    // New Add Task Modal State
    const isAddTaskModalOpen = ref(false);
    const newTaskData = ref({
      description: "",
      date: "",
      time: "",
      priority: 0,
    });

    const isAIResultModalOpen = ref(false);
    const aiDeadlines = ref([]);

    // New AI Task Edit Modal State
    const isAIEditModalOpen = ref(false);
    const editAITask = ref({
      id: null,
      description: "",
      deadline_time: "",
    });
    const editAITaskDate = ref("");
    const editAITaskTime = ref("");

    const taskInputMode = ref("text");
    document.body.style.overflowY = 'hidden';

    const isInfiniteDeadline = ref(false);
    const deadlineViewMode = ref("byDays");
    const upcomingDeadlines = computed(() => {
      return deadlines.value.filter(
        task => task.deadline_time && new Date(task.deadline_time) > new Date() && task.status == 0
      );
    });
    const overdueDeadlines = computed(() => {
      return deadlines.value.filter(
        task => task.deadline_time && new Date(task.deadline_time) < new Date() && task.status == 0
      );
    });

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
    const getUser = async () => {
      try {
        const token = getToken();
        if (token == null) {
          return -1
        }
        const response = await axios.get(`http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/user/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        return response.data;
      } catch (error) {
          return -1
      }
    };

    const fetchUser = async () => {
      user.value = await getUser()
    }

    /**
     * Запрос всех задач (дедлайнов).
     */
    const fetchDeadlines = async () => {
      try {
        const token = getToken();
        const response = await axios.get(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/get_tasks/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        deadlines.value = response.data.map(task => ({
          ...task,
          deadline_time: task.deadline_time ? new Date(task.deadline_time).toISOString() : null,
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
        const priority = 0;

        await axios.post(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/create_deadline_task`,
          { description, deadline_time, priority },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

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
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/complete_task`,
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
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/delete_task`,
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
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/return_to_active`,
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
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/ai_generation`,
          { text: user_text },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
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
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/submit_ai_generation`,
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
      return usual_deadlines.value.reduce((groups, task) => {
        const localDate = new Date(task.deadline_time);
        const year = localDate.getFullYear();
        const month = String(localDate.getMonth() + 1).padStart(2, "0");
        const day = String(localDate.getDate()).padStart(2, "0");
        const dateKey = `${year}-${month}-${day}`; // Формируем ключ в локальном времени

        if (!groups[dateKey]) {
          groups[dateKey] = [];
        }
        groups[dateKey].push(task);
        return groups;
      }, {});
    });

    /**
     * Формирование списка ближайших 30 дней с фильтрацией задач.
     */
    const allDaysWithTasks = computed(() => {
      const days = Array.from({ length: 30 }, (_, i) => {
        const date = new Date();
        date.setDate(date.getDate() + i);
        return date.toLocaleDateString("en-CA");
      });

      return days.reduce((result, day) => {
        if (!newTask.value[day]) {
          newTask.value[day] = { description: "", time: "" };
        }
        if (dayFilters.value[day] === undefined) {
          dayFilters.value[day] = 0;
        }
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
     * Открыть модалку редактирования для обычных задач.
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
     * Закрыть модалку редактирования для обычных задач.
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
        const [year, month, day] = date.split("-");
        const [hours, minutes] = time.split(":");
        const deadlineDate = new Date(year, month - 1, day, hours, minutes);
        const deadline_time = deadlineDate.toISOString();

        await axios.put(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/update_task`,
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
      aiLoading.value = false;
    };

    /**
     * Отправить запрос для генерации задач (AI).
     * Сразу переключаем отображение на спиннер, а после ответа открываем форму Add New Task.
     */
    const submitAI = async () => {
      if (aiInput.value.trim() === "") {
        alert("Please enter a task description.");
        return;
      }
      aiLoading.value = true;
      try {
        await AIGeneration(aiInput.value.trim());
        closeAIModal();
      } catch (error) {
        console.error("Error submitting AI task:", error);
      } finally {
        aiLoading.value = false;
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
      const { description, date, time, priority } = newTaskData.value;
      if (!description.trim()) {
        alert("Please fill in all fields.");
        return;
      }

      let deadline_time = null;
      if (!isInfiniteDeadline.value) {
        if (!date || !time) {
          alert("Please fill in all fields.");
          return;
        }
        const deadlineDate = new Date(`${date}T${time}`);
        deadline_time = deadlineDate.toISOString();
      }

      try {
        const token = getToken();
        await axios.post(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/create_deadline_task`,
          { description: description.trim(), deadline_time, priority },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        newTaskData.value = { description: "", date: "", time: "", priority: 0 };
        isInfiniteDeadline.value = false;
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
     */
    const getDeadlineTimeClass = (task) => {
      const deadlineTime = new Date(task.deadline_time);
      const now = new Date();
      const diffMs = deadlineTime - now;
      const diffHours = diffMs / (1000 * 60 * 60);
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

    /**
     * Открыть модалку редактирования AI задачи.
     */
    const openAIEditModal = (task) => {
      editAITask.value = { ...task };
      const deadline = new Date(task.deadline_time);
      editAITaskDate.value = deadline.toISOString().split('T')[0];
      const hours = String(deadline.getHours()).padStart(2, "0");
      const minutes = String(deadline.getMinutes()).padStart(2, "0");
      editAITaskTime.value = `${hours}:${minutes}`;
      isAIEditModalOpen.value = true;
    };

    /**
     * Закрыть модалку редактирования AI задачи.
     */
    const closeAIEditModal = () => {
      isAIEditModalOpen.value = false;
    };

    /**
     * Сохранить изменения AI задачи и обновить список aiDeadlines.
     */
    const submitAIEdit = () => {
      const newDeadline = new Date(`${editAITaskDate.value}T${editAITaskTime.value}`).toISOString();
      editAITask.value.deadline_time = newDeadline;
      const index = aiDeadlines.value.findIndex(task => task.id === editAITask.value.id);
      if (index !== -1) {
        aiDeadlines.value[index] = { ...editAITask.value };
      }
      isAIEditModalOpen.value = false;
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
      aiLoading,
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
      // AI Task Edit Modal
      isAIEditModalOpen,
      editAITask,
      editAITaskDate,
      editAITaskTime,
      openAIEditModal,
      closeAIEditModal,
      submitAIEdit,
      taskInputMode,
      invalidUserPanel,
      isInfiniteDeadline,
      usual_deadlines,
      deadlineViewMode,
      upcomingDeadlines,
      overdueDeadlines,
      indefiniteDeadlines,
    };
  },
};
</script>

<style scoped>
/* Импортируем шрифт Inter из Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

.page-wrapper {
  position: relative;
  z-index: 0;
}

.page-container {
  display: flex;
  min-height: 100vh;
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}

.content-container {
  flex: 1;
  padding: 1.25rem; /* 20px */
  box-sizing: border-box;
  overflow: hidden;
}

.background-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 120vw;
  height: 100vh;
  /* Пример фона – можно заменить на нужное изображение или другой стиль */
  background: url('../../../public/dl2.jpg') no-repeat center center;
  background-size: cover;
  z-index: -1;
  opacity: 0.8;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem; /* 20px */
}

.title {
  margin: 0;
  font-size: 4.5rem;
}

.header-buttons {
  display: flex;
  gap: 0.625rem; /* 10px */
}

.add-easier-button {
  background: linear-gradient(45deg, #3498db, #e67e22);
  color: white;
  border: none;
  width: 9.375rem; /* 150px */
  height: 3.125rem; /* 50px */
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 0.5rem; /* 8px */
  transition: background 0.3s, transform 0.3s, box-shadow 0.3s;
  margin-left: -20%;
  box-shadow: 0 0.25rem 0.375rem rgba(0, 0, 0, 0.1);
}

.add-easier-button:hover {
  background: linear-gradient(45deg, #2980b9, #d35400);
  transform: translateY(-0.125rem); /* 2px */
  box-shadow: 0 0.375rem 0.5rem rgba(0, 0, 0, 0.15);
}

.add-easier-button:active {
  transform: translateY(0);
  box-shadow: 0 0.25rem 0.375rem rgba(0, 0, 0, 0.1);
}

.add-task-button {
  background-color: white;
  color: #7f8c8d;
  border: 1px solid #ccc;
  width: 9.375rem; /* 150px */
  height: 3.125rem; /* 50px */
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 0.5rem; /* 8px */
  transition: background-color 0.3s, border-color 0.3s, transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 0.25rem 0.375rem rgba(0, 0, 0, 0.1);
}

.add-task-button:hover {
  background-color: #f0f0f0;
  border-color: #a0a0a0;
  transform: translateY(-0.125rem); /* 2px */
  box-shadow: 0 0.375rem 0.5rem rgba(0, 0, 0, 0.15);
}

.add-task-button:active {
  background-color: #e0e0e0;
  border-color: #909090;
  transform: translateY(0);
  box-shadow: 0 0.25rem 0.375rem rgba(0, 0, 0, 0.1);
}

.deadline-wrapper {
  display: flex;
  position: relative;
}

.scroll-button {
  position: fixed;
  width: 2.5rem; /* 40px */
  height: 2.5rem; /* 40px */
  background-color: white;
  border: 0.05rem solid #bdc3c7; /* 2px */
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.1);
  padding: 0;
  z-index: 10;
}

.scroll-button.scroll-left {
  /* Если требуется позиционирование относительно контейнера, можно использовать проценты */
  left: 14.7rem; /* 250px, можно заменить на процентное значение при необходимости */
  top: 27%;
  transform: translateY(-50%);
}

.scroll-button.scroll-right {
  right: 1.3rem; /* 30px */
  top: 27%;
  transform: translateY(-50%);
}

.scroll-button:hover {
  background-color: #ecf0f1;
  transform: translateY(-50%) scale(1.05);
}

.scroll-button:active {
  transform: translateY(-50%) scale(0.95);
}

.deadline-list {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  flex-wrap: nowrap;
  width: 100%;
  margin: 0 3.75rem; /* 60px */
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.deadline-list::-webkit-scrollbar {
  display: none;
}

.deadline-day-wrapper {
  display: flex;
  flex-direction: column;
  margin-right: 1.25rem; /* 20px */
  position: relative;
}

.deadline-day {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffffff;
  border-radius: 1.25rem; /* 20px */
  padding: 0.9375rem; /* 15px */
  box-shadow: 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.1);
  width: 18.75rem; /* 300px */
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.625rem; /* 10px */
}

.day-title {
  font-size: 1.5rem;
  color: #000000;
  text-align: center;
  margin: 0 auto;
}

.filter-buttons {
  position: absolute;
  top: 0.625rem; /* 10px */
  right: 0.625rem; /* 10px */
  display: flex;
  gap: 0.3125rem; /* 5px */
  z-index: 10;
}

.filter-button {
  background: #fff;
  border: 0.125rem solid #87CEEB; /* 2px */
  color: #87CEEB;
  border-radius: 1.25rem; /* 20px */
  padding: 0.375rem 1rem; /* 6px 16px */
  font-size: 0.9rem;
  font-weight: 600;
  transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s;
  cursor: pointer;
  margin-bottom: 0.9375rem; /* 15px */
}

.filter-button:hover {
  background-color: #4daceb;
  transform: scale(1.05);
}

.filter-button:active {
  transform: scale(0.95);
}

.tasks {
  margin-top: 2.1875rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-height: 3.125rem;
  width: 100%;
}

.empty-task-card {
  color: #9e9e9e;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 3.125rem; /* 50px */
}

.task-card {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 1.25rem; /* 20px */
  padding: 0.9375rem; /* 15px */
  background-color: #ffffff;
  flex-direction: row;
  position: relative;
  box-shadow: 0 0.1875rem 0.3125rem rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}

.task-card .task-details .task-name {
  margin-left: 0.15rem; /* подберите значение по вкусу */
}

.task-card:hover {
  background-color: #f0f8ff;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.2);
}

.task-status {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.task-status input {
  width: 0.9375rem; /* 15px */
  height: 0.9375rem; /* 15px */
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
  gap: 0.3125rem; /* 5px */
}

.time-icon {
  width: 0.75rem; /* 12px */
  height: 0.75rem; /* 12px */
  color: #555;
  flex-shrink: 0;
}

.task-time {
  font-size: 0.9rem;
  margin: 0;
  line-height: 1;
}

.deadline-bg-red {
  background-color: #ffcccc;
  padding: 0.125rem 0.375rem; /* 2px 6px */
  border-radius: 0.9375rem; /* 15px */
}

.deadline-bg-yellow {
  background-color: #ffffcc;
  padding: 0.125rem 0.375rem;
  border-radius: 0.9375rem;
}

.deadline-bg-purple {
  background-color: #e6ccff;
  padding: 0.125rem 0.375rem;
  border-radius: 0.9375rem;
}

.new-task-form {
  display: flex;
  align-items: center;
  gap: 0.625rem; /* 10px */
  margin-top: 0.9375rem; /* 15px */
}

.new-task-input {
  flex: 2;
  padding: 0.3125rem; /* 5px */
  height: 2.1875rem; /* 35px */
  border: 1px solid #ccc;
  border-radius: 3.125rem; /* 50px */
  font-size: 0.9rem;
  color: #555;
  background-color: white;
  box-shadow: 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s, box-shadow 0.3s;
  padding-left: 0.625rem; /* 10px */
  box-sizing: border-box;
}

.new-task-input:focus {
  border-color: #3498db;
  box-shadow: 0 0 0.5rem rgba(52, 152, 219, 0.5);
}

.new-task-time {
  flex: 1;
  padding: 0.3125rem;
  height: 2.1875rem;
  border: 1px solid #ccc;
  border-radius: 3.125rem;
  font-size: 0.9rem;
  text-align: center;
  color: #555;
  appearance: none;
  background-color: white;
  box-shadow: 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.new-task-time:focus {
  border-color: #3498db;
  box-shadow: 0 0 0.5rem rgba(52, 152, 219, 0.5);
}

.new-task-time::placeholder {
  color: #aaa;
  font-style: italic;
}

.new-task-time::-webkit-calendar-picker-indicator {
  display: none;
}

.create-task-button {
  width: 2.5rem; /* 40px */
  height: 2.5rem; /* 40px */
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

.action-buttons {
  position: absolute;
  top: 0.625rem; /* 10px */
  right: 0.625rem; /* 10px */
  display: flex;
  gap: 0.3125rem; /* 5px */
}

.edit-button,
.delete-button,
.return-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.3125rem; /* 5px */
  border-radius: 0.3125rem; /* 5px */
  transition: background-color 0.3s, color 0.3s;
  font-size: 0.8rem;
  white-space: nowrap;
}

.return-button {
  background-color: #2ecc71;
  color: white;
  padding: 0.3125rem 0.625rem; /* 5px 10px */
  border-radius: 0.9375rem; /* 15px */
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
}

.modal-content form {
  display: flex;
  flex-direction: column;
}

.modal-content label {
  margin-bottom: 0.9375rem; /* 15px */
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
}

.modal-buttons button {
  padding: 0.5rem 1rem; /* 8px 16px */
  border: none;
  border-radius: 0.3125rem; /* 5px */
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

.ai-deadlines-list {
  max-height: 18.75rem; /* 300px */
  overflow-y: auto;
  margin-bottom: 1.25rem; /* 20px */
}

.ai-task {
  padding: 0.625rem; /* 10px */
  border-bottom: 0.0625rem solid #ddd; /* 1px */
}

.ai-task:last-child {
  border-bottom: none;
}

.ai-task p {
  margin: 0.3125rem 0; /* 5px 0 */
}

.ai-task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.3125rem; /* 5px */
}

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 6.25rem; /* 100px */
}

.spinner {
  animation: spin 1s linear infinite;
  width: 3.125rem; /* 50px */
  height: 3.125rem; /* 50px */
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

.arrow-button {
  background: none;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  padding: 0;
}

.arrow-button:hover {
  transform: scale(1.1);
}

textarea.text-box {
  width: 100%;
  height: 200px; /* фиксированная высота */
  margin: 0; /* убраны внешние отступы */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 12px;
  box-sizing: border-box;
  overflow-y: auto;
  font-size: 0.9rem;
  font-family: 'Inter', sans-serif;
  text-align: left;
  vertical-align: top;
  line-height: 1.5;
  margin-bottom: 0.8rem;
  margin-top: 0.5rem;
}

/* Дополнительное правило для textarea */
textarea.text-box {
  resize: none;
}

.text-box::-webkit-scrollbar {
  width: 8px;
}

.text-box::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.text-box::-webkit-scrollbar-thumb {
  background: #cacaca;
  border-radius: 4px;
}

.text-box::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Фиксированный размер модального окна */
.fixed-form-size {
  width: 25rem;
  max-width: 90%;
  min-height: 30rem; /* Фиксированная минимальная высота */
  padding: 1.875rem; /* 30px */
  border-radius: 0.625rem; /* 10px */
  box-shadow: 0 0.3125rem 0.9375rem rgba(0, 0, 0, 0.3);
  background-color: #fff;
  position: relative;
}

/* Обёртка для форм, чтобы их высота не менялась */
.form-container {
  min-height: 10rem;
}

/* Переключатель режимов ввода */
.toggle-button {
  display: inline-flex;
  align-items: center;
}

.toggle-button button {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  background-color: #e0e0e0; /* цвет неактивной кнопки */
  border: none;
  cursor: pointer;
  border-radius: 1.5rem;
  margin-right: 0.5rem;
  transition: background-color 0.3s;
}

.toggle-button button.active {
  background-color: #f0f0f0; /* активное состояние – светлее */
}

h3 {
  margin-top: 1rem;
  color: #717781;
  margin-bottom: 0rem;
  font-size: 0.95rem;
}

.modal-buttons {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  gap: 0.625rem;
}

.modal-buttons button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.3125rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* Стиль для кнопки отправки */
.modal-buttons button[type="submit"] {
  background-color: #4285F4;
  color: #fff;
}

/* Стиль для кнопки отмены */
.modal-buttons button[type="button"] {
  background-color: #d86154;
  color: #fff;
}

.toggle-switch {
  position: relative;
  display: flex;
  width: 10rem;         /* можно скорректировать по необходимости */
  height: 1.5rem;
  background-color: #ccc;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  margin-bottom: 1rem;
}

.toggle-slider {
  position: absolute;
  top: 0;
  left: 0;
  width: 52%;
  height: 100%;
  background-color: #f3f1f1;
  border-radius: 20px;
  transition: left 0.3s;
}

.toggle-slider.manual {
  left: 50%;
}

.toggle-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  font-size: 0.8rem;
  color: #000000;
  user-select: none;
}

.toggle-option:hover {
  color: #000;
}

.manual-add-task-form {
  margin-top: -1rem;
}

.description-input {
  font-size: 0.9rem;
  color: #717781;
}

.infinite-deadline-toggle {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  margin-top: 1rem;
  margin-bottom: -0.5rem;
}

.custom-toggle {
  width: 40px;
  height: 20px;
  background-color: #ccc;
  border-radius: 10px;
  position: relative;
  transition: background-color 0.3s;
  margin-right: 0.5rem;
}

.custom-toggle.active {
  background-color: #4285F4;
}

.toggle-circle {
  width: 16px;
  height: 16px;
  background-color: #fff;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.3s;
}

.custom-toggle.active .toggle-circle {
  transform: translateX(20px);
}

.toggle-label {
  color: #717781;
  font-size: 0.9rem;
  margin-top: -2px;
}

.title-container {
  display: flex;
  align-items: flex-end;
  gap: 2rem;
}

.all-deadlines-wrapper {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  max-width: 70vw; /* задаёт фиксированную максимальную ширину */
  margin-left: 0;   /* начинаем с левого края */
}

/* Задаём фиксированную ширину для каждой карточки */
.all-deadline-card {
  width: 25vw;                /* зафиксированная ширина формы */
  height: 60vh;               /* зафиксированная высота формы */
  display: flex;               /* даём дочерним элементам выстраиваться колонкой */
  flex-direction: column;
  background-color: #fff;
  border-radius: 1.25rem;
  padding: 0.9375rem;
  box-shadow: 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.1);
}

.all-deadline-card .task-card {
  margin-bottom: 0.5rem; /* увеличенный отступ только внутри карточек "All" */
}

/* Поднимаем заголовок карточки и уменьшаем размер шрифта */
.all-deadline-card .card-header {
  margin-top: 0;
  padding-bottom: 0.5rem;
  height: auto;       /* убираем фиксированную высоту заголовка */
  overflow: visible;  /* при желании можно оставить auto/visible */
}

.all-deadline-card .card-content {
  flex-grow: 1;       /* занимаем всё оставшееся место в карточке */
  overflow-y: auto;   /* добавляем вертикальную прокрутку для дедлайнов */
}

.all-deadline-card .card-header h2 {
  font-size: 0.9rem;  /* уменьшаем шрифт заголовка */
  margin-bottom: 0.5rem;
}

.card-content {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.all-deadline-card .task-card .action-buttons {
  display: none;
}

/* Показываем иконку при наведении на карточку */
.all-deadline-card .task-card:hover .action-buttons {
  display: block;
}

/* Выравнивание даты по правому краю и изменение цвета */
.all-deadline-card .deadline-date {
  display: inline-block;
  width: 9rem; /* подберите нужную ширину */
  margin-left: auto;
  text-align: left;
  color: grey;
  font-size: 0.85rem;
}

.all-deadline-card .task-time-container {
  white-space: nowrap;
}

.toggle-switch.deadline-view-switch {
  width: 350px;       /* фиксированная ширина */
  height: 550px;
  position: relative;
  display: flex;
  width: 10rem;  /* например, 160px */
  height: 1.5rem;
  background-color: #ccc; /* "пассивный" фон переключателя */
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
}

/* Сам "ползунок" */
.toggle-slider {
  position: absolute;
  top: 0;
  left: 0;
  width: 55%;
  height: 100%;
  background-color: #fff; /* цвет активной половинки */
  border-radius: 20px;
  transition: left 0.3s;
}
.toggle-slider.all {
  left: 50%; /* Если .all, двигаем ползунок вправо */
}

/* Текст внутри переключателя */
.toggle-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  color: #000; /* текст по умолчанию */
  font-size: 0.9rem;
  user-select: none;
  transition: color 0.3s;
}

/* Когда опция активна, делаем текст белым */
.toggle-option.active {
  color: #fff;
}

/* Три колонки во вкладке "All" */
.all-deadlines-wrapper {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.all-deadline-card {
  flex: 1;
  background-color: #fff;
  border-radius: 1.25rem;
  padding: 0.9375rem;
  box-shadow: 0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.1);
}

.priority-block {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.priority-slider-container {
  width: 50%; /* полвина ширины формы */
  position: relative;
  z-index: 3;
}

.tick-label {
  font-size: 0.8rem;
  color: #ccc; /* светло-серый цвет */
}

.priority-slider {
  width: 100%;
  background: #ddd;
  height: 4px;
  border-radius: 2px;
  outline: none;
}

/* Стили для Webkit */
.priority-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff; /* белый шарик */
  border: 1px solid #ccc;
  cursor: pointer;
  z-index: 2;
}

/* Стили для Firefox */
.priority-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #fff;
  border: 1px solid #ccc;
  cursor: pointer;
  z-index: 2;
}

.slider-ticks {
  position: absolute;
  top: 36%; /* Центрируем по вертикали ползунка */
  transform: translateY(-50%);
  width: 100%;
  pointer-events: none;
  z-index: 1;
}

.slider-ticks .tick {
  position: absolute;
  width: 2px;           /* увеличенная ширина */
  height: 12px;         /* увеличенная высота */
  background-color: #888;
  transform: translateY(-50%);
}

/* Надписи под черточками */
.priority-labels {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 4px; /* немного ближе к ползунку */
}
</style>
