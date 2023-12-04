<template>
  <main class="form">
    <h2>This is the Course Creation page.</h2>
    <p>
      This page is for an administrator to create new courses. They can add the course name, instructor, room, meeting time, etc.
    </p>

    <form @submit.prevent="createTodo" class="create-todo">
      <input type="text" id="todo" name="todo" v-model="classname" placeholder = "Classname" />
      <input type="text" id="class_id" name="class_id" v-model="class_id" placeholder = "Class ID" />
      <input type = "text" id="instructor" name="instructor" v-model="instructor" placeholder = "Instructor name"/>
      <input type = "text" id = "room" name="room" v-model= "room" placeholder = "Room" />
      <input type = "text" id = "search_tags" name="search_tags" v-model= "search_tags" placeholder = "Ex. PHAR" />
      <input type = "text" id = "prerequisite" name="prerequisite" v-model= "prerequisite" placeholder = "Seperate multiple prerequisites with comma and space" />
      <input type = "text" id = "meeting_time" name = "meeting_time" v-model = "meeting_time" placeholder = "Ex. M / W / F 1:00-2:00"/>
      <input type = "text" id = "max_enrollment" name = "max_enrollment" v-model = "max_enrollment" placeholder = "Max Enrollment" />
      
      <button type="submit">Save</button>
      <!-- add more fields for each variable-->
    </form>
    <p v-if="apiResponse">{{ apiResponse }}</p> 
  </main>
</template>

<script setup>
import { ref } from "vue";

const classname = ref("") ;  
const classnamed = ref("");

const class_id = ref("");
const instructor = ref("") ; 
const room = ref("");
const meeting_time = ref("");
const prerequisite = ref("");
const search_tags = ref(""); // list
const max_enrollment = ref(null);

const apiResponse = ref("");

// function to run when the create todo form is submitted
function createTodo() {
  const endpointURL = "https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1" ;
  const path = '/classes'; 

  const url = `${endpointURL}${path}`;

  fetch(url, { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'class_name': classname.value,
        'class_id' : class_id.value,
        'instructor' : instructor.value,
        'room' : room.value,
        'meeting_time' : meeting_time.value,
        'pre_requisites' : prerequisite.value,
        'search_tags' : search_tags.value,
        'max_enrollment' : max_enrollment.value,
      })
    })
    .then(response => response.json())
    .then(data => {
      apiResponse.value = JSON.parse(data.body);
      // Reset fields after submission
      classname.value = "";
      class_id.value = "";
      instructor.value = "";
      room.value = "";
      meeting_time.value = "";
      prerequisite.value = ""; 
      search_tags.value = ""; 
      max_enrollment.value = null;
    })
    .catch(error => {
      console.error("Error creating course:", error);
  });
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
/* flex layouts allow us to position elements next to each other that would otherwise have been on top of each other */
.form ul {
  display: flex;
  gap: 1rem;
  flex-direction: column;
}
.form li {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
/* create some space beneath the create todo form */
.form form {
  margin-bottom: 1rem;
}
/* set some default styling to buttons and inputs for borders, heights, and padding */
.form :is(input, button) {
  line-height: 2rem;
  padding-inline: 0.5rem;
  border-radius: 0.375rem;
  border: 1px solid #d9d9d9;
  margin-left: 0.5rem;
  color: #8a8a8a;
}
</style>