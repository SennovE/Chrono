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
  
ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

export default defineComponent({
  name: 'BarChart',
  components: {
    Bar
  },
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      required: true
    }
  },
});
</script>
  
<style scoped>
</style>
