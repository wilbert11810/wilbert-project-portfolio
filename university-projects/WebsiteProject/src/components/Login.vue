<template>
  <div class="container mt-4">
    <div class="card border shadow-sm p-4">
      <h2 class="text-center">Sign In</h2>
      <p class="text-muted text-center">Access your financial dashboard</p>

      
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label>Email</label>
          <input type="email" v-model="email" class="form-control" placeholder="Enter your email">
        </div>
        <div class="mb-3">
          <label>Password</label>
          <input type="password" v-model="password" class="form-control" placeholder="Enter password">
        </div>

        
        <div v-if="isLoading" class="text-center mt-2">
          <div class="spinner-border text-primary" role="status"></div>
          <p>Logging in...</p>
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
          {{ isLoading ? "Logging in..." : "Login" }}
        </button>
      </form>
      <p v-if="errorMessage" class="error"> {{ errorMessage }}</p>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  data() {
    return { 
        email: "", 
        password: "",
        user: null,
        errorMessage: ""
    };
  },
  async mounted() {
  await this.fetchSession();
  },
  methods: {
    async loginUser() {
        if (!this.email || !this.password) { 
            this.errorMessage = "Email or password cannot be empty"; 
            return;
        }
        try {
            const response = await axios.post("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/login.php", {
              email: this.email,
              password: this.password
            }, {
              headers: { "Content-Type": "application/json"}
            });
            console.log("Login response:", response.data);
            if (response.data.user) {
              localStorage.setItem("user", JSON.stringify(response.data.user));
              alert("Logged in successfully!");
              this.$router.push("/cos30043/s104323659/finance-project/");
              this.errorMessage = "";
            } else {
              this.errorMessage = response.data.error;
            }
        } 
        catch (error) {
            console.error("Login failed:", error);
            this.errorMessage = "Login error. Please try again!"
        }
    },
    async fetchSession() {
      try {
        const response = await axios.get("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/session.php");
        if (response.data.user) {
          this.user = response.data.user;
          localStorage.setItem("user", JSON.stringify(this.user)); 
        }      
      }catch (error) {
        console.error("Session error: ", error);
        }

    }
  }
};
</script>
