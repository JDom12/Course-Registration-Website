<template>
  <header class="app-header">
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
            <RouterLink to="/course_creation">Create Courses</RouterLink>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup>
// import the <RouterLink> component so that we can use it in the template above
import { RouterLink } from "vue-router";
// give this component a title property so that the parent component (app.vue) can set whatever title it wants
defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>

<style>
/* give the header itself a background color, a border, and add some padding to the content */
.app-header {
  background-color: #dcdcdc;
  border-bottom: 1px solid #dcdcdc;
  padding: 1rem;
}
/* make the title within the header a larger and bolder font */
.app-header h1 {
  font-size: 2rem;
  font-weight: bold;
}
</style>