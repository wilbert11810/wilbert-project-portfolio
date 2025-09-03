<template>
  <div class="expense-chart-container">
    <h2>Expense Overview</h2>
    <div class="filter-controls">
      <label>
        Filter by Category:
        <select v-model="selectedCategory" @change="fetchData">
          <option value="">All Categories</option>
          <option value="food">Food</option>
          <option value="bills">Bills</option>
          <option value="entertainment">Entertainment</option>
          <option value="others">Others</option>
        </select>
      </label>
      <label>
        Filter by Month:
        <select v-model="selectedMonth" @change="fetchData">
          <option value="">All Months</option>
          <option
            v-for="month in availableMonths"
            :value="month"
            :key="month"
          >
            {{ formatMonth(month) }}
          </option>
        </select>
      </label>
    </div>
    <div class="chart-wrapper">
      <canvas ref="chartCanvas" width="600" height="400"></canvas>
    </div>
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default {
  name: "ExpenseChartWithFilters",
  data() {
    return {
      selectedCategory: "",
      selectedMonth: "",
      availableMonths: [],
      chartInstance: null,
      expensesData: {},
      errorMessage: ""
    };
  },
  mounted() {
    this.fetchData();
  },
  beforeUnmount() {
    this.destroyChart();
  },
  methods: {
    async fetchData() {
      this.errorMessage = "";
      try {
        let url =
          "https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/get_visualization_transactions.php";
        const params = new URLSearchParams();
        if (this.selectedMonth) params.append("month", this.selectedMonth);
        if (this.selectedCategory) params.append("category", this.selectedCategory);
        if (params.toString()) {
          url = `${url}?${params.toString()}`;
        }
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.expensesData =
          data.visualizationData &&
          Object.keys(data.visualizationData).length > 0
            ? data.visualizationData
            : {};
        this.updateAvailableMonths(data);
        this.renderChart();
      } catch (error) {
        console.error("Error fetching expense data:", error);
        this.errorMessage =
          "Failed to load expense data. Please try again later.";
        this.expensesData = {};
        this.renderChart(); // Render empty state
      }
    },
    updateAvailableMonths(responseData) {
      if (responseData && responseData.transactions && Array.isArray(responseData.transactions)) {
        const monthsSet = new Set();
        responseData.transactions.forEach(transaction => {
          if (transaction.date) {
            monthsSet.add(this.getExpenseMonth(transaction.date));
          }
        });
        this.availableMonths = Array.from(monthsSet).sort().reverse();
      } else {
        const currentDate = new Date();
        const dummyMonths = [];
        for (let i = 0; i < 6; i++) {
          const d = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1);
          const monthStr = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
          dummyMonths.push(monthStr);
        }
        this.availableMonths = dummyMonths;
      }
    },
    getExpenseMonth(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;
    },
    formatMonth(monthString) {
      const [year, month] = monthString.split("-");
      const date = new Date(year, month - 1);
      return date.toLocaleString("default", { month: "long", year: "numeric" });
    },
    renderChart() {
      this.$nextTick(() => {
        const canvas = this.$refs.chartCanvas;
        if (!canvas) {
          console.error("Chart canvas not available.");
          return;
        }
        const ctx = this.$refs.chartCanvas.getContext("2d");
        if (this.chartInstance) {
          this.chartInstance.destroy();
        }
        
        if (!this.expensesData || Object.keys(this.expensesData).length === 0) {
          this.renderEmptyState(ctx);
          return;
        }
        
        const categories = ["food", "bills", "entertainment", "others"];
        const categoryLabels = ["Food", "Bills", "Entertainment", "Others"];
        
        const chartData = categories.map(
          category => Number(this.expensesData[category]) || 0
        );
        this.chartInstance = new Chart(ctx, {
          type: "bar",
          data: {
            labels: categoryLabels,
            datasets: [
              {
                label: "Total Expenses ($)",
                data: chartData,
                backgroundColor: [
                  "rgba(255, 99, 132, 0.7)",
                  "rgba(54, 162, 235, 0.7)",
                  "rgba(255, 206, 86, 0.7)",
                  "rgba(75, 192, 192, 0.7)"
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(75, 192, 192, 1)"
                ],
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: "Amount ($)"
                }
              }
            },
            plugins: {
              tooltip: {
                callbacks: {
                  label: function (context) {
                    return `$${context.raw.toFixed(2)}`;
                  }
                }
              }
            }
          }
        });
      });
    },
    renderEmptyState(ctx) {
      ctx.clearRect(
        0,
        0,
        this.$refs.chartCanvas.width,
        this.$refs.chartCanvas.height
      );
      ctx.font = "16px Arial";
      ctx.fillStyle = "#999";
      ctx.textAlign = "center";
      ctx.fillText(
        "No expense data available",
        this.$refs.chartCanvas.width / 2,
        this.$refs.chartCanvas.height / 2
      );
    },
    destroyChart() {
      if (this.chartInstance) {
        this.chartInstance.destroy();
        this.chartInstance = null;
      }
    }
  }
};
</script>

<style scoped>
.expense-chart-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}

.filter-controls {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

label {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-weight: 500;
}

select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
  min-width: 200px;
}

.chart-wrapper {
  position: relative;
  height: 400px;
  width: 100%;
  margin-top: 20px;
}

.error-message {
  color: #d32f2f;
  background-color: #fde8e8;
  padding: 10px;
  border-radius: 4px;
  margin-top: 20px;
  text-align: center;
}

@media (max-width: 600px) {
  .filter-controls {
    flex-direction: column;
    gap: 10px;
  }
  select {
    width: 100%;
  }
}
</style>
