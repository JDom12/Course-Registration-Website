<template>
    <main class="fetch">
      <h2>User Management</h2>
      <p>
        For use by administrators only. 
      </p>
      <form @submit.prevent="userSearch" class="userSearch">
        <label for="login">Enter User ID to view User Information: </label>
        <input type="text" id="studentid" name="Student" v-model="userID" />
        <button type="submit">Load</button>
      </form>
      <div v-if="isDataAvailable()">
        <table>
          <thead>
            <tr>
              <th>NetID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Email</th>
              <th>Role</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="usersID in ids" :key="usersID.netID">
              <td>{{ usersID.netID }}</td>
              <td>{{ usersID.first_name }}</td>
              <td>{{ usersID.last_name }}</td>
              <td>{{ usersID.email }}</td>
              <td>{{ usersID.role }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td>Immutable</td> 
              <td><input type="text" v-model="newUser.first_name" placeholder="First Name"></td>
              <td><input type="text" v-model="newUser.last_name" placeholder="Last Name"></td>
              <td><input type="text" v-model="newUser.email" placeholder="Email"></td>
              <td>Immutable</td>
              <td><button @click="userChange">Submit</button></td>
            </tr>
          </tfoot>
        </table>
      </div>
      <p v-if="message_search">{{ message_search }}</p>
    </main>
    <p v-if="message_change">{{ message_search }}</p>
  </template>
  
<script setup>
import { ref } from "vue";

const userID = ref("");
const ids = ref([]);
const newUser = ref({
  netID: '',
  first_name: '',
  last_name: '',
  email: '',
  role: ''
})
const message_search = ref("");
const message_change = ref("");


function isDataAvailable() {
  const condition = ids.value && ids.value.length > 0;
  return condition;
}

function userSearch() {
  const netID = userID.value.trim();
  const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
  const path = '/user';

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
      ids.value = [JSON.parse(data.body)]; 
      console.log(ids);
      userID.value = "";
      message_search.value = "";
    })
    .catch(error => {
      console.error('There was an error fetching the classes:', error);
      message_search.value = `error fetching user profile: ${error.message}`;
      console.log(message_search);
    });
  };
}

function userChange(){

  const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
  const path = '/user';
  const url = `${endpointURL}${path}`;

  const UserToUpdate = { ...newUser.value };

  for (const key in UserToUpdate) {
    if (UserToUpdate[key] == '') {
      UserToUpdate[key] = ids.value[0][key];
    }
  }
  fetch(url, {
    method: 'PUT', 
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(UserToUpdate),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    message_change.value = "User successfully update";
  })
  .catch((error) => {
    console.error('Error:', error);
    message_change.value = `Error updating user: ${error.message}`;
    console.log(message_change);
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