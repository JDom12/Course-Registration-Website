<template>
  <div id="app-layout">
    <AppHeader title="Course Registration" />
    <div class="main">
      <div class="sidebar">
        <ul>
          <li>
            <RouterLink to="/">Home</RouterLink>
          </li>
          <li v-if="user.userroles == 'isStudent'">
            <RouterLink to="/register">Register for Course</RouterLink>
          </li>
          <li v-if="user.userroles == 'isStudent'">
            <RouterLink to="/StudentUnenroll">Unenroll from a Course</RouterLink>
          </li>
          <li v-if="isAuthenticated">
            <RouterLink to="/course">View Courses</RouterLink>
          </li>
          <li v-if="user.userroles == 'isProfessor' || user.userroles == 'isAdmin'">
            <RouterLink to=/course_creation>Add a Course</RouterLink>
          </li>
          <li v-if="user.userroles == 'isProfessor' || user.userroles == 'isAdmin'">
            <RouterLink to="/edit">Edit Courses</RouterLink>
          </li>
          <li v-if="user.userroles == 'isAdmin'">
            <RouterLink to="/usermanage">Manage Users</RouterLink>
          </li>
          <li v-if="user.userroles == 'isAdmin'">
            <RouterLink to="/usersearch">Search for User</RouterLink>
          </li>
          <li v-if="user.userroles == 'isStudent'">
            <RouterLink to="/StudentSchedule">View Student Schedule</RouterLink>
          </li>
          <li v-if="user.userroles == 'isAdmin'">
            <RouterLink to="/AdminRegister">Register for a Student</RouterLink>
          </li>
          <li v-if="user.userroles == 'isAdmin'">
            <RouterLink to="/AdminSchedule">View Student's Schedule</RouterLink>
          </li>
          <li v-if="user.userroles == 'isProfessor' || user.userroles == 'isAdmin'">
            <RouterLink to="/ProfessorSchedule">View and Edit Instructor Schedule</RouterLink>
          </li>
        </ul>
        <b-button @click="login" v-if="!isAuthenticated">Log In</b-button>
        <b-button @click="logout" v-if="isAuthenticated">Log Out</b-button>
      </div>
      <div class="content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue";
import { RouterView } from "vue-router";
import { useAuth0 } from '@auth0/auth0-vue';
export default{
  components: {
    "AppHeader":AppHeader
  },
  setup() {
    const auth0 = useAuth0();
    return {
      isAuthenticated: auth0.isAuthenticated,
      user: auth0.user,
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
</style>
