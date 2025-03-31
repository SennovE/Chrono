<template>
  <div class="catppuccin-background">
    <div class="mocha-container">
      <h1 class="title">Подписка</h1>
      
      <div class="subscription-options">
        <p>Выберите срок подписки:</p>
        <div class="radio-group">
          <label>
            <input type="radio" value="1" v-model="selectedMonths" />
            1 месяц (200₽/мес)
          </label>
          <label>
            <input type="radio" value="6" v-model="selectedMonths" />
            6 месяцев (150₽/мес)
          </label>
          <label>
            <input type="radio" value="12" v-model="selectedMonths" />
            12 месяцев (100₽/мес)
          </label>
        </div>
        <p class="total-cost">Общая стоимость: {{ totalCost }}₽</p>
      </div>
      
      <button class="buy-button" @click="togglePaymentOptions">
        Купить подписку
      </button>
      
      <transition name="fade">
        <div v-if="showPaymentOptions" class="payment-options">
          <h2 class="subtitle">Выберите способ оплаты</h2>
          <button class="payment-option" @click="payWithCrypto">
            Оплатить криптовалютой
          </button>
        </div>
      </transition>
      
      <!-- Вывод сообщения об ошибке с подробностями -->
      <div v-if="errorMessage" class="error-message">
        <p>Ошибка: {{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const getToken = () => {
  const token = localStorage.getItem("chronoJWTToken");
  if (!token) {
    throw new Error("Token is missing. Please log in.");
  }
  return token;
};

export default {
  name: "CatppuccinSubscription",
  data() {
    return {
      selectedMonths: "1",
      showPaymentOptions: false,
      errorMessage: "" // для хранения сообщения об ошибке
    };
  },
  computed: {
    totalCost() {
      const months = parseInt(this.selectedMonths);
      let costPerMonth = 200;
      if (months === 6) {
        costPerMonth = 150;
      } else if (months === 12) {
        costPerMonth = 100;
      }
      return months * costPerMonth;
    },
  },
  methods: {
    togglePaymentOptions() {
      this.errorMessage = ""; // сбрасываем ошибку при повторном выборе
      this.showPaymentOptions = !this.showPaymentOptions;
    },
    async payWithCrypto() {
      try {
        this.errorMessage = "";
        const token = getToken();
        const response = await axios.post(
          `http://${process.env.VUE_APP_BACKEND_URL}:8080/api/v1/payment/invoice/create`,
          {
            shop_id: "oMAMXR7C4iMjbEC0",  
            amount: this.totalCost,
            currency: "RUB"
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        if (response.data && response.data.pay_url) {
          window.location.href = response.data.pay_url;
        } else {
          this.errorMessage = "Ссылка для оплаты не получена.";
        }
      } catch (error) {
        console.error("Ошибка оплаты:", error);
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || error.response.data.message || "Неизвестная ошибка";
        } else if (error.message) {
          this.errorMessage = error.message;
        } else {
          this.errorMessage = "Ошибка оплаты, попробуйте снова";
        }
      }
    },
  },
};
</script>

<style scoped>
.catppuccin-background {
  background-color: #1e1e2e;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.mocha-container {
  max-width: 500px;
  padding: 30px;
  background: #313244;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  color: #cdd6f4;
  font-family: 'Inter', sans-serif;
  text-align: center;
}

.title {
  font-size: 2em;
  margin-bottom: 20px;
  color: #cad3f5;
}

.subscription-options {
  margin-bottom: 20px;
}

.radio-group {
  display: flex;
  justify-content: space-around;
  margin: 10px 0;
}

.radio-group label {
  cursor: pointer;
  font-size: 1em;
}

.radio-group input[type="radio"] {
  margin-right: 5px;
}

.total-cost {
  font-size: 1.2em;
  margin-top: 10px;
}

.buy-button {
  width: 100%;
  padding: 15px;
  background-color: #45475a;
  border: none;
  border-radius: 8px;
  font-size: 1.2em;
  color: #cdd6f4;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}

.buy-button:hover {
  background-color: #565e7e;
}

.payment-options {
  margin-top: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.subtitle {
  font-size: 1.5em;
  margin-bottom: 15px;
  color: #cad3f5;
}

.payment-option {
  width: 100%;
  padding: 12px;
  background-color: #45475a;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  color: #cdd6f4;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.payment-option:hover {
  background-color: #565e7e;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.error-message {
  margin-top: 20px;
  color: #f38ba8; /* яркий акцент для ошибки */
  font-weight: bold;
  font-size: 1.1em;
}
</style>
