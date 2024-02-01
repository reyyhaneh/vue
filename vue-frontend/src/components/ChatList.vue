<!-- ChatList.vue -->
<template>
    <div class="chat-list">
      <input v-model="searchQuery" placeholder="Search..." class="search-bar" />
      <ul>
        
        <li v-for="chat in filteredChats" :key="chat.id" @click="selectChat(chat)">
        <div class="chat-item">
        <router-link to="/profile">
        <img src="../assets/profile.png" alt="Profile Picture" class="profile-pic" />
        </router-link>          <div class="chat-details">
            <div class="chat-name">{{ chat.name }}</div>
            <div class="unseen-messages" v-if="chat.unseenMessages > 0">{{ chat.unseenMessages }} unseen messages</div>
          </div>
        </div>
            
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {

    props: {
      // Remove the 'chats' prop
    },
    data() {
      return {
        searchQuery: '',
        chats: [], // Store chats locally
      };
    },
    computed: {
  
      filteredChats() {
        console.log(this.chats)
        return this.chats.filter(chat =>
          chat.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      },
    },
    methods: {
      selectChat(chat) {
        this.$emit('select-chat', chat);
      },
      fetchChats() {
          const headers = {
          Authorization: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzExOTkwMzcyLCJpYXQiOjE3MDY4MDYzNzIsImp0aSI6IjA3M2FhMzVmZDM5MzRhODBiYzdlOTE2NjY3MzlhNDk0IiwidXNlcl9pZCI6MX0.Y3_X9-XnQ7jQ7H2uNrfTliL3ZA84hjhWIsbetkoahRw`,
        };
        // Make a GET request to fetch chats from the Django API
        axios.get('http://localhost:8000/api/chat/', { headers })
          .then(response => {
            this.chats = response.data;
          })
          .catch(error => {
            console.error('Error fetching chats:', error);
          });
      },
    },
    mounted() {
      // Fetch chats when the component is mounted
      this.fetchChats();
    },
  };
  </script>
  
  <style scoped>
  /* Add your styling here */
  .chat-list {
    position: fixed;
    top: 62px; /* Adjust based on the height of your navbar */
    left: 0;
    bottom: 0;
    width: 20%;
    overflow-y: auto;
    background-color: #f4f4f4;
    border-right: 1px solid #ddd;
    padding: 10px;
    background-color: #81b1ce;
  }
  
  .search-bar {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  
  ul {
    list-style: none;
    padding: 0;
    margin-top: 10px;
  }
  
  li {
    padding: 10px;
    cursor: pointer;
    border-bottom: 1px solid #eee;
  }
  
  li:hover {
    background-color: #e0e0e0;
  }
  </style>