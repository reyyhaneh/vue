<template>
  <div class="navbar">
    <div class="navbar-left">
      <a @click="profile">

        <img src="../assets/profile.png" alt="Profile Picture" class="profile-pic"/>
      </a>
    </div>
    <div class="navbar-right">
      <button class="logout-button" @click="logout">Log Out</button>
      <button class="delete-account-button" @click="deleteAccount">Delete Account</button>
    </div>
  </div>

</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('jwtToken');
      localStorage.removeItem('uid');

      this.$router.push('/login');
    },
    deleteAccount() {
    },
    profile() {
      this.$router.push('/userProfile');

    }, contact() {
      this.$router.push('/contact');

    }
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #81ceb8;
  color: #fff;
  grid-column-start: 1;
  grid-column-end: 4;
  position: absolute;
  right: 0;
  left: 0;
  top: 0;
  height: 6%;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.logout-button,
.delete-account-button {
  background-color: #151269;
  color: #fff;
  border: none;
  padding: 8px 16px;
  margin-left: 10px;
  cursor: pointer;
}

.logout-button:hover,
.delete-account-button:hover {
  background-color: #0f1056;
}
</style>
  