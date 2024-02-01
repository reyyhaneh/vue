<!-- ChatList.vue -->
<template>
    <div class="chat-list">
      <input v-model="searchQuery" placeholder="Search..." class="search-bar" />
      <ul>
        <li v-for="chat in filteredChats" :key="chat.id" @click="selectChat(chat)">
          <div class="chat-item">
            <img src="../assets/profile.png" alt="Profile Picture" class="profile-pic" />
            <div class="chat-details">
              <div class="chat-name">{{ chat.name }}</div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      chats: Array, // Array of chat objects received from the backend
    },
    data() {
      return {
        searchQuery: '',
      };
    },
    computed: {
      filteredChats() {
        // Filter the chats based on the search query
        return this.chats.filter(chat => chat.name.toLowerCase().includes(this.searchQuery.toLowerCase()));
      },
    },
    methods: {
      selectChat(chat) {
        // Emit an event to notify the parent component about the selected chat
        this.$emit('select-chat', chat);
      },
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
  
  .chat-item {
    display: flex;
    align-items: center;
    margin: 5px;

  }
  
  .profile-pic {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
  }
  
  .chat-details {
    flex: 1;
  }
  
  .chat-name {
    font-weight: bold;
  }
  
  .unseen-messages {
    color: #777;
    font-size: 0.8em;
  }
  li:hover {
  background-color: #e0e0e0;
}
  </style>
  