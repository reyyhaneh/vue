<template>
  <div class="profile-page">


    <div style="text-align: center">
      <img style="width: 100px; height: 100px; border-radius: 50%" :src="user.image" alt="Profile Picture"
           class="profile-picture"/>

      <h2>{{ user.contact_name }}<br/>{{ user.first_name }} {{ user.last_name }}</h2>
      <p>Phone: {{ user.phone }}</p>
      <p>Username: {{ user.username }}</p>
      <p>Bio: {{ user.bio }}</p>

      <div class="profile-options">
        <div>
          <input style="margin: 10px" v-show="!user.cid" v-model="user.contact_name" name="contact_name"
                 type="text"/>

        </div>
        <div>

          <button style="margin: 10px" v-show="!user.cid" @click="addToContactsOrFollow">Add to Contacts / Follow
          </button>

        </div>
        <div>
          <button style="margin: 10px" @click="deleteChat">Delete Chat</button>

        </div>
        <div>
          <button style="margin: 10px" v-show="user.cid" @click="deleteFromContacts">Delete from Contacts</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user: {
        id: '',
        cid: '',
        contact_name: '',
        chat: '',
        first_name: '',
        last_name: '',
        username: '',
        phone: '',
        image: ''
      }
    };
  },


  mounted() {

    this.fetchContactData();
  },

  methods: {
    fetchContactData() {
      this.user = JSON.parse(localStorage.getItem('contact'))
      console.log(this.user)

    },
    addToContactsOrFollow() {
      const token = localStorage.getItem('jwtToken');
      const uid = localStorage.getItem('uid');
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      axios.post('api/users/' + uid + '/contacts/', {
        "contact_name": this.user.contact_name,
        "contact": this.user.id,
      }, {headers})
      this.$router.push('/');
    },
    deleteChat() {
      const token = localStorage.getItem('jwtToken');
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      axios.delete('api/chat/' + this.user.chat + '/', {headers})
      this.$router.push('/');

    },
    deleteFromContacts() {
      const token = localStorage.getItem('jwtToken');
      const uid = localStorage.getItem('uid');
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      axios.delete('api/users/' + uid + '/contacts/' + this.user.cid + '/', {headers})
      this.$router.push('/');

    },
  }
};

</script>

<style scoped>
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
  