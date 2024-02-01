<template>
    <div class="profile-page">
      <div class="profile-header">
        <img :src="user.picture" alt="Profile Picture" class="profile-picture" />
        <div class="profile-info">
          <h2>{{ user.name }}</h2>
          <p>{{ user.status }}</p>
        </div>
      </div>
  
      <div class="profile-options">
        <!-- Add to contacts / Follow button -->
        <button @click="addToContactsOrFollow">Add to Contacts / Follow</button>
  
        <!-- Delete chat button -->
        <button @click="deleteChat">Delete Chat</button>
  
        <!-- Delete from contacts button -->
        <button @click="deleteFromContacts">Delete from Contacts</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        user: {
          name: 'John Doe',
          picture: '@/assets/profile.png', // Replace with the actual path
          status: 'Online', // or 'Offline'
        },
      };
    },
    methods: {
      addToContactsOrFollow() {
        // Implement logic for adding to contacts or following
        console.log('Adding to contacts or following...');
      },
      deleteChat() {
        // Implement logic for deleting the chat
        console.log('Deleting the chat...');
      },
      deleteFromContacts() {
        // Implement logic for deleting from contacts
        console.log('Deleting from contacts...');
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  .profile-page {
    padding: 20px;
  }
  
  .profile-header {
    display: flex;
    align-items: center;
  }
  
  .profile-picture {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-right: 20px;
  }
  
  .profile-info {
    flex: 1;
  }
  
  .profile-options {
    margin-top: 20px;
  }
  
  button {
    margin-right: 10px;
    padding: 10px;
    cursor: pointer;
  }
  </style>
  