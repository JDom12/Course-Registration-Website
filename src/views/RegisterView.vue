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
    <p>{{ apiResponse }}</p>
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
      <li v-if="ids.length > 0">
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
      <li v-if="ids.length == 0">
        <p>No courses yet, go ahead and register for one!</p>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { ref } from "vue";
//const apiName = 'InsertAPINameHere'; //Change to finalized API database name

const studentName = ref("");
const courseName = ref("");
const ids = ref([]);
const apiResponse = ref("");

// function to run when the create todo form is submitted
function studentLogin() {
  const netID = studentName.value.trim();
  const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
  const path = '/RegisteredClasses'

  if (netID !== ""){
    const url = `${endpointURL}${path}?netID=${encodeURIComponent(netID)}`;

    fetch(url,{
      method: 'GET',
      headers: {
        'Content-Type' : 'application/json',
      }
    })
    .then(response => response.json())
    .then(data => {
      ids.value = JSON.parse(data.body); 
    })
    .catch(error => {
      console.error('There was an error fetching the classes:', error);
    });
  };

}

function registerCourse() {
  // sanitize the input by removing the whitespace from the beginning and end of the input values
  const class_name = courseName.value.trim();
  const netID = studentName.value.trim();

  const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 

  const path = '/registration'; 

  if (class_name !== "") {
    
    const url = `${endpointURL}${path}`;

    // Make POST request
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
      ids.value.push(class_name);
      courseName.value = "";
    })
    .catch(error => {
      // Handle errors
      console.error("Error registering course:", error);
    });
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
