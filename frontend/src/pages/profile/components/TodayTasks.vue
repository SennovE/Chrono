<template>
    <div class="task-carousel">
      <h2>Задания на сегодня</h2>
      
      <div v-if="loading" class="loading-indicator">
        Загрузка заданий...
      </div>
      
      <div class="carousel-container" v-else-if="tasks.length > 0">
        <button
          class="nav-button left"
          @click="prev"
          :disabled="currentIndex === 0"
        >
          &#8592;
        </button>
        
        <div class="tasks-wrapper">
          <div
            class="tasks"
            :style="`transform: translateX(-${currentIndex * (100 / visibleTasksCount)}%);`"
          >
            <div
              class="task-card"
              v-for="task in visibleTasksList"
              :key="task.id"
              :style="`width: ${100 / visibleTasksCount}%`"
            >
              <div class="task-content">
                <h3>{{ task.title }}</h3>
                <p>{{ task.description }}</p>
              </div>
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
          class="nav-button right"
          @click="next"
          :disabled="isLastPage"
        >
          &#8594;
        </button>
      </div>
      
      <p v-else-if="!error">Нет заданий на сегодня.</p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { ref, onMounted, computed, onBeforeUnmount } from 'vue';
  
  export default {
    name: 'TaskCarousel',
    setup() { 
      // Реактивные переменные
      const user = ref({ 
        username: "Loading...", 
        avatarUrl: "https://via.placeholder.com/190" 
      });
      
      const tasks = ref([]); // Отфильтрованные задачи на сегодня и не завершённые
      const allTasks = ref([]); // Все задачи, полученные с сервера
      const currentIndex = ref(0);
      const visibleTasksCount = ref(4); // Количество видимых задач
      const error = ref(null);
      const loading = ref(true); // Индикатор загрузки
      
      // Функция для получения токена из localStorage
      const getToken = () => {
        const token = localStorage.getItem("chronoJWTToken");
        if (!token) {
          throw new Error("Token is missing. Please log in.");
        }
        return token;
      };
  
      // Функция для получения данных пользователя
      const fetchUser = async () => {
        try {
          const token = getToken();
          const response = await axios.get("http://localhost:8080/api/v1/user/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          user.value = response.data;
        } catch (err) {
          console.error("Error fetching user:", err);
          error.value = "Не удалось загрузить данные пользователя.";
        }
      };
  
      // Функция для получения и фильтрации задач на сегодня и не завершённых
      const fetchDeadlines = async () => {
        try {
          loading.value = true;
          const token = getToken();
          const response = await axios.get(
            "http://localhost:8080/api/v1/deadline_task/get_tasks/",
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          
          // Преобразуем deadline_time в объект Date и добавляем поле completed
          allTasks.value = response.data.map(task => ({
            ...task,
            deadline_time: new Date(task.deadline_time),
          }));
          
          // Определяем сегодняшнюю дату
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          
          // Определяем завтрашнюю дату
          const tomorrow = new Date(today);
          tomorrow.setDate(tomorrow.getDate() + 1);
          
          // Фильтруем задачи, дедлайн которых сегодня и не завершены
          const todaysTasks = allTasks.value.filter(task => {
            const deadline = task.deadline_time;
            return deadline >= today && deadline < tomorrow && task.status == 0;
          });
          
          // Преобразуем deadline_time обратно в ISO строку, если необходимо
          tasks.value = todaysTasks.map(task => ({
            ...task,
            deadline_time: task.deadline_time.toISOString(),
          }));
          
          // Сбрасываем индекс карусели при загрузке новых задач
          currentIndex.value = 0;
          
        } catch (err) {
          console.error("Error fetching deadlines:", err);
          error.value = "Не удалось загрузить задания.";
        } finally {
          loading.value = false;
        }
      };
  
      // Функция для отметки задачи как выполненной
      const markTaskAsComplete = async (taskId) => {
        const confirmDelete = confirm("Вы уверены, что хотите отметить эту задачу как выполненную?");
        if (!confirmDelete) return;
        
        try {
          const token = getToken();
          // Отправляем запрос для завершения задачи
          await axios.post(
            "http://localhost:8080/api/v1/deadline_task/complete_task",
            { id: taskId },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
  
          console.log(`Задача с ID ${taskId} отмечена как выполненная.`);
  
          // Обновляем список задач
          await fetchDeadlines();
        } catch (error) {
          console.error("Error completing task:", error);
          alert("Не удалось отметить задачу как выполненную.");
        }
      };
  
      // Функции навигации карусели
      const prev = () => {
        if (currentIndex.value > 0) {
          currentIndex.value--;
        }
      };
  
      const next = () => {
        if ((currentIndex.value + visibleTasksCount.value) < tasks.value.length) {
          currentIndex.value++;
        }
      };
  
      // Вычисляемое свойство для форматированной даты
      const formattedToday = computed(() => {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
      });
  
      // Вычисляемое свойство для определения, достигнут ли конец списка
      const isLastPage = computed(() => {
        return (currentIndex.value + visibleTasksCount.value) >= tasks.value.length;
      });
  
      // Вычисляемое свойство для отображаемых задач в текущей странице карусели
      const visibleTasksList = computed(() => {
        const start = currentIndex.value * visibleTasksCount.value;
        const end = start + visibleTasksCount.value;
        return tasks.value.slice(start, end);
      });
  
      // Обработчик изменения размера окна для адаптации количества видимых задач
      const updateVisibleTasksCount = () => {
        const width = window.innerWidth;
        if (width >= 1200) {
          visibleTasksCount.value = 4;
        } else if (width >= 992) {
          visibleTasksCount.value = 3;
        } else if (width >= 768) {
          visibleTasksCount.value = 2;
        } else {
          visibleTasksCount.value = 1;
        }
        // Сбрасываем индекс при изменении количества видимых задач
        currentIndex.value = 0;
      };
  
      // Жизненный цикл компонента
      onMounted(() => {
        fetchUser();
        fetchDeadlines();
        updateVisibleTasksCount();
        window.addEventListener('resize', updateVisibleTasksCount);
      });
  
      // Удаляем обработчик при уничтожении компонента
      onBeforeUnmount(() => {
        window.removeEventListener('resize', updateVisibleTasksCount);
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
      };
    },
  };
  </script>
  
  <style scoped>
  .task-carousel {
    position: absolute;
    top: 190px; /* Указание позиции отдельно */
    left: 1000px; /* Центрирование по горизонтали */
    transform: translateX(-50%); /* Центрирование по горизонтали */
    border: 1px solid #272626;
    padding: 16px;
    border-radius: 8px;
    width: 60%;
    max-width: 1200px;
    margin: 0 auto;
    background-color: #1b1a1a;
    color: #ffffff; /* Изменение цвета текста на светлый для контраста с темным фоном */
  }
  
  .task-carousel h2 {
    text-align: center;
    margin-bottom: 16px;
  }
  
  .loading-indicator {
    text-align: center;
    font-size: 18px;
    color: #ffffff;
  }
  
  .carousel-container {
    display: flex;
    align-items: center;
    position: relative;
  }
  
  .nav-button {
    background-color: #007bff;
    border: none;
    color: white;
    padding: 12px;
    cursor: pointer;
    border-radius: 50%;
    font-size: 18px;
    transition: background-color 0.3s;
  }
  
  .nav-button:disabled {
    background-color: #555555;
    cursor: not-allowed;
  }
  
  .nav-button:hover:not(:disabled) {
    background-color: #0056b3;
  }
  
  .tasks-wrapper {
    overflow: hidden;
    width: 100%;
    margin: 0 16px;
  }
  
  .tasks {
    display: flex;
    transition: transform 0.5s ease-in-out;
  }
  
  .task-card {
    position: relative; /* Для позиционирования кнопки удаления */
    background: #2c2c2c;
    margin: 0 8px;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.5);
    box-sizing: border-box;
    transition: background-color 0.3s;
  }
  
  .task-card:hover {
    background-color: #3a3a3a;
  }
  
  .delete-button {
    position: absolute;
    top: 8px;
    right: 8px;
    background: transparent;
    border: none;
    color: #ff4d4d;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.3s;
  }
  
  .task-card:hover .delete-button {
    opacity: 1;
  }
  
  .delete-button:hover {
    color: #ff1a1a;
  }
  
  .error {
    color: red;
    text-align: center;
    margin-top: 16px;
  }
  
  @media (max-width: 1200px) {
    .task-carousel {
      width: 80%;
    }
    .task-card {
      padding: 12px;
    }
  }
  
  @media (max-width: 768px) {
    .task-carousel {
      width: 95%;
    }
    .task-card {
      padding: 8px;
    }
    
    .nav-button {
      padding: 8px;
      font-size: 16px;
    }
  }
  </style>
  