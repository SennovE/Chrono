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
      
      <div v-else>
        <BarChart :chartData="chartData" :options="chartOptions" />
      </div>
      
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </template>
<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { Bar } from 'vue-chartjs';
import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  Title, 
  Tooltip, 
  Legend 
} from 'chart.js';

// Регистрация компонентов Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// Создание компонента графика
const BarChart = {
  extends: Bar,
  props: ['chartData', 'options'],
};

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
        overdue: 0
      };


      tasks.value.forEach(task => {
        // Определяем статус задачи
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
      } else if (selectedPeriod.value === 'week') {
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
      }
    }));

    const chartData = computed(() => getChartData());

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
  border: 1px solid #121111;
  padding: 16px;
  border-radius: 8px;
  width: 100%;
  max-width: 800px;
  margin: 40px auto;
  background-color: #131212;
  color: #f1f1f1;
  position: absolute;
    top: 400px; /* Указание позиции отдельно */
    left: 600px;
}

.task-statistics h2 {
  text-align: center;
  margin-bottom: 20px;
}

.controls {
  text-align: center;
  margin-bottom: 20px;
}

.controls button {
  background-color: #434547;
  border: none;
  color: white;
  padding: 10px 20px;
  margin: 0 5px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.controls button.active, .controls button:hover {
  background-color: #3b3d3e;
}

.loading-indicator {
  text-align: center;
  font-size: 18px;
  color: #555;
}

.error {
  color: red;
  text-align: center;
  margin-top: 16px;
}
</style>
  