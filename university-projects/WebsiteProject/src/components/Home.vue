<template>
  <div class="container-home container mt-4">
    
    <div class="alert alert-primary text-center">
      <h2>Welcome back, {{ firstName }} {{ lastName ? lastName[0] : '' }}!</h2>
      <div class="mb-3">
        <label for="budgetInput">Set Your Monthly Budget:</label><br />
        <small v-if="errorMessage" class="text-danger d-block mt-1">{{ errorMessage }}</small>
        <input v-model="monthBudget" type="number" class="form-control" id="budgetInput" placeholder="Set Your Budget" @change="saveBudget" min="1">
      </div>

      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card border shadow-sm p-3 bg-light">
            <h5>Monthly Budget</h5>
            <p class="text-success font-weight-bold">${{ monthBudget }}</p>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card border shadow-sm p-3 bg-light">
            <h5>Total Spent</h5>
            <p class="text-danger font-weight-bold">${{ totalSpent }}</p>
          </div>
        </div>
      </div>
      <div class="progress mt-3">
        <div 
          class="progress-bar" 
          :class="remainingBudgetClass"
          role="progressbar" 
          :style="{ width: remainingBudgetPercentage + '%' }">
        </div>
      </div>
      <p class="mt-2 text-center">Remaining Budget: ${{ remainingBudget }}</p>
    </div>
  </div>
  <div class="home-page">
    <ExpenseChartWithFilters />
  </div>
</template>

<script>
import ExpenseChartWithFilters from "./ExpensesChart.vue";
export default {
  data() {
    return {
      firstName: "",
      lastName: "",
      monthBudget: localStorage.getItem("monthlyBudget") || "",
      totalSpent: 0,
      remainingBudget: 0,
      remainingBudgetPercentage: 100,
      remainingBudgetClass: "bg-success",
      errorMessage: ""

    }
  },
  mounted() {
    this.fetchData();
    this.getBudgetData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/retrieve_user.php");
        const data = await response.json();
        this.firstName = data.firstName || "Guest";
        this.lastName = data.lastName || "Guest";
      } 
      catch(error) {
        console.log("Error retrieving data: ", error);
      }
    },
    async getBudgetData() {
      const response = await fetch("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/budget.php");
      const data = await response.json();
      this.totalSpent = data.totalSpent || 0;
      this.calculateBudget();
    },
    saveBudget() {
      if (!this.monthBudget || isNaN(this.monthBudget) || this.monthBudget < 1) {
        this.errorMessage = "Please Input a Valid Number.";
        this.monthBudget = ""; 
        return; 
      }

      this.errorMessage = ""; 
      localStorage.setItem("monthlyBudget", this.monthBudget);
      this.calculateBudget();
    },
    calculateBudget() {
      this.remainingBudget = this.monthBudget - this.totalSpent;
      this.remainingBudgetPercentage = (this.remainingBudget / this.monthBudget) * 100;

      if (this.remainingBudgetPercentage < 25) {
        this.remainingBudgetClass = "bg-danger";
      } else if (this.remainingBudgetPercentage < 50) {
        this.remainingBudgetClass = "bg-warning";
      } else {
        this.remainingBudgetClass = "bg-success";
      }
    }
  },
  components: {
    ExpenseChartWithFilters
  }
};
</script>
<style>
.container-home {
  padding-top: 70px;
}
</style>
