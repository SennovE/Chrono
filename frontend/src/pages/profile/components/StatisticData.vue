<template>
  <div class="get-task-statistics">
    <h2>Статистика задач</h2>
    
    <div class="choose-day-weak">
      <button 
        :class="{ active1: selectedPeriod === 'day' }" 
        @click="selectedPeriod = 'day'"
      >
        День
      </button>
      <button 
        :class="{ active1: selectedPeriod === 'week' }" 
        @click="selectedPeriod = 'week'"
      >
        Даты
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
import BarChart from './BarChart.vue';
import { useRouter } from "vue-router";

export default {
  name: 'TaskStatistics',
  components: {
    BarChart
  },
  setup() {
    const router = useRouter();
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
        if (!token) {
          redirectToLogin();
          return;
        }
        const response = await axios.get(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/deadline_task/get_tasks/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
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

    // Формирование данных для графика с обработкой просроченных дедлайнов
    const getChartData = () => {
      const now = new Date();
      if (selectedPeriod.value === 'day') {
        // Фильтруем задачи только на сегодняшний день
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const tomorrow = new Date(today);
        tomorrow.setDate(today.getDate() + 1);
        const todaysTasks = tasks.value.filter(task => task.deadline_time >= today && task.deadline_time < tomorrow);
  
        const counts = { active1: 0, completed: 0, overdue: 0 };
        todaysTasks.forEach(task => {
          if (task.status === 1) {
            counts.completed++;
          } else if (task.status === 0) {
            // Если дедлайн уже прошёл, считаем задачу просроченной
            if (task.deadline_time < now) {
              counts.overdue++;
            } else {
              counts.active1++;
            }
          } else if (task.status === 2) {
            counts.overdue++;
          }
        });
        return {
          labels: ['Активные', 'Завершенные', 'Просроченные'],
          datasets: [{
            label: 'Количество задач',
            backgroundColor: ['#89b4fa', '#a6e3a1', '#fab387'],
            data: [counts.active1, counts.completed, counts.overdue]
          }]
        };
      } else {
        // Группировка по датам (начало дня)
        const groups = {};
        tasks.value.forEach(task => {
          const d = new Date(task.deadline_time);
          d.setHours(0, 0, 0, 0);
          const timeKey = d.getTime();
          if (!groups[timeKey]) {
            groups[timeKey] = { active1: 0, completed: 0, overdue: 0, date: new Date(timeKey) };
          }
          if (task.status === 1) {
            groups[timeKey].completed++;
          } else if (task.status === 0) {
            if (task.deadline_time < now) {
              groups[timeKey].overdue++;
            } else {
              groups[timeKey].active1++;
            }
          } else if (task.status === 2) {
            groups[timeKey].overdue++;
          }
        });
        const sortedKeys = Object.keys(groups).sort((a, b) => a - b);
        const labels = sortedKeys.map(key => {
          const dateObj = groups[key].date;
          return dateObj.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' });
        });
        return {
          labels: labels,
          datasets: [
            {
              label: 'Активные',
              backgroundColor: '#89b4fa',
              data: sortedKeys.map(key => groups[key].active1)
            },
            {
              label: 'Завершенные',
              backgroundColor: '#a6e3a1',
              data: sortedKeys.map(key => groups[key].completed)
            },
            {
              label: 'Просроченные',
              backgroundColor: '#fab387',
              data: sortedKeys.map(key => groups[key].overdue)
            }
          ]
        };
      }
    };

    // Вычисление максимального значения из данных для оси Y
    const chartOptions = computed(() => {
      let maxValue = 0;
      if (chartData.value && chartData.value.datasets) {
        chartData.value.datasets.forEach(dataset => {
          dataset.data.forEach(val => {
            if (val > maxValue) {
              maxValue = val;
            }
          });
        });
      }
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: "#cdd6f4"
            }
          },
          title: {
            display: true,
            text: selectedPeriod.value === 'day' ? 'Статистика за День' : 'Статистика по датам',
            color: "#89b4fa"
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1,
              min: 0,
              callback: function(value) {
                return Number.isInteger(value) ? value : '';
              },
              color: "#cdd6f4"
            },
            grid: {
              color: "#302d41"
            },
            suggestedMax: maxValue + 1,
          },
          x: {
            ticks: {
              color: "#cdd6f4"
            },
            grid: {
              display: false
            }
          }
        }
      };
    });

    const chartData = computed(() => {
      const data = getChartData();
      console.log('Chart Data:', data);
      return data;
    });

    function redirectToLogin() {
      router.push({ name: "Login Page" });
    }

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
.get-task-statistics {
  position: absolute;
  top: 100px;
  left: 75%;
  transform: translateX(-50%);
  background-color: #1e1e2e; /* Фон Mocha */
  border: 1px solid #302d41;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  max-width: 700px; /* Уменьшенная ширина панели */
  min-height: 850px;
  color: #cdd6f4;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}


/* Если экран ещё уже – меняем позиционирование, чтобы не перекрывать другие элементы */
@media (max-width: 600px) {
  .get-task-statistics {
    position: relative; /* Относительное позиционирование вместо абсолютного */
    top: -850px; /* Отступ сверху можно настроить отдельно */
    left: 90px;
    transform: none;
    max-width: 100%;
    width: 45%;
    margin: 20px auto;
    min-height: 40px;
  }
}


.choose-day-weak {
  text-align: center;
  margin-bottom: 20px;
}

.choose-day-weak button {
  background-color: #2e2e42;
  border: 1px solid #302d41;
  color: #cdd6f4;
  padding: 10px 20px;
  margin: 0 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s, box-shadow 0.3s;
}

.choose-day-weak button:hover {
  background-color: #3a3a55;
}

.choose-day-weak button.active1 {
  background-color: #89b4fa;
  color: #1e1e2e;
  border-color: #89b4fa;
}

.loading-indicator {
  text-align: center;
  font-size: 16px;
  color: #a6adc8;
  margin-top: 20px;
}

.error {
  color: #fab387;
  text-align: center;
  margin-top: 20px;
  font-size: 16px;
}

.chart-container {
  position: relative;
  height: 140px; /* Уменьшенная высота графика */
  width: 100%;
  margin: 20px 0;
}
</style>
