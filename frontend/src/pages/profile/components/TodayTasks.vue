<template>
  <div class="task-carousel">
    <h2>Задания на сегодня</h2>
    
    <div v-if="loading" class="loading-indicator">
      Загрузка заданий...
    </div>
    
    <div class="carousel-container" v-else-if="tasks.length > 0">
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
          :style="`transform: translateY(-${currentIndex * (100 / visibleTasksCount)}%);`"
        >
          <div
            class="task-card"
            v-for="task in visibleTasksList"
            :key="task.id"
            :style="`height: ${100 / visibleTasksCount}%`"
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
    top: 40px; /* Указание позиции отдельно */
    left: 450px;
  border: 1px solid var(--color-dark-grey); /* Светло-серая граница */
  padding: 16px; /* Увеличен паддинг для внутреннего отступа */
  border-radius: 8px;
  width: 50%; /* Ширина может быть скорректирована при необходимости */
  max-width: 800px;
  margin: 100px auto; /* Центрирование компонента с отступом сверху */
  background-color: var(--color-brighter-black); /* Белый фон */
  color: var(--color-black); /* Темно-серый текст */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Лёгкая тень для глубины */
}

.task-carousel h2 {
  text-align: center;
  margin-bottom: 16px;
  color: var(--color-black); /* Темно-серый цвет заголовка */
}

.loading-indicator {
  text-align: center;
  font-size: 18px;
  color: var(--color-grey); /* Светло-серый цвет */
}

.carousel-container {
  display: flex;
  flex-direction: row; /* Горизонтальное расположение */
  align-items: center;
  position: relative;
}

.nav-button {
  background-color: var(--color-deep-purple); /* Акцентный пурпурный цвет */
  border: none;
  color: #ffffff; /* Белый текст */
  padding: 12px;
  cursor: pointer;
  border-radius: 50%;
  font-size: 9px;
  transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  margin: 4px 0; /* Добавляет вертикальный отступ между кнопками */
  flex-shrink: 0; /* Не позволяет кнопкам сжиматься */
}

.nav-buttons-container {
  display: flex;
  flex-direction: column; /* Кнопки располагаются вертикально */
  justify-content: center;
  align-items: center;
  margin-right: 8px; /* Расстояние между кнопками и задачами */
}

.nav-button:disabled {
  background-color: var(--color-dark-grey); /* Светло-серая кнопка при отключении */
  cursor: not-allowed;
  opacity: 0.6;
}

.nav-button:hover:not(:disabled) {
  background-color: #5e0cff; /* Немного светлее пурпурный при наведении */
  transform: scale(1.1); /* Увеличивает кнопку при наведении */
  box-shadow: 0 4px 8px rgba(94, 12, 255, 0.3);
}

.tasks-wrapper {
  overflow: hidden;
  flex-grow: 1; /* Задачи занимают оставшееся пространство */
  height: 100%; /* Высота равна контейнеру */
}

.tasks-wrapper {
  overflow: hidden;
  width: 100%;
  height: calc(100% / var(--visible-tasks-count) * var(--visible-tasks-count)); /* Высота контейнера */
  margin: 0 16px;
}

.tasks {
  display: flex;
  flex-direction: column; /* Вертикальное расположение задач */
  transition: transform 0.5s ease-in-out;
}

.task-card {
  position: relative; /* Для позиционирования кнопки удаления */
  background: var(--color-dark-grey); /* Светло-серый фон карточки */
  margin: 8px 0;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Лёгкая тень для карточки */
  box-sizing: border-box;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.task-card:hover {
  background-color: #f5f5f5; /* Очень светло-серый фон при наведении */
  box-shadow: 0 4px 10px rgba(0,0,0,0.15); /* Усиленная тень при наведении */
}

.task-content {
  margin-bottom: 8px;
}

.task-content h3 {
  margin: 0 0 8px 0;
  color: var(--color-black); /* Темно-серый цвет заголовка */
}

.task-content p {
  margin: 0;
  color: var(--color-grey); /* Светло-серый текст */
}

.delete-button {
  position: absolute;
  top: 8px;
  right: 8px;
  background: transparent;
  border: none;
  color: var(--color-red); /* Красный цвет для кнопки удаления */
  font-size: 20px;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.3s, color 0.3s;
}

.task-card:hover .delete-button {
  opacity: 1;
}

.delete-button:hover {
  color: #cc0000; /* Более тёмный красный при наведении */
}

.error {
  color: var(--color-red); /* Красный цвет для ошибок */
  text-align: center;
  margin-top: 16px;
}

@media (max-width: 1200px) {
  .task-carousel {
    width: 80%; /* Увеличена ширина на средних экранах */
  }
  .task-card {
    padding: 12px; /* Уменьшен паддинг */
  }
}

@media (max-width: 768px) {
  .task-carousel {
    width: 95%; /* Увеличена ширина на мобильных устройствах */
    padding: 12px; /* Уменьшен паддинг */
    margin: 80px auto; /* Отступ снизу уменьшен */
  }
  .task-card {
    padding: 8px; /* Дополнительное уменьшение паддинга */
  }
  
  .nav-button {
    padding: 8px;
    font-size: 16px;
    width: 35px;
    height: 35px;
  }
}
</style>

  