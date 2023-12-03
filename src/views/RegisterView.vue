<template>
  <main class="form">
    <h2>Register for a Course</h2>
    <p>
      Please enter the courseID for the desired course. 
    </p>
    <form @submit.prevent="studentLogin" class="studentLogin">
      <label for="login">Load Classes</label>
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
import { useAuth0 } from '@auth0/auth0-vue';
const auth0 = useAuth0();
const user = auth0.user;
const studentName = user.name;
const courseName = ref("");
const ids = ref([]);
const apiResponse = ref("");

// function to run when the create todo form is submitted
function studentLogin() {
  const netID = studentName;
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
  const netID = studentName;

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
  const courseToRemove = ids.value.splice(index, 1)[0]; 
  const studentToRemove = studentName;

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
      class_name: courseToRemove
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.statusCode === 200) {
      console.log(data.body); // Successfully unregistered
    } else {
      console.error(data.body); // Error unregistering
      ids.value.splice(index, 0, courseToRemove); // Re-add the course if there was an error
    }
  })
  .catch(error => {
    console.error("Error unregistering course:", error);
    ids.value.splice(index, 0, courseToRemove); // Re-add the course if there was an error
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
