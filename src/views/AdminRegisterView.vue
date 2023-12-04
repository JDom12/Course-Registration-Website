<template>
    <main class="form">
      <h2>Register for a Course</h2>
      <p>
        Please enter a student's studentID and the courseID for the desired course. 
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
        <li v-if="ids.length > 0">
          <p>Registered Courses for the Fall Semester:</p>
        </li>
        <li v-for="(item, index) in ids" :key="index">
          {{ item.message }}
          <button v-if="item.isSuccess" @click="unregisterCourse(item.message, index)">
             Unregister from Course
          </button>
        </li>
        <li v-if="ids.length == 0">
          <p>No courses yet, go ahead and register for one!</p>
       </li>
  </ul>
    </main>
  </template>
  
  <script setup>
  import { ref } from "vue";
  const studentName = ref("");
  const courseName = ref("");
  const ids = ref([]);
  const apiResponse = ref("");
  // function to run when the create todo form is submitted
  function studentLogin() {
  const netID = studentName.value.trim();
  const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
  const path = '/RegisteredClasses';
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
        apiResponse.value = data.body;
        const parsedData = JSON.parse(data.body);
        // Assuming that an error message does not have a 'class_name' property
        ids.value = parsedData
          .filter(item => item.class_name && item.isSuccess !== false)
          .map(item => {
            return { message: item.class_name, isSuccess: true };
          });
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
    apiResponse.value = '';
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
        if (data.statusCode === 200) { 
          ids.value.push({ message: class_name, isSuccess: true });
        } else {
          ids.value.push({ message: data.body, isSuccess: false });
        }
        courseName.value = "";
        console.log(ids.value);
      })
      .catch(error => {
        // Handle errors
        console.error("Error registering course:", error);
      });
    }
  }
  // when a todo's delete button is clicked, the index of that todo is passed to this function
  // Array.splice takes an index in the array and a number of items to delete after that
  function unregisterCourse(courseName, index) {
  const studentToRemove = studentName.value.trim();
  const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1';
  const path = '/DropCourse'; 
  const url = `${endpointURL}${path}`;

  fetch(url, {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      netID: studentToRemove,
      class_name: courseName 
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.statusCode === 200) {
      console.log(data.body); // Successfully unregistered
      ids.value.splice(index, 1); // Remove the course from the list
    } else {
      console.error(data.body); // Error unregistering
    }
  })
  .catch(error => {
    console.error("Error unregistering course:", error);
  });
}

  </script>
  
  <style>
    /* add padding around the page */
    .fetch {
      padding: 1rem;
    }
    /* make the heading font larger and add spacing below */
    .fetch h2 {
      font-size: 1.5rem;
      margin-bottom: 2rem;
    }
    /* add spacing below the text */
    .fetch p {
      margin-bottom: 1rem;
    }
    /* add borders to the table and its top row */
    .fetch table,
    .fetch thead {
      border: 1px solid #d9d9d9;
    }
    /* setup the spacing and the text alignment of the table headers and table cells */
    .fetch :is(th, td) {
      text-align: left;
      padding: 0.25rem 0.75rem;
      min-width: 10rem;
    }
    /* make even numbered rows an off-white color to make the table more legible */
    .fetch tr:nth-child(even) {
      background-color: #f9f9f9;
    }
  </style>