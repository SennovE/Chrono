<template>
  <div>
    <h1>Список дедлайнов</h1>
    <table class="styled-table">
      <!-- Заголовки таблицы -->
      <thead>
        <tr>
          <th>ID</th>
          <th>Author</th>
          <th>Author ID</th>
          <th>Deadline Time</th>
          <th>Description</th>
          <th>Status</th>
        </tr>
      </thead>
      <!-- Тело таблицы -->
      <tbody>
        <tr v-for="task in deadline_tasks" :key="task.deadline_time">
          <td>{{ task.deadline_time }}</td>
          <td>{{ task.description }}</td>
          <td>{{ task.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
data() {
    return {
        deadline_tasks: []
    }
},
methods: {
    async get_tasks() {
        const response = await axios.get('http://localhost:8080/api/v1/deadline_task/get_tasks/');
        this.deadline_tasks = response.data;
    }
},
mounted() {
    // Загружаем пользователей при монтировании компонента
    this.get_tasks();
  },

name: 'DeadlineTaskDebugComponent'  
};

</script>

<style>
.deadline-container {
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.no-deadlines {
  text-align: center;
  font-size: 18px;
  color: #888;
}

.day-block {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
}

.day-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.tasks {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.task p {
  margin: 0;
  font-size: 14px;
  color: #555;
}
</style>
