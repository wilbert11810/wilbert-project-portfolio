<template>
  <div class="container mt-4">
    <div class="card border shadow-sm p-4">
      <h2 class="text-center">Create an Account</h2>
      <p class="text-muted text-center">Join us to track your finances easily</p>

      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <label>First Name</label>
          <input v-model="firstName" type="text" class="form-control" placeholder="Enter your first name" required>
        </div>
        <div class="mb-3">
          <label>Last Name</label>
          <input v-model="lastName" type="text" class="form-control" placeholder="Enter your last name" required>
        </div>
        <div class="mb-3">
          <label>Email</label>
          <input v-model="email" type="email" class="form-control" placeholder="Enter your email" required>
          <small v-if="emailError" class="text-danger">{{ emailError }}</small>
        </div>
        <div class="mb-3">
          <label>Password</label>
          <input v-model="password" type="password" class="form-control" placeholder="Enter a strong password" required>
          <small v-if="passwordError" class="text-danger">{{ passwordError }}</small>
        </div>
        <div class="mb-3">
          <label>Confirm Password</label>
          <input v-model="confirmPassword" type="password" class="form-control" placeholder="Confirm your password" required>
          <small v-if="passwordMismatch" class="text-danger">Passwords do not match!</small>
        </div>

        <div v-if="isLoading" class="text-center mt-2">
          <div class="spinner-border text-primary" role="status"></div>
          <p>Creating account...</p>
        </div>

        <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
          {{ isLoading ? "Signing Up..." : "Sign Up" }}
        </button>

        <p class="mt-3 text-center">
          Already have an account?<router-link to="/signin">Sign In</router-link>
        </p>
      </form>
    </div>
  </div>
</template> 

<script>
import axios from "axios";

export default {
    data() {
        return {
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            confirmPassword: "",
            emailError: "",
            passwordError: "",
            isLoading: false
        };
    },
    methods: {
        async registerUser() {
            this.emailError = "";
            this.passwordError = "";
            
            if (!this.email.includes("@")) {
                this.emailError = "Please enter a valid email.";
                return;
            }
            
            if (this.password.length < 8 || !/[A-Z]/.test(this.password) || !/[0-9]/.test(this.password)) {
                this.passwordError = "Password must have at least 8 characters, an uppercase letter, and a number.";
                return;
            }

            if (this.password !== this.confirmPassword) {
                this.passwordError = "Passwords do not match!";
                return;
            }
            this.isLoading = true;
            try {
                const response = await axios.post("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/register.php", {
                    first_name: this.firstName,
                    last_name: this.lastName,
                    email: this.email,
                    password: this.password
                });
                console.log("Server Response:", response.data);
                alert(response.data.message || "Registration failed!");
                if (response.data.success) {
                  this.$router.push("/signin")
                  
                }
            } 
            catch (error) {
              console.error("Register error:", error);
            }
            this.isLoading = false;
        }
    },
    computed: {
        passwordMismatch() {
            return this.confirmPassword && this.confirmPassword != this.password;
        }
    }

};
</script>
