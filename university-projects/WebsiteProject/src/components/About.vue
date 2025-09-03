<template>
  <div class="container mt-4">
    <div class="card border shadow-sm p-4 text-center">
      <h2>About Our Finance Management App</h2>
      <p class="text-muted">
        Welcome to Finance Management, a smart tool designed to help you track your expenses, 
        set budgets, and make informed financial decisions with ease.
      </p>
    </div>

    <div class="card p-3 text-center mt-4">
      <h3>Personalized Greeting</h3>
      <div class="mb-3">
        <input v-model="firstName" type="text" class="form-control" placeholder="Enter your first name">
      </div>
      <div class="mb-3">
        <input v-model="lastName" type="text" class="form-control" placeholder="Enter your last name">
      </div>
      <h4 v-if="firstName && lastName">Hello, {{ firstName }} {{ lastName }}! Welcome to our platform.</h4>
    </div>


    <div class="card p-3 text-center mt-4">
      <h3>Choose Your Favorite Scene</h3>
      <div>
        <label>
          <input type="radio" v-model="selectedImage" value="mountain"> Mountain
        </label>
        <label>
          <input type="radio" v-model="selectedImage" value="ocean"> Ocean
        </label>
      </div>

      <div class="mt-3">
        <img v-if="selectedImage === 'mountain'" src="/mountain.jpg" alt="Mountain"> 
        <img v-if="selectedImage === 'ocean'" src="/ocean.jpg" alt="Mountain"> 
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: "",
      lastName: "",
      selectedImage: ""
    };
  }
};
</script>

<style scoped>
.selected-image {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 10px;
  margin-top: 15px;
}
</style>
