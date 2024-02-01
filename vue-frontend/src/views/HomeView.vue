<!-- Home.vue -->
<template>
  <div class="grid-container">
    <Navbar class="item1"/>
    <ChatList :chats="chats" @select-chat="selectChat" class="item2"/>
    <ChatDisplay :selectedChat="selectedChat" class="item3" />

  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'; // Adjust the path based on your project structure
import ChatList from '@/components/ChatList.vue';
import ChatDisplay from '@/components/ChatDisplay.vue';
import axios from 'axios';

export default {
  components: {
    Navbar,
    ChatList,
    ChatDisplay,
  },
   created() {
    // Check if the token is in localStorage
    const jwtToken = localStorage.getItem('jwtToken');

    // If the token is not present, redirect to the login page
    if (!jwtToken) {
      this.$router.push('/login');
    }
  },
  data() {
    return {
      chats: [
        {id: 1 ,name: "name",profilePic: "../assets/profile.png", unseenMessages: 0},
        {id: 2 ,name: "John Doe",profilePic: "../assets/profile.png", unseenMessages: 3},
        // Add more chat objects as needed
      ],
      selectedChat: null,
    };
  },
  methods: {
    async selectChat(chat) {
       const token = localStorage.getItem('jwtToken');

      const headers = {
        Authorization: `Bearer ${token}`,
      };
              const response = await axios.get('http://localhost:8000/api/chat/'+chat.id+'/',{headers});
      this.selectedChat = response.data;
    },
  },
};
</script>

<style>

.home {
  display: grid;
}
.item1 { grid-area: header; }
.item2 { grid-area: menu; }
.item3 { grid-area: main; }


.grid-container {
  display: grid;
  grid-template-areas:
    'header header header header header header'
    'menu main main main main main'
    'menu main main main main main';
  padding: 10px;
}
</style>
