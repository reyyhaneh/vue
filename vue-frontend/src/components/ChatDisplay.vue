<template>
  <div class="chat-display">
    <div v-if="selectedChat">
      <h2>{{ selectedChat.name }}</h2>
      <div
          style="padding: 20px"
          v-for="message in selectedChat.messages"
          :key="message.id"
          :class="{ 'my-message': isMyMessage(message.sender.id) }"
          @mouseover="setHoveredMessage(message.id)"
          @mouseout="resetHoveredMessage()"
      >
        <p>
          <span
              class="message-text"
              :class="{ 'my-message-text': isMyMessage(message.sender.id), 'msg-content': true }"
          >
            {{ message.content }}
          </span>
          <br/>
        <div class="msg-time">
          {{ message.created_at }}
        </div>
        <div
            v-show="hoveredMessageId === message.id && isMyMessage(message.sender.id)"
            class="message-actions"
            :class="{ 'my-btns': isMyMessage(message.sender.id) }"
        >
          <button @click="editMessage(message.id)">Edit</button>
          <button @click="deleteMessage(message.id)">Delete</button>
        </div>
        </p>
      </div>
      <div class="message-input-container sticky-input">
        <input
            id="msg-input"
            v-model="newMessage"
            placeholder="Type your message..."
            :style="{ backgroundColor: editMode ? '#ffcccb' : 'white' }"
        />
        <button id="send-btn" @click="sendMessage">Send</button>
      </div>
    </div>
    <div v-else>
      <p>Select a chat to start the conversation</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    selectedChat: Object, // The selected chat object
  },
  data() {
    return {
      newMessage: '', // Input for typing a new message
      hoveredMessageId: null,
      editMode: false, // Add edit mode flag
    };
  },
  methods: {
    isMyMessage(senderId) {
      const uid = localStorage.getItem('uid');
      return senderId.toString() === uid.toString();
    },
    sendMessage() {
      const token = localStorage.getItem('jwtToken');
      const headers = {
        Authorization: `Bearer ${token}`,
      };

      axios
          .post('api/chat/' + this.selectedChat.id + '/message/', {content: this.newMessage,}, {headers})
          .then((response) => {
            console.log('Message sent successfully:', response.data);
          })
          .catch((error) => {
            console.error('Error sending message:', error);
          });
      this.newMessage = '';
    },
    setHoveredMessage(messageId) {
      this.hoveredMessageId = messageId;
    },
    resetHoveredMessage() {
      this.hoveredMessageId = null;
    },
    editMessage(messageId) {
      const element = document.getElementById('msg-input');
      element.classList.add('msg-edit');
      this.editMode = !this.editMode;

       const token = localStorage.getItem('jwtToken');
      const headers = {
        Authorization: `Bearer ${token}`,
      };

      axios
          .put('api/chat/' + this.selectedChat.id + '/message/'+messageId+'/', {content: this.newMessage,}, {headers})
      this.newMessage = '';
    },
    deleteMessage(messageId) {
      const token = localStorage.getItem('jwtToken');
      const headers = {
        Authorization: `Bearer ${token}`,
      };

      axios
          .delete('api/chat/' + this.selectedChat.id + '/message/' + messageId + '/', {headers})
    },
  },
};
</script>

<style scoped>
/* Your existing styles */
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

.my-message {
  text-align: right;
}

.my-message-text {
  background-color: #58afff !important;
}

.msg-content {
  background-color: #205b8f;
  color: white;
  padding: 10px;
  border-radius: 10px;
}

.message-input-container {
  display: flex;
  margin: 20px;
}

.message-input-container input {
  flex: 1;
  padding: 8px;
  margin-right: 10px;
}

.message-input-container button {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.message-input-container button:hover {
  background-color: #0056b3;
}

.msg-time {
  margin: 10px 7px 7px 7px;
  font-size: small;
  font-weight: bold;
}

.message-actions {
  display: flex;
  margin-top: 5px;
}

.message-actions button {
  margin-right: 5px;
}

.my-btns {
  justify-content: end;
}

.sticky-input {
  flex: 1;
  padding: 8px;
  margin-right: 10px;
  position: sticky;
  bottom: 0;
}

.msg-edit {
  background-color: red;
}
</style>
