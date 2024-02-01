<template>
  <form @submit.prevent="submitForm" class="signup-form">
    <label for="first_name">First Name:</label>
    <input v-model="form.first_name" name="first_name" type="text" required />

    <label for="last_name">Last Name:</label>
    <input v-model="form.last_name" name="last_name" type="text" required />

    <label for="phone">Phone:</label>
    <input v-model="form.phone" name="phone" type="text" required :class="{ 'error': !isPhoneValid }" />
    <div v-if="!isPhoneValid">
      <p class="error-message">Phone must be exactly 13 digits long, start with 0, and consist of digits only.</p>
    </div>

    <label for="username">Username:</label>
    <input v-model="form.username" name="username" type="text" required :class="{ 'error': !isUsernameUnique }" />
    <div v-if="!isUsernameUnique">
      <p class="error-message">Username is already taken. Please choose a different one.</p>
    </div>

    <label for="password">Password:</label>
    <input v-model="form.password" name="password" type="password" required :class="{ 'error': isPasswordInvalid }" />
    <div v-if="isPasswordInvalid">
      <p class="error-message">Password must be at least 8 characters long.</p>
    </div>

    <label for="image">Image:</label>
    <input ref="imageInput" name="image" type="file" accept="image/*" @change="handleImageChange" :class="{ 'error': !isImageValid }" />
    <div v-if="!isImageValid">
      <p class="error-message">Please select a valid image file.</p>
    </div>

    <label for="bio">Bio:</label>
    <textarea v-model="form.bio" name="bio" required></textarea>

    <button type="submit" :disabled="loading">Sign Up</button>
    <router-link to="/login" class="login-link">Already have an account? Log In</router-link>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        phone: '',
        username: '',
        password: '',
        image: null,
        bio: '',
      },
      isUsernameUnique: true,
      isPhoneUnique: true,
      isPasswordInvalid: false,
      isPhoneValid: true,
      isImageValid: true,
      loading: false,
    };
  },
  methods: {
    async checkUsernameUniqueness() {
      try {
        this.loading = true;
        const response = await axios.post('/api/checkusername/', {
          username: this.form.username,
        });

        this.isUsernameUnique = response.data.unique;
      } catch (error) {
        console.error('Error checking username uniqueness:', error);
      } finally {
        this.loading = false;
      }
    },
    async checkPhoneUniqueness() {
      try {
        this.loading = true;
        if (/^0\d{10}$/.test(this.form.phone) && /^\d+$/.test(this.form.phone)) {
          const response = await axios.post('/api/checkphone/', {
            phone: this.form.phone,
          });

          this.isPhoneUnique = response.data.unique;
        } else {
          this.isPhoneValid = false;
        }
      } catch (error) {
        console.error('Error checking phone uniqueness:', error);
      } finally {
        this.loading = false;
      }
    },
    validatePassword() {
      this.isPasswordInvalid = this.form.password.length < 8;
    },
    handleImageChange(event) {
      this.form.image = event.target.files[0];
      this.validateImage();
    },
    validateImage() {
      if (this.form.image && this.form.image.type.startsWith('image/')) {
        this.isImageValid = true;
      } else {
        this.isImageValid = false;
      }
    },
    async submitForm() {
      this.checkUsernameUniqueness();
      this.checkPhoneUniqueness();
      this.validatePassword();
      this.validateImage();

      if (this.isUsernameUnique && this.isPhoneUnique && !this.isPasswordInvalid && this.isImageValid) {
        try {
          this.loading = true;
           const formData = new FormData();
      formData.append('first_name', this.form.first_name);
      formData.append('last_name', this.form.last_name);
      formData.append('phone', this.form.phone);
      formData.append('username', this.form.username);
      formData.append('password', this.form.password);
      formData.append('image', this.form.image);
      formData.append('bio', this.form.bio);

      const response = await axios.post('/api/register/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

          // const jwtToken = response.data.token;
          // localStorage.setItem('jwtToken', jwtToken);

          this.$router.push('/login');
        } catch (error) {
          console.error('Error registering user:', error);
        } finally {
          this.loading = false;
        }
      } else {
        console.error('Form validation failed. Please correct the errors.');
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
  margin: 5px;
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

input.error {
  border: 1px solid #ff0000;
}
</style>
