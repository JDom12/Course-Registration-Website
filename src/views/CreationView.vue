<template>
  <main class="form">
    <h2>This is the Course Creation page.</h2>
    <p>
      This page is for an administrator to create new courses. They can add the course name, instructor, room, meeting time, etc.
    </p>

    <form @submit.prevent="createTodo" class="create-todo">
      <label for="todo">New Course</label>
      <input type="text" id="todo" name="todo" v-model="classname" placeholder = "Classname" />
      <input type = "text" id="instructor" name="instructor" v-model="instructor" placeholder = "Instructor"/>
      <input type = "text" id = "room" name="room" v-model= "room" placeholder = "Room" />
      <input type = "text" id = "meeting_time" name = "meeting_time" v-model = "meeting_time" placeholder = "Meeting Time"/>
      <input type = "text" id = "max_enrollment" name = "max_enrollment" v-model = "max_enrollment" placeholder = "Max Enrollment" />
      
      <button type="submit">Save</button>
      <!-- add more fields for each variable-->
    </form>
    <!-- only add string variables for now - will add update course function later-->
    <form @submit.prevent = "deleteTodo" class = "delete-todo">
      <label for = "delete"> Delete Course</label>
      <input type = "text" id = "delete" name = "delete" v-model="classnamed" placeholder = "Classname" />
      <button type = "submit">Delete</button>
    </form>
  </main>
</template>

<script setup>
import { ref } from "vue";

const classname = ref("") ;  
const classnamed = ref("");

const instructor = ref("") ; 
const room = ref("");
const meeting_time = ref("");
const pre_requisites = ref([]); // list
const search_tags = ref([]); // list
const max_enrollment = ref("");

const apiResponse = ref("");

// function to run when the create todo form is submitted
function createTodo() {
  const endpointURL = "https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'" ;
  const path = '/all_classes'; 

  const url = `${endpointURL}${path}`;

  fetch(url, { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        class_name: classname,
        'instructor' : instructor.value,
        'room' : room.value,
        'meeting_time' : meeting_time.value,
        'pre_requisites' : pre_requisites.value,
        'search_tags' : search_tags.value,
        'max_enrollment' : max_enrollment.value,

      })
    })
    .then(response => response.json())
    .then(data => {
      apiResponse.value = data.body;
      classname.value = "";
      instructor.value = "";
      room.value = "";
      meeting_time.value = "";
      pre_requisites.value = [];
      search_tags.value = [];
      max_enrollment.value = "";
      // do for all variables
    })
    .catch(error => {
      // Handle errors
      console.error("Error creating course:", error);
    });
  }

// when a todo's delete button is clicked, the index of that todo is passed to this function
// Array.splice takes an index in the array and a number of items to delete after that
function deleteTodo(index) {
  const coursetoremove =  classnamed.value.trim();

  const endpointURL = "https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1" ;
  const path = '/all_classes'; 

  const url = `${endpointURL}${path}`;

  fetch(url, {
    method: 'DELETE', 
    headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        class_name : coursetoremove,
      }
      )  
  })
  .then(response => response.json())
  .then(data=> {
    if (data.statusCode === 200) {
      console.log(data.body); // successfully deleted course
    } else{
      console.error(data.body); // error
    }
    classnamed.value = "" ;
  })
  .catch(error => {
    console.error("Error deleting course:", error);
  })
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