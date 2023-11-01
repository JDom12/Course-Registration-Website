<template>
    <main class="fetch">
      <h2>User Management</h2>
      <p>
        For use by administrators only. 
      </p>
      <label for="userTypeSelect">
        User Type:
        <select name="type" id="userTypeSelect" v-model="selectedUserType">
          <option
            v-for="userType in userTypes"
            :key="userType"
            :value="userType"
          >
            {{ userType }}
          </option>
        </select>
      </label>
      <table>
        <thead>
          <tr>
            <th>NetID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="userid in displayuser" :key="userid.netid">
            <td>{{ userid.netid }}</td>
            <td>{{ userid.first_name }}</td>
            <td>{{ userid.last_name }}</td>
            <td>{{ userid.email }}</td>
          </tr>
        </tbody>
      </table>
    </main>
  </template>
  
  <script setup>
  import { ref, computed, watch } from "vue";
  const userTypes = ["Student", "Instructor", "Administrator"];
  // store the selected value in the dropdown
  const selectedUserType = ref(userTypes[0]);
  // store the endpoint for our api request

  const rawApiData = ref(null);
  const data = ref();


  function fetchUsersByType() {
    const userType = selectedUserType.value.trim();
    const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
    const path = '/user'; //Change the API path to the correct one

    if (userType !== "") {
        const url = `${endpointURL}${path}?search_tags=${encodeURIComponent(userType)}`;
        console.log("Constructed URL:", url);
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(apiResponse => {
            rawApiData.value = JSON.stringify(apiResponse, null, 2);  //For debugging purposes
            data.value = JSON.parse(apiResponse.body);  
        })
        .catch(error => {
            console.error('There was an error fetching users:', error);
        });
    }
  }

  // Watch for changes in selectedSecurityType and fetch courses
  watch(selectedUserType, () => {
      fetchUsersByType();
  }, { immediate: true });


  // take 25 of the data points from the API, if there is a value in our data ref
  // otherwise, return an empty array
  const records = computed(() => {
  if (data.value && Array.isArray(data.value)) { // Check if data.value is an array
    return data.value.slice(0, 25);
  } else {
    return [];
  }
  });
  // convert each item in records (noting that for this code, we don't need to worry about unfetched data!)
  // into an object that has a formatted date and the value we want to display
  const displayuser = computed(() =>
    records.value.map((user) => {
      return {
      netid: user.netid,
      first_name: user.first_name,
      last_name: user.last_name,
      ids: user.ids,
      };
    })
  );
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