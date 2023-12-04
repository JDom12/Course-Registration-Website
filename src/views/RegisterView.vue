<template>
  <main class="form">
    <h2>Register for a Course</h2>
    <p>Please enter the course name for the desired course.</p>
    <form @submit.prevent="registerCourse" class="registerCourse">
      <label for="registration">Register for Course</label>
      <input type="text" id="courseid" name="Course" v-model="courseName" />
      <button type="submit">Register</button>
    </form>
    <div v-if="apiResponse">
      <p>{{ apiResponse }}</p>
    </div>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useAuth0 } from '@auth0/auth0-vue';

const auth0 = useAuth0();
const user = auth0.user;
const courseName = ref("");
const apiResponse = ref("");

function registerCourse() {
  const class_name = courseName.value.trim();
  const netID = user._rawValue.name;
  const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
  const path = '/registration'; 

  if (class_name !== "") {
    const url = `${endpointURL}${path}`;
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        netID: netID,
        class_name: class_name
      })
    })
    .then(response => response.json())
    .then(data => {
      apiResponse.value = data.body;
      courseName.value = "";
    })
    .catch(error => {
      console.error("Error registering course:", error);
    });
  }
}
</script>

<style>
  .form {
    padding: 1rem;
  }

  .form h2 {
    font-size: 1.5rem;
    margin-bottom: 2rem;
  }

  .form p {
    margin-bottom: 1rem;
  }
</style>