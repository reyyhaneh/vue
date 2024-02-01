<template>
    <div class="login-container">
      <div class="login-form">
        <h2>Login</h2>
        <form @submit.prevent="login">
          <label for="username">Username:</label>
          <input v-model="form.username" name="username" type="text" required />
  
          <label for="password">Password:</label>
          <input v-model="form.password" name="password" type="password" required />
  
          <button type="submit">Log In</button>
        </form>
        <router-link to="/" class="signup-link">Don't have an account? Sign Up</router-link>
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      // Simulated login request
      // In a real-world scenario, you would make an HTTP request to your backend for authentication
      // For now, we'll simulate a successful login and receive a JWT token
      const simulatedToken = 'your_simulated_jwt_token';

      // Store the token in localStorage (or use a more secure storage mechanism depending on your app's requirements)
      localStorage.setItem('jwtToken', simulatedToken);

      // Redirect to the home page after successful login
      this.$router.push('/home');
    },
  },
};
</script>

  
  <style scoped>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f4f4f4;
  }
  
  .login-form {
    max-width: 400px;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  h2 {
    text-align: center;
    color: #333;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-bottom: 16px;
    box-sizing: border-box;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    background-color: #007bff;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  
  .signup-link {
    display: block;
    text-align: center;
    margin-top: 10px;
    color: #007bff;
    text-decoration: none;
  }
  
  .signup-link:hover {
    text-decoration: underline;
  }
  </style>
  