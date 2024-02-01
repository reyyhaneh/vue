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

export default {
  components: {
    Navbar,
    ChatList,
    ChatDisplay,
  },
  data() {
    return {
      chats: [
        { id: 1, name: 'Chat 1', content: 'Chat 1 content...' },
        { id: 2, name: 'Chat 2', content: 'Chat 2 content...' },
        // Add more chat objects as needed
      ],
      selectedChat: null,
    };
  },
  methods: {
    selectChat(chat) {
      this.selectedChat = chat;
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
