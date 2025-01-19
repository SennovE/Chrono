<template>
  <div class="task-statistics">
    <h2>Статистика задач</h2>
    
    <div class="controls">
      <button 
        :class="{ active: selectedPeriod === 'day' }" 
        @click="selectedPeriod = 'day'"
      >
        День
      </button>
      <button 
        :class="{ active: selectedPeriod === 'week' }" 
        @click="selectedPeriod = 'week'"
      >
        Неделя
      </button>
    </div>
    
    <div v-if="loading" class="loading-indicator">
      Загрузка статистики...
    </div>
    
    <div v-else class="chart-container">
      <BarChart :chartData="chartData" :options="chartOptions" />
    </div>
    
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import BarChart from './BarChart.vue'; // Убедитесь, что путь правильный

export default {
  name: 'TaskStatistics',
  components: {
    BarChart
  },
  setup() {
    const tasks = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const selectedPeriod = ref('day'); // 'day' или 'week'

    const getToken = () => {
      const token = localStorage.getItem("chronoJWTToken");
      if (!token) {
        throw new Error("Token is missing. Please log in.");
      }
      return token;
    };

    const fetchTasks = async () => {
      try {
        loading.value = true;
        error.value = null;
        const token = getToken();
        const response = await axios.get(
          "http://localhost:8080/api/v1/deadline_task/get_tasks/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        
        // Предполагаем, что API возвращает поле status и deadline_time
        tasks.value = response.data.map(task => ({
          ...task,
          deadline_time: new Date(task.deadline_time),
        }));
      } catch (err) {
        console.error("Error fetching tasks:", err);
        error.value = "Не удалось загрузить задачи.";
      } finally {
        loading.value = false;
      }
    };

    // Функция для агрегации данных
    const aggregateData = () => {
      const counts = {
        active: 0,
        completed: 0,
        overdue: 0,
      };

      tasks.value.forEach(task => {
        if (task.status === 1) {
          counts.completed += 1;
        } else if (task.status === 2) {
          counts.overdue += 1;
        } else if (task.status === 0) {
          counts.active += 1;
        }
      });

      return counts;
    };

    // Функция для получения данных для графика в зависимости от выбранного периода
    const getChartData = () => {
      if (selectedPeriod.value === 'day') {
        // Для дня отображаем общее количество задач по статусам
        const counts = aggregateData();
        return {
          labels: ['Активные', 'Завершенные', 'Просроченные'],
          datasets: [
            {
              label: 'Количество задач',
              backgroundColor: ['#3498db', '#2ecc71', '#e74c3c'],
              data: [counts.active, counts.completed, counts.overdue]
            }
          ]
        };
      } else  {
        // Для недели отображаем динамику по дням
        const daysOfWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
        const counts = {
          active: Array(7).fill(0),
          completed: Array(7).fill(0),
          overdue: Array(7).fill(0)
        };

        tasks.value.forEach(task => {
          const taskDate = task.deadline_time;
          const dayIndex = taskDate.getDay(); // 0 (Воскресенье) - 6 (Суббота)
          // Преобразуем Sunday to 6, Monday to 0, etc.
          const adjustedDayIndex = (dayIndex + 6) % 7; // 0 - Пн, 6 - Вс

          if (task.status === 1) {
            counts.completed[adjustedDayIndex] += 1;
          } else if (task.status === 2) {
            counts.overdue[adjustedDayIndex] += 1;
          } else if (task.status === 0) {
            counts.active[adjustedDayIndex] += 1;
          }
        });

        return {
          labels: daysOfWeek,
          datasets: [
            {
              label: 'Активные',
              backgroundColor: '#3498db',
              data: counts.active
            },
            {
              label: 'Завершенные',
              backgroundColor: '#2ecc71',
              data: counts.completed
            },
            {
              label: 'Просроченные',
              backgroundColor: '#e74c3c',
              data: counts.overdue
            }
          ]
        };
      }
    };

    const chartOptions = computed(() => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: selectedPeriod.value === 'day' ? 'Статистика за День' : 'Статистика за Неделю'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,       // Интервал между отметками
            precision: 0,      // Убирает десятичные знаки
            // Можно добавить callback для дополнительной настройки
            // callback: function(value) {
            //   if (Number.isInteger(value)) {
            //     return value;
            //   }
            // }
          },
          grid: {
            display: false      // Скрыть сетку по оси Y
          }
        },
        x: {
          grid: {
            display: false      // Скрыть сетку по оси X (если нужно)
          }
        }
      }
    }));

    const chartData = computed(() => {
      const data = getChartData();
      console.log('Chart Data:', data); // Для отладки
      return data;
    });

    onMounted(() => {
      fetchTasks();
    });

    return {
      tasks,
      loading,
      error,
      selectedPeriod,
      chartData,
      chartOptions
    };
  },
};
</script>

<style scoped>
.task-statistics {
  position: absolute;
    top: 100px; /* Указание позиции отдельно */
    left:1320px;
  /* Удалено абсолютное позиционирование */
  border: 1px solid #dddddd; /* Светло-серая граница */
  padding: 16px; /* Увеличен паддинг для внутреннего отступа */
  border-radius: 8px;
  width: 20%; /* Уменьшена ширина */
  max-width: 600px; /* Уменьшен максимальный размер */
  margin: 40px auto; /* Центрирование компонента */
  background-color: #ffffff; /* Светлый фон */
  color: #333333; /* Темно-серый текст */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Легкая тень для глубины */
}

.task-statistics h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333333; /* Темно-серый цвет заголовка */
}

.controls {
  text-align: center;
  margin-bottom: 20px; /* Увеличен отступ */
}

.controls button {
  background-color: #f0f0f0; /* Светло-серый фон кнопок */
  border: 1px solid #cccccc; /* Светло-серая граница */
  color: #333333; /* Темно-серый текст */
  padding: 8px 16px; /* Уменьшен паддинг */
  margin: 0 50px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
  font-size: 14px; /* Уменьшен размер шрифта */
}

.controls button.active, .controls button:hover {
  background-color: #e0e0e0; /* Светло-серый фон при наведении и активном состоянии */
}

.loading-indicator {
  text-align: center;
  font-size: 14px; /* Увеличен размер шрифта для лучшей читаемости */
  color: #666666; /* Светло-серый цвет */
}

.error {
  color: #ff4d4d; /* Красный цвет для ошибок */
  text-align: center;
  margin-top: 16px;
}

.chart-container {
  position: relative;
  height: 400px; /* Установлена подходящая высота для графика */
  width: 100%; /* Ширина 100% контейнера */
}


</style>
