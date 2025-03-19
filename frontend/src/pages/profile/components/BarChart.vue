<template>
  <Bar :chartData="chartData" :options="chartOptions" />
</template>
  
<script>
import { defineComponent } from 'vue';
import { Bar } from 'vue-chartjs';
import { 
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js';
  
export default defineComponent({
  name: 'BarChart',
  components: {
    Bar
  },
});
  
ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, BarElement);
</script>
  
<style scoped>
</style>
