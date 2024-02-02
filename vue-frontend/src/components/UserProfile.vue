<template>
    <div class="user-profile">
      <div v-if="editMode">
        <!-- Editable Fields -->
        <label for="firstname">First Name:</label>
        <input v-model="user.firstname" name="firstname" type="text" required />
  
        <label for="lastname">Last Name:</label>
        <input v-model="user.lastname" name="lastname" type="text" required />
  
        <label for="phone">Phone:</label>
        <input v-model="user.phone" name="phone" type="text" required />
  
        <label for="username">Username:</label>
        <input v-model="user.username" name="username" type="text" required />
  
        <label for="password">Password:</label>
        <input v-model="user.password" name="password" type="password" required />
  
        <label for="image">Image:</label>
        <input v-model="user.image" name="image" type="text" />
  
        <label for="bio">Bio:</label>
        <textarea v-model="user.bio" name="bio" required></textarea>
  
        <button @click="saveChanges">Save Changes</button>
      </div>
      <div v-else>
        <!-- Display Mode -->
        <h2>{{ user.firstname }} {{ user.lastname }}</h2>
        <p>Phone: {{ user.phone }}</p>
        <p>Username: {{ user.username }}</p>
        <p>Bio: {{ user.bio }}</p>
  
        <button @click="toggleEditMode">Edit Profile</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        user: {
          firstname: 'John',
          lastname: 'Doe',
          phone: '123456789',
          username: 'johndoe',
          password: '', // For security reasons, usually not displayed in the profile
          image: 'path/to/profile.jpg',
          bio: 'A brief bio about me...',
        },
        editMode: false,
      };
    },
    methods: {
      toggleEditMode() {
        this.editMode = !this.editMode;
      },
      saveChanges() {
        // Implement logic to save changes to the backend API
        // You can use an API request to update the user's profile
        console.log('Saving changes...');
        // After saving changes, switch back to display mode
        this.editMode = false;
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  .user-profile {
    padding: 20px;
  }
  
  /* Style for error messages if needed */
  .error-message {
    color: red;
  }
  </style>
  