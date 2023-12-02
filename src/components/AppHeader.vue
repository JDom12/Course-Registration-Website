<template>
  <header class="app-header">
<<<<<<< HEAD
    <div>
      <h1>{{ title }}</h1>
      <nav>
        <ul>
          <li>
            <RouterLink to="/">Home</RouterLink>
          </li>
          <li>
            <RouterLink to="/fetch">Fetch Example</RouterLink>
          </li>
          <li>
            <!--
              This RouterLink does not point to a specific path, but rather the name of a route.
              Check out router/index.js for how this is defined
            -->
            <RouterLink :to="{ name: 'form' }">Form Example</RouterLink>
          </li>
          <li>
            <RouterLink to="/register">Register for Course</RouterLink>
          </li>
          <li>
            <RouterLink to="/course">View Courses</RouterLink>
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
            <RouterLink to="/course_creation">Create Courses</RouterLink>
          </li>
        </ul>
      </nav>
    </div>
=======
    <img src="/husky_qa.jpeg" alt="Logo" class="logo">
    <h1>{{ title }}</h1>
>>>>>>> css-changes
  </header>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  title: String 
});
</script>

<style>
<<<<<<< HEAD
/* give the header itself a background color, a border, and add some padding to the content */
.app-header {
  background-color: #dcdcdc;
  border-bottom: 1px solid #dcdcdc;
  padding: 1rem;
}
/* make the title within the header a larger and bolder font */
=======

>>>>>>> css-changes
.app-header h1 {
  color: #ffffff; 
  text-align: center; 
  font-family: 'Arial', sans-serif; 
  font-size: 24px; 
  margin-left: 500px; 
  padding: 0; 
}
.app-header {
  display: flex; /* Enable items to be on same line */
  align-items: center; /* Vertically align items in the middle */
}
</style>