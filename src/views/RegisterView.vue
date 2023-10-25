<template>
  <main class="form">
    <h2>Register for a Course</h2>
    <p>
      Please enter your studentID and the courseID for the desired course. 
    </p>
    <form @submit.prevent="studentLogin" class="studentLogin">
      <label for="login">Enter Student ID to load classes</label>
      <input type="text" id="studentid" name="Student" v-model="studentName" />
      <button type="submit">Load</button>
    </form>
    <form @submit.prevent="registerCourse" class="registerCourse">
      <label for="registration">Register for Course</label>
      <input type="text" id="courseid" name="Course" v-model="courseName" />
      <button type="submit">Save</button>
    </form>

    <ul>
      <!--
        v-for requires a unique key for every element so that it can efficiently keep track
        of each list item. it is possible for the user to type the same todo more than once,
        so the todo itself isn't necessarily unique. the index on its own is of course unique,
        it represents each unique place in the array. there are unfortunately edge case issues
        with using the index alone that we don't need to get into, so we combine the todo and
        the index into a unique key that will work in all situations
      -->
      <li v-if="ids.length > 0">
        <p>Registered Courses for the Fall Semester:</p>
      </li>
      <li v-for="(courseID, index) in ids" :key="courseID + index">
        {{ courseID }}
        <button @click="unregisterCourse(index)">Unregister from Course</button>
      </li>

      <!--
        it is a good user experience practice to provide feedback when in an "emtpy state",
        in this case, where there are no todos to show yet. this informs the user of
        the current status of the system (working), and doesn't make them wonder if something
        has gone wrong
       -->
      <li v-if="ids.length === 0">
        <p>No courses yet, go ahead and register for one!</p>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { ref } from "vue";
const apiName = 'InsertAPINameHere'; //Change to finalized API database name

const studentName = ref("");
const courseName = ref("");
const ids = ref([]);

// function to run when the create todo form is submitted
function studentLogin() {
  const studentToAdd = studentName.value.trim();
  const path = '../../Lambda_Functions/Registration/course-view-student.py'; 
  const MyInit = {
    headers: {},
    queryStringParameters: {
      'netID' : studentToAdd,
    }
  };
  API.get(apiName, path, MyInit) 
    .then((response) => {
      ids.value.push(response);
    });
}

function registerCourse() {
  // sanitize the input by removing the whitespace from the beginning and end of newTodo.value
  const courseToAdd = courseName.value.trim();
  const studentToAdd = studentName.value.trim();
  // if the sanitized input is not an empty string (i.e., an actual todo), add it to the list and reset the form
  if (courseToAdd != "") {
    const path = '../../Lambda_Functions/Registration/course-register.py'
    const MyInit = {
      headers: {},
      queryStringParameters: {
        'netID' : studentToAdd,
        'courseID' : courseToAdd
      }
    }
    API.post(apiName, path, MyInit)
    ids.value.push(courseToAdd);
    courseName.value = "";  
  }
}

// when a todo's delete button is clicked, the index of that todo is passed to this function
// Array.splice takes an index in the array and a number of items to delete after that
function unregisterCourse(index) {
  newVals = ids.value.splice(index, 1);
  const courseToAdd = newVals.value.trim();
  const studentToAdd = studentName.value.trim();
  const path = "../..Lambda_Function/Registration/course-drop.py"
  const MyInit = {
    headers: {},
    queryStringParameters: {
      'netID' : studentToAdd,
      'class_ID' : courseToAdd
    }
  }
  API.put(apiName, path, MyInit)
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
