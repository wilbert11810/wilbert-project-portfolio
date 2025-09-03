<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top shadow-sm">
    <h2 class="company-name">Finance Management</h2>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="ms-auto">
        <li class="nav-item"><router-link to="/cos30043/s104323659/finance-project/">Home</router-link></li>
        <li class="nav-item"><router-link to="/cos30043/s104323659/finance-project/expenses">Expenses</router-link></li>
        <li class="nav-item"><router-link to="/cos30043/s104323659/finance-project/about">About</router-link></li>
        <li class="nav-item"><router-link to="/cos30043/s104323659/finance-project/news">News</router-link></li>

        <router-link v-if="!user" to="/cos30043/s104323659/finance-project/signin">Sign In</router-link>
        <router-link v-if="!user" to="/cos30043/s104323659/finance-project/signup">Sign Up</router-link>
        

        <button v-if="user" @click="logout">Logout</button>
      </ul>
    </div>
    </nav>

    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import { getCurrentUser, logoutUser } from "./utils/auth.js";

export default { 
  data() {
    return {
      user: null
    };
  },
  async mounted() {
    this.refreshUser();
  },
  methods: {
    async logout() {
      await logoutUser();
      this.user = null;
    },
    async refreshUser() {
      this.user = await getCurrentUser();
    }
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #007bff;
  padding: 10px 0;
  justify-content: space-between;
  align-items: center;
  z-index: 1000;
}
.company-name {
  margin-left: 20px;
}

.navbar ul {
  list-style: none;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
}

.navbar a {
  text-decoration: none;
  font-weight: bold;
  color: white;
  font-size: 18px;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background 0.3s;
  margin-right: 10px;
}

.navbar a:hover {
  background: rgba(255, 255, 255, 0.2);
}

.main-content {
  max-width: 1200px;
  margin: auto;
  padding: 20px;
  min-height: 80vh;
}
</style>
