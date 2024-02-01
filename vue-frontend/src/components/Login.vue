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
      <p v-if="error" class="error-message">{{ error }}</p>
      <router-link to="/" class="signup-link">Don't have an account? Sign Up</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/api/login/', this.form);

        if (response.data.hasOwnProperty('access')) {
          const token =response.data.access;
          const uid = response.data.uid;
          localStorage.setItem('jwtToken', token);
          localStorage.setItem('uid', token);
          this.$router.push('/');
          // console.log(token)
        } else {
          // Handle the case where the 'token' key is missing in the response
          this.error = response.data.error;
        }
      } catch (error) {
        console.error('Login failed:', error);
        this.error = 'Invalid username or password'; // Set a custom error message
      }
    },
  },
};
</script>

  <style scoped>
  .error-message {
  color: red;
  margin-top: 10px;
  text-align: center;
  }
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
