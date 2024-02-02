<template>
  <div class="user-profile">
    <div v-if="editMode" style="text-align: center;" class="signup-form">
      <!-- Editable Fields -->
       <label for="first_name">First Name:</label>
    <input v-model="user.first_name" name="first_name" type="text" required />

    <label for="last_name">Last Name:</label>
    <input v-model="user.last_name" name="last_name" type="text" required />

    <label for="phone">Phone:</label>
    <input v-model="user.phone" name="phone" type="text" required :class="{ 'error': !isPhoneValid }" />
    <div v-if="!isPhoneValid">
      <p class="error-message">Phone must be exactly 10 digits long, start with 0, and consist of digits only.</p>
    </div>

    <label for="username">Username:</label>
    <input v-model="user.username" name="username" type="text" required :class="{ 'error': !isUsernameUnique }" />
    <div v-if="!isUsernameUnique">
      <p class="error-message">Username is already taken. Please choose a different one.</p>
    </div>


    <label for="password">Password:</label>
    <input v-model="user.password" name="password" type="password" required :class="{ 'error': isPasswordInvalid }" />
    <div v-if="isPasswordInvalid">
      <p class="error-message">Password must be at least 8 characters long.</p>
    </div>

    <label for="image">Image:</label>
    <input  ref="imageInput" name="image" type="file" accept="image/*" @change="handleImageChange" :class="{ 'error': !isImageValid }" />
    <div v-if="!isImageValid">
      <p class="error-message">Please select a valid image file.</p>
    </div>

    <label for="bio">Bio:</label>
    <textarea v-model="user.bio" name="bio" required></textarea>

      <button @click="saveChanges">Save Changes</button>
    </div>
    <div v-else style="text-align: center">
      <!-- Display Mode -->
              <img style="width: 100px; height: 100px; border-radius: 50%" :src="user.image" alt="Profile Picture" class="profile-picture" />

      <h2>{{ user.first_name }} {{ user.last_name }}</h2>
      <p>Phone: {{ user.phone }}</p>
      <p>Username: {{ user.username }}</p>
      <p>Bio: {{ user.bio }}</p>

      <button @click="toggleEditMode">Edit Profile</button>
<div  class="signup-form">
       <li v-for="contact in user.contacts" :key="contact.id" style=" text-align: center" @click="selectContact(contact)"  >
        <div class="chat-row" >
            <div >
              <img :src="contact.image || '/src/assets/profile.png'" alt="Profile Picture"
                   class="profile-pic"/>
            </div>
            <div class="chat-name">{{ contact.contact_name }}</div>
        </div>

      </li>
  </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {
        first_name: '',
        last_name: '',
        phone: '',
        username: '',
        password: '',
        image: '',
        bio: '',
        contacts: '',
      },
      editMode: false,
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
          username: this.user.username,
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
        if (/^0\d{10}$/.test(this.user.phone) && /^\d+$/.test(this.user.phone)) {
          const response = await axios.post('/api/checkphone/', {
            phone: this.user.phone,
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
      this.isPasswordInvalid = this.user.password.length < 8;
    },
    handleImageChange(event) {
      this.user.image = event.target.files[0];
      console.log(this.user.image)
      this.validateImage();
    },
    validateImage() {
      if (this.user.image && this.user.image.type.startsWith('image/')) {
        this.isImageValid = true;
      } else {
        this.isImageValid = false;
      }
    },
    async submitForm() {
          const token = localStorage.getItem('jwtToken');
       const uid = localStorage.getItem('uid');

      this.checkUsernameUniqueness();
      this.checkPhoneUniqueness();
      this.validatePassword();
      this.validateImage();

      if (this.isUsernameUnique && this.isPhoneUnique && !this.isPasswordInvalid && this.isImageValid) {
        try {
          this.loading = true;
           const formData = new FormData();
      formData.append('first_name', this.user.first_name);
      formData.append('last_name', this.user.last_name);
      formData.append('phone', this.user.phone);
      formData.append('username', this.user.username);
      formData.append('password', this.user.password);
      formData.append('image', this.user.image);
      formData.append('bio', this.user.bio);

      const response = await axios.put('/api/users/'+uid+'/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
                  Authorization: `Bearer ${token}`,

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


    toggleEditMode() {
      this.editMode = !this.editMode;
    },
    saveChanges() {
        const token = localStorage.getItem('jwtToken');
       const uid = localStorage.getItem('uid');
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      // Use Axios to fetch user data from your backend API
      axios.put('api/users/'+uid+'/',this.user,{headers})
        .then(response => {
          console.log('Profile updated successfully:', response.data);
        })
        .catch(error => {
          console.error('Error updating profile:', error);
        });

      // After saving changes, switch back to display mode
      this.editMode = false;
    },
  selectContact(contact) {
        const uid =     localStorage.getItem('uid')
         const token = localStorage.getItem('jwtToken');

      const headers = {
        Authorization: `Bearer ${token}`,
      };
      // Make a GET request to fetch chats from the Django API
      axios.get('http://localhost:8000/api/getcontact/'+contact.id+'/', {headers})
          .then(response => {
            localStorage.setItem('contact',JSON.stringify(response.data))
            console.log(response.data)
                  this.$router.push('/profile');

          })
    },

    fetchUserData() {
       const token = localStorage.getItem('jwtToken');
       const uid = localStorage.getItem('uid');
      const headers = {
        Authorization: `Bearer ${token}`,
      };
      // Use Axios to fetch user data from your backend API
      axios.get('api/users/'+uid+'/',{headers})
        .then(response => {
          // Update the user data in the component
          this.user = response.data;
          console.log(response.data)
          console.log(this.user)
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
    },
  },

  mounted() {
    // Fetch user data when the component is mounted
    this.fetchUserData();
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

img {

  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.chat-col {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.chat-row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.unread-count{
  background-color: greenyellow;
  border-radius: 50%;
  width: 20px;
  height: 20px;
text-align: center;
}
</style>
