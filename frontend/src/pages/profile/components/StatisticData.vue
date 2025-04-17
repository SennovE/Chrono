<template>
  <div class="get-task-statistics">
    <h2>Статистика задач</h2>
    
    <div class="task-stats-period-selector">
      <button 
        :class="{ active1: taskStatsSelectedPeriod === 'day' }" 
        @click="taskStatsSelectedPeriod = 'day'"
      >
        День
      </button>
      <button 
        :class="{ active1: taskStatsSelectedPeriod === 'week' }" 
        @click="taskStatsSelectedPeriod = 'week'"
      >
        Неделя
      </button>
      <button 
        :class="{ active1: taskStatsSelectedPeriod === 'calendar' }" 
        @click="taskStatsSelectedPeriod = 'calendar'"
      >
        Календарь
      </button>
    </div>

    <div v-if="taskStatsSelectedPeriod === 'calendar'" class="year-select">
      <label>
        Выберите год:
        <select v-model="selectedYear">
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </label>
    </div>
    
    <div v-if="loading" class="loading-indicator">
      Загрузка статистики...
    </div>
    
    <div v-else>
      <div v-if="taskStatsSelectedPeriod === 'day' || taskStatsSelectedPeriod === 'week'" class="chart-container">
  <BarChart :key="taskStatsSelectedPeriod" :chartData="chartData" :options="chartOptions" :chartType="chartType" />
</div>
      
      <div v-else class="calendar-all-months">
        <div v-for="month in calendarByMonth" :key="month.month" class="month-container">
          <h3>{{ month.monthName }}</h3>
          <div class="calendar-grid">
            <div class="week" v-for="(week, weekIndex) in month.weeks" :key="weekIndex">
              <div 
                v-for="(day, dayIndex) in week" 
                :key="dayIndex"
                class="day"
                @click="day && openDayModal(day)"
                :style="day ? { backgroundColor: getDayColor(day.total, maxCalendarCount) } : {}"
              >
                <span v-if="day">{{ day.date.getDate() }}</span>
                <!-- Tooltip в стиле Mocha -->
                <div v-if="day" class="tooltip">
                  {{ formatDate(day.date) }}<br>
                  Запланировано: {{ day.planned }}<br>
                  Сделано: {{ day.done }}<br>
                  Пропущено: {{ day.missed }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
    </div>
    
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>Задачи на {{ formatDate(selectedDay.date) }}</h3>
        <ul>
          <li v-for="task in dayTasks" :key="task.id" :style="getTaskColor(task)">
            <strong>{{ task.title || 'Задача' }}</strong><br>
            Время: {{ formatTime(task.deadline_time) }}<br>
            Описание: {{ task.description || 'Нет описания' }}
          </li>
        </ul>
        <button @click="closeModal">Закрыть</button>
      </div>
    </div>
    
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import BarChart from './BarChart.vue';
import { useRouter } from "vue-router";

export default {
  name: 'TaskStatistics',
  components: { BarChart },
  setup() {
    const router = useRouter();
    const tasks = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const taskStatsSelectedPeriod = ref('calendar');
    const selectedYear = ref(new Date().getFullYear());
    const availableYears = computed(() => {
      const current = new Date().getFullYear();
      const years = [];
      for (let i = current - 2; i <= current + 3; i++) {
        years.push(i);
      }
      return years;
    });

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
          { headers: { Authorization: `Bearer ${token}` } }
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

    function redirectToLogin() {
      router.push({ name: "Login Page" });
    }
    const chartType = computed(() => 'bar');

    const chartData = computed(() => {
      const now = new Date();
      if (taskStatsSelectedPeriod.value === 'day') {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const tomorrow = new Date(today);
        tomorrow.setDate(today.getDate() + 1);
        const todaysTasks = tasks.value.filter(task => task.deadline_time >= today && task.deadline_time < tomorrow);
        const activeCount = todaysTasks.filter(task => task.status === 0 && task.deadline_time >= now).length;
        const completedCount = todaysTasks.filter(task => task.status === 1).length;
        const overdueCount = todaysTasks.filter(task => (task.status === 0 && task.deadline_time < now) || task.status === 2).length;
        
        return {
          labels: [today.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' })],
          datasets: [
            { label: 'Надо сделать', backgroundColor: '#89b4fa', data: [activeCount] },
            { label: 'Сделано', backgroundColor: '#a6e3a1', data: [completedCount] },
            { label: 'Пропущено', backgroundColor: '#fab387', data: [overdueCount] }
          ]
        };
      } else if (taskStatsSelectedPeriod.value === 'week') {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const labels = [];
        const activeCounts = [];
        const completedCounts = [];
        const overdueCounts = [];
        // 7 дней: от -3 до +3
        for (let offset = -3; offset <= 3; offset++) {
          const day = new Date(today);
          day.setDate(today.getDate() + offset);
          const dayStart = new Date(day);
          dayStart.setHours(0, 0, 0, 0);
          const dayEnd = new Date(dayStart);
          dayEnd.setDate(dayStart.getDate() + 1);
          const label = day.toLocaleDateString('ru-RU', { weekday: 'short', day: '2-digit', month: '2-digit' });
          labels.push(label);
          
          const dayTasks = tasks.value.filter(task => task.deadline_time >= dayStart && task.deadline_time < dayEnd);
          const active = dayTasks.filter(task => task.status === 0 && task.deadline_time >= now).length;
          const completed = dayTasks.filter(task => task.status === 1).length;
          const overdue = dayTasks.filter(task => (task.status === 0 && task.deadline_time < now) || task.status === 2).length;
          
          activeCounts.push(active);
          completedCounts.push(completed);
          overdueCounts.push(overdue);
        }
        return {
          labels,
          datasets: [
            { label: 'Надо сделать', backgroundColor: '#89b4fa', data: activeCounts },
            { label: 'Сделано', backgroundColor: '#a6e3a1', data: completedCounts },
            { label: 'Пропущено', backgroundColor: '#fab387', data: overdueCounts }
          ]
        };
      } else {
        return {};
      }
    });

    const chartOptions = computed(() => {
      const titleText = taskStatsSelectedPeriod.value === 'day' ? 'Статистика за День' : 'Статистика за Неделю';
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: "#cdd6f4" } },
          title: { display: true, text: titleText, color: "#89b4fa" },
          tooltip: { 
            mode: 'index', 
            intersect: false, 
            callbacks: { label: context => context.dataset.label + ': ' + context.parsed.y.toFixed(0) } 
          }
        },
        scales: {
          x: { stacked: true, ticks: { color: "#cdd6f4" }, grid: { display: false } },
          y: { 
            stacked: true, 
            beginAtZero: true, 
            ticks: { stepSize: -0.1111, callback: value => Number.isInteger(value) ? value : '', color: "#cdd6f4" },
            grid: { display: false } 
          }
        }
      };
    });

    const tasksByDate = computed(() => {
      const map = {};
      const now = new Date();
      tasks.value.forEach(task => {
        const dateObj = task.deadline_time;
        if (dateObj.getFullYear() === selectedYear.value) {
          const dateStr = dateObj.toISOString().slice(0,10);
          if (!map[dateStr]) {
            map[dateStr] = { planned: 0, done: 0, missed: 0 };
          }
          if (task.status === 1) {
            map[dateStr].done += 1;
          } else if (task.status === 0) {
            if (dateObj >= now) {
              map[dateStr].planned += 1;
            } else {
              map[dateStr].missed += 1;
            }
          } else if (task.status === 2) {
            map[dateStr].missed += 1;
          }
        }
      });
      return map;
    });

    const maxCalendarCount = computed(() => {
      let max = 0;
      for (const key in tasksByDate.value) {
        const total = tasksByDate.value[key].planned + tasksByDate.value[key].done + tasksByDate.value[key].missed;
        if (total > max) max = total;
      }
      return max;
    });

    const calendarByMonth = computed(() => {
      const months = [];
      for (let month = 0; month < 12; month++) {
        const firstDay = new Date(selectedYear.value, month, 1);
        const lastDay = new Date(selectedYear.value, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const weeks = [];
        let week = [];
        const startDayIndex = firstDay.getDay();
        for (let i = 0; i < startDayIndex; i++) {
          week.push(null);
        }
        for (let day = 1; day <= daysInMonth; day++) {
          const dateObj = new Date(selectedYear.value, month, day);
          const dateStr = dateObj.toISOString().slice(0,10);
          const counts = tasksByDate.value[dateStr] || { planned: 0, done: 0, missed: 0 };
          week.push({
            date: dateObj,
            planned: counts.planned,
            done: counts.done,
            missed: counts.missed,
            total: (counts.planned || 0) + (counts.done || 0) + (counts.missed || 0)
          });
          if (week.length === 7) {
            weeks.push(week);
            week = [];
          }
        }
        if (week.length > 0) {
          while (week.length < 7) week.push(null);
          weeks.push(week);
        }
        months.push({
          month,
          monthName: new Date(selectedYear.value, month, 1).toLocaleString('ru-RU', { month: 'long' }),
          weeks
        });
      }
      return months;
    });

    const showModal = ref(false);
    const selectedDay = ref(null);
    const openDayModal = (day) => {
      selectedDay.value = day;
      showModal.value = true;
    };
    const closeModal = () => {
      showModal.value = false;
    };
    const dayTasks = computed(() => {
      if (!selectedDay.value) return [];
      const dayStr = selectedDay.value.date.toISOString().slice(0,10);
      return tasks.value.filter(task => task.deadline_time.toISOString().slice(0,10) === dayStr);
    });
    const formatDate = date => date.toISOString().slice(0,10);
    const formatTime = date => {
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`;
    };
    const getTaskColor = (task) => {
      if (task.status === 1) {
        return { color: 'green' };
      } else if (task.status === 0) {
        if (task.deadline_time >= new Date()) {
          return { color: 'green' };
        } else {
          return { color: 'orange' };
        }
      } else if (task.status === 2) {
        return { color: 'orange' };
      }
      return {};
    };
    const getDayColor = (count, maxCountValue) => {
      if (count === 0) return "#ebedf0";
      const ratio = count / maxCountValue;
      const lightness = 90 - ratio * 60;
      return `hsl(120, 50%, ${lightness}%)`;
    };
    onMounted(() => {
      fetchTasks();
    });
    return {
      tasks,
      loading,
      error,
      taskStatsSelectedPeriod,
      selectedYear,
      availableYears,
      chartType,
      chartData,
      chartOptions,
      calendarByMonth,
      maxCalendarCount,
      formatDate,
      getDayColor,
      showModal,
      selectedDay,
      openDayModal,
      closeModal,
      dayTasks,
      formatTime,
      getTaskColor
    };
  },
};
</script>

<style scoped>
.get-task-statistics {
  background: none;
  padding: 20px;
  border-radius: 10px;
  width: 90%;
  max-width: 700px;
  height: 770px;
  color: #cdd6f4;
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  padding-left: 60%;
}

.task-stats-period-selector {
  text-align: center;
  margin-bottom: 20px;
}

.year-select {
  text-align: center;
  margin-bottom: 10px;
  color: #cdd6f4;
}

.year-select select {
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid #302d41;
  background-color: #2e2e42;
  color: #cdd6f4;
  font-size: 14px;
}

.task-stats-period-selector button {
  background-color: #2e2e42;
  border: 1px solid #302d41;
  color: #cdd6f4;
  padding: 10px 20px;
  margin: 0 5px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
}

.task-stats-period-selector button:hover {
  background-color: #3a3a55;
}

.task-stats-period-selector button.active1 {
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
  height: 10px;
  width: 80%;
  margin: 20px 0;
}


.calendar-all-months {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 10px;
}

.month-container {
  border: 1px solid #302d41;
  padding: 5px;
  border-radius: 5px;
  min-width: 140px;
}

.calendar-grid {
  display: flex;
  flex-direction: column;
}

.week {
  display: flex;
}

.day {
  position: relative;
  width: 18px;
  height: 18px;
  margin: 1px;
  border: 1px solid #ccc;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  cursor: pointer;
}


.day .tooltip {
  position: absolute;
  bottom: 120%;
  left: 50%;
  transform: translateX(-50%);
  background: #3e2723;
  color: #f5f5f5;
  padding: 4px 6px;
  border-radius: 4px;
  font-size: 10px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s;
  z-index: 10;
}

.day:hover .tooltip {
  opacity: 1;
  visibility: visible;
}


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right:0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: #1e1e2e;
  padding: 20px;
  border-radius: 10px;
  color: #cdd6f4;
  max-width: 400px;
  width: 90%;
}
.modal-content button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  background-color: #89b4fa;
  color: #1e1e2e;
  cursor: pointer;
}
</style>
