<template>
    <main class="form">
      <h2>User Management</h2>
      <p>
        For administrator use only. 
      </p>
      <form @submit.prevent="createUser" class="createUser">
        <label for="creation">Enter new netID to create a new user</label>
        <input type="text" id="netid" name="User" v-model="userIDc" placeholder="NetID" />
        <input type="text" id="first" name="FirstName" v-model="first_name" placeholder="First Name" />
        <input type="text" id="last" name="LastName" v-model="last_name" placeholder="Last Name" />
        <input type="text" id="email" name="email" v-model="email" placeholder="Email" />
        <input type="text" id="role" name="Role" v-model="role" placeholder="Role" />
        <button type="submit">Create</button>
      </form>
      <form @submit.prevent="deleteUser" class="deleteUser">
        <label for="deletion">Enter User's netid to delete them</label>
        <input type="text" id="netid" name="User" v-model="userIDd" placeholder="NetID" />
        <button type="submit">Delete</button>
      </form>
    </main>
  </template>
  
  <script setup>
  //Setup for user creation and deletion
  import { ref } from "vue";
  
  const userIDc = ref("");
  const first_name = ref("");
  const last_name = ref("");
  const email = ref("");
  const role = ref("");
  const userIDd = ref("");
  const apiResponse = ref("");
  
  function createUser() {
    // sanitize the input by removing the whitespace from the beginning and end of the input values
    const netID = userIDc.value.trim();
  
    const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
  
    const path = '/user'; //Change api path here
  
    if (netID !== "") {
      
      const url = `${endpointURL}${path}`;
  
      // Make POST request
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          netID: netID,
          'first_name': first_name,
          'last_name': last_name,
          'email': email,
          'role': role
        })
      })
      .then(response => response.json())
      .then(data => {
        apiResponse.value = data.body;
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
  function deleteUser(index) { 
    const userToRemove = userIDd.value.trim();
  
    const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1';
    const path = '/user'; //Change API path here
    const url = `${endpointURL}${path}`;
  
    fetch(url, {
      method: 'DELETE', 
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        netID: userToRemove,
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.statusCode === 200) {
        console.log(data.body); // Successfully unregistered
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
  