<template>
  <div id="app-layout">
    <AppHeader title="Course Registration" />
    <div class="main">
      <div class="sidebar">
        <ul>
          <li>
            <RouterLink to="/">Home</RouterLink>
          </li>
          <li>
            <RouterLink to="/register">Register for Course</RouterLink>
          </li>
          <li>
            <RouterLink to="/StudentUnenroll">Unenroll from a Course</RouterLink>
          </li>
          <li>
            <RouterLink to="/course">View Courses</RouterLink>
          </li>
          <li>
            <RouterLink to="/edit">Edit Courses</RouterLink>
          </li>
          <li>
            <RouterLink to="/edit">Edit Courses</RouterLink>
          </li>
          <li>
            <RouterLink to="/usermanage">Manage Users</RouterLink>
          </li>
          <li>
            <RouterLink to="/usersearch">Search for User</RouterLink>
          </li>
          <li>
            <RouterLink to="/StudentSchedule">View Student Schedule</RouterLink>
          </li>
          <li>
            <RouterLink to="/ProfessorSchedule">View and Edit Instructor Schedule</RouterLink>
          </li>
        </ul>
      </div>
      <div class="content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import AppHeader from "./components/AppHeader.vue";
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
