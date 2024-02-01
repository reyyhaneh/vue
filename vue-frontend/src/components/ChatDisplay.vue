<template>
    <div class="chat-display">
      <div v-if="selectedChat">
        <h2>{{ selectedChat.name }}</h2>
        <div v-for="message in selectedChat.messages" :key="message.id">
          <p>{{ message.sender.username }}: {{ message.content }}</p>
        </div>
      </div>
      <div v-else>
        <p>Select a chat to start the conversation</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      selectedChat: Object, // The selected chat object
    },
  };
  </script>
  
  <style scoped>
  .chat-display {
    padding: 20px;
    right: 0;
    position: absolute;
    bottom: 0;
    height: 85%;
    margin-top: 10px;
    position: absolute;
    grid-column-start: 4;
    width: 76%;
  }
  
  </style>
  