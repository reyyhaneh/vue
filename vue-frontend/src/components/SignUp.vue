<template>
    <form @submit.prevent="submitForm" class="signup-form">
      <label for="firstname">First Name:</label>
      <input v-model="form.firstname" name="firstname" type="text" required />
  
      <label for="lastname">Last Name:</label>
      <input v-model="form.lastname" name="lastname" type="text" required />
  
      <label for="phone">Phone:</label>
      <input v-model="form.phone" name="phone" type="text" required />
  
      <label for="username">Username:</label>
      <input v-model="form.username" name="username" type="text" required />
  
      <label for="password">Password:</label>
      <input v-model="form.password" name="password" type="password" required />
  
      <label for="image">Image:</label>
      <input v-model="form.image" name="image" type="text" />
  
      <label for="bio">Bio:</label>
      <textarea v-model="form.bio" name="bio" required></textarea>

      <div v-if="!isUsernameUnique">
      <p class="error-message">Username is already taken. Please choose a different one.</p>
      </div>
      <div v-if="!isPhoneUnique">
      <p class="error-message">Phone number is already in use. Please enter a different one.</p>
      </div>
  
      <button type="submit">Sign Up</button>
      <router-link to="/login" class="login-link">Already have an account? Log In</router-link>

    </form>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        form: {
          firstname: '',
          lastname: '',
          phone: '',
          username: '',
          password: '',
          image: null,
          bio: '',
        },
        isUsernameUnique: true,
        isPhoneUnique: true,
      };
    },
    methods: {
    async checkUsernameUniqueness() {
      // Make a request to the backend API to check the uniqueness of the username
      // Assume your backend API endpoint is /api/check-username

      try {
        const response = await this.$axios.post('/api/check-username', {
          username: this.form.username,
        });

        // Check the response from the backend
        this.isUsernameUnique = response.data.isUnique;
      } catch (error) {
        console.error('Error checking username uniqueness:', error);
      }
    },
    async checkPhoneUniqueness() {
      // Make a request to the backend API to check the uniqueness of the phone number
      // Assume your backend API endpoint is /api/check-phone

      try {
        const response = await this.$axios.post('/api/check-phone', {
          phone: this.form.phone,
        });

        // Check the response from the backend
        this.isPhoneUnique = response.data.isUnique;
      } catch (error) {
        console.error('Error checking phone uniqueness:', error);
      }
    },
    async submitForm() {
      // Check uniqueness before submitting the form
      await this.checkUsernameUniqueness();
      await this.checkPhoneUniqueness();

      // Proceed with form submission if both username and phone are unique
      if (this.isUsernameUnique && this.isPhoneUnique) {
        try {
          // Make a request to the backend to get the JWT token
          const response = await this.$axios.post('/api/register', {
            firstname: this.form.firstname,
            lastname: this.form.lastname,
            phone: this.form.phone,
            username: this.form.username,
            password: this.form.password,
            image: this.form.image,
            bio: this.form.bio,
            
          });

          // Assuming the backend returns a JWT token upon successful registration
          const jwtToken = response.data.token;

          // Store the token in localStorage (or use a more secure storage mechanism)
          localStorage.setItem('jwtToken', jwtToken);

          // Redirect to the user's dashboard or home page
          this.$router.push('/home');
        } catch (error) {
          console.error('Error registering user:', error);
        }
      } else {
        // Show a message to the user about non-unique username or phone
        console.error('Username or phone is not unique. Please choose different values.');
      }
    },
    },
  };
  </script>
  

  
<style scoped>
.signup-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 8px;
}

label {
  display: block;
  margin-bottom: 8px;
}

input,
textarea {
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
  margin:5px;
}
.login-link {
  display: block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}

button:hover {
  background-color: #0056b3;
}
.error-message {
  color: #ff0000; 
}
</style>