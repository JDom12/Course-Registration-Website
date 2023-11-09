<template>
    <main class="form">
      <h2>Course Edit</h2>
      <p>
        This page allows modifications to be made to courses by Admins/Professors.
      </p>
  
      <form @submit.prevent="editcourse" class="editcourse">
        <label for="edit">Search Course</label>
        <input type="text" id="admin_id" name="admin" v-model="admin_name" />
        <button type="submit">Search</button>
      </form>


  <div>
    <table class="fetch">
      <thead>
        <tr>
          <th>Edit Class Name</th>
          <th>Edit Instructor</th>
          <th>Edit Room</th>
          <th>Edit Meeting Time</th>
          <th>Edit Prerequisites</th>
          <th>Edit Search Tags</th>
          <th>Edit Max Enrollment</th>
          <th>Action</th> <!-- added a new column for the save button -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="(course, index) in displayCourses" :key="course.class_name">
          <td>
            <input type="text" v-model="displayCourses[index].class_name" />
          </td>
          <td>
            <input type="text" v-model="displayCourses[index].instructor" />
          </td>
          <td>
            <input type="text" v-model="displayCourses[index].room" />
          </td>
          <td>
            <input type="text" v-model="displayCourses[index].meeting_time" />
          </td>
          <td>
            <input type="text" v-model="displayCourses[index].pre_requisites" />
          </td>
          <td>
            <input type="text" v-model="displayCourses[index].search_tags" />
          </td>
          <td>
            <input type="number" v-model="displayCourses[index].max_enrollment" />
          </td>
          <td>
            <button @click="saveCourse(index)">Save</button> <!-- Save button -->
          </td>
        </tr>
      </tbody>
    </table>
  </div>



  
      <ul>
        <!--
          v-for requires a unique key for every element so that it can efficiently keep track
          of each list item. it is possible for the user to type the same todo more than once,
          so the todo itself isn't necessarily unique. the index on its own is of course unique,
          it represents each unique place in the array. there are unfortunately edge case issues
          with using the index alone that we don't need to get into, so we combine the todo and
          the index into a unique key that will work in all situations
        -->

        <!-- <li v-for="(todo, index) in todos" :key="todo + index">
          {{ todo }}
          <button @click="delete_edit(index)">Delete</button>
        </li> -->

        <!-- <li v-for="(edit, index) in edits" :key="edit + index">
          {{ edits }}
          <button @click="delete_edit(index)">Delete</button>
        </li> -->

        <li v-if="edits.length > 0">
          <p>Edit Courses:</p>
        </li>
        <li v-if="edits.length > 0">
        </li>
        <li v-for="(edit, index) in edits" :key="edit + index">
          {{ edit }}
          <button @click="delete_edit(index)">Delete</button>
        </li>
  
        <!--
          it is a good user experience practice to provide feedback when in an "emtpy state",
          in this case, where there are no todos to show yet. this informs the user of
          the current status of the system (working), and doesn't make them wonder if something
          has gone wrong
         -->
        <!-- <li v-if="todos.length === 0"> -->
        <li v-if="edits.length === 0">
          <p>No Courses Entered</p>
        </li>
      </ul>
    </main>
  </template>
  
  <script setup>
  import { ref } from "vue";
  const newTodo = ref("");
  const edits = ref([]);
  function editcourse() {
    const todoToAdd = newTodo.value.trim();
    if (todoToAdd !== "") {
      edits.value.push(todoToAdd);
      newTodo.value = "";
    }
  }
  // function deleteTodo(index) {
    function editCourse(index, updatedCourseData) {
    const courseToUpdate = displayCourses[index];

    const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1';
    const path = '/EditCourse'; 
    const url = `${endpointURL}${path}`;

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        courseId: courseToUpdate.id, // 'id'is property name used to identify the course
        updatedCourseData,
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.statusCode === 200) {
        console.log(data.body); // successfully updated 
      } else {
        console.error(data.body); // error updating course
      }
    })
    .catch(error => {
      console.error("Error updating course:", error);
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
    color: #202020;
  }
  </style>