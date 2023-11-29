<template>
  <div id="app-layout">
    <AppHeader title="Course Registration" />
    <div class="main">
      <div class="sidebar">
        <ul>
          <li>
            <RouterLink to="/">Home</RouterLink>
          </li>
          <li v-if="isStudent || isAdmin">
            <RouterLink to="/register">Register for Course</RouterLink>
          </li>
          <li v-if="isStudent || isProf || isAdmin">
            <RouterLink to="/course">View Courses</RouterLink>
          </li>
          <li v-if="isProf || isAdmin">
            <RouterLink to="/edit">Edit Courses</RouterLink>
          </li>
          <li v-if="isAdmin">
            <RouterLink to="/usermanage">Manage Users</RouterLink>
          </li>
          <li v-if="isAdmin">
            <RouterLink to="/usersearch">Search for User</RouterLink>
          </li>
        </ul>
        <button @click="login" v-if="!isAuthenticated">Log In</button>
        <button @click="logout" v-if="isAuthenticated">Log Out</button>
      </div>
      <div class="content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script>
import { RouterView } from "vue-router";
import AppHeader from "./components/AppHeader.vue";
import { useAuth0 } from '@auth0/auth0-vue';
export default{
  setup() {
    const auth0 = useAuth0();
    return {
      isAuthenticated: auth0.isAuthenticated,
      isAdmin: auth0.isAdmin,
      isStudent: auth0.isStudent,
      isProf: auth0.isProf,
      netID: auth0.netID,
      login: () => {
        auth0.loginWithRedirect();
      },
      logout: () => {
        auth0.logout({ 
          logoutParams: { 
            returnTo: window.location.origin 
          } 
        });
      },
    };
  }
};
</script>

<style>
.app-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
}

.app-sidebar {
  /* Sidebar styles */
  background-color: #f5f5f5;
  padding: 20px;
  border-right: 1px solid #ccc;
}

.app-content {
  /* Styles for the main content area */
}
</style>
