<template>
    <main class="fetch">
      <h2>Course Search</h2>
      <p>
        For the university 
        <a
          href="https://catalog.uconn.edu/directory-of-courses/"
          >course catalog</a
        >.     </p>
      <label for="courseTypeSelect">
        Course Type:
        <select name="type" id="courseTypeSelect" v-model="selectedSecurityType">
          <option
            v-for="securityType in securityTypes"
            :key="securityType"
            :value="securityType"
          >
            {{ securityType }}
          </option>
        </select>
      </label>
      <table>
        <thead>
          <tr>
            <th>Class Name</th>
            <th>Intructor</th>
            <th>Room</th>
            <th>Meeting Time</th> 
            <th>Prerequistes</th>
            <th>Search Tags</th>
            <th>Max Enrollment</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in displaycourse" :key="course.class_name">
            <td>{{ course.class_name }}</td>
            <td>{{ course.instructor }}</td>
            <td>{{ course.room }}</td>
            <td>{{ course.meeting_time }}</td>
            <td>{{ course.pre_requisites }}</td>
            <td>{{ course.search_tags }}</td>
            <td>{{ course.max_enrollment }}</td>
          </tr>
        </tbody>
      </table>
    </main>
  </template>
  
  <script setup>
  import { ref, computed, watch } from "vue";
  import { monthNames } from "../util/constants";
  // the three financial security types in our api's dataset
  // const securityTypes = ["CMBs", "Bills", "Bonds", "FRNs", "Notes", "TIPS"];
  const securityTypes = ["ENG", "PHAR", "CSE", "PHYS", "LANG", "FRE"];
  // placeholder securityTypes
  // store the selected value in the dropdown
  const selectedSecurityType = ref(securityTypes[0]);
  // store the endpoint for our api request

  const rawApiData = ref(null);
  const data = ref();


  function fetchCoursesByType() {
    const courseType = selectedSecurityType.value.trim();
    const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
    const path = '/all_classes';

    if (courseType !== "") {
        const url = `${endpointURL}${path}?search_tags=${encodeURIComponent(courseType)}`;
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
            console.error('There was an error fetching the courses:', error);
        });
    }
  }

  // Watch for changes in selectedSecurityType and fetch courses
  watch(selectedSecurityType, () => {
      fetchCoursesByType();
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
  const displaycourse = computed(() =>
    records.value.map((course) => {
      return {
      class_name: course.class_name,
      instructor: course.instructor,
      room: course.room[0],
      meeting_time: course.meeting_time,
      pre_requisites: course.pre_requisites,
      search_tags: course.search_tags.join(', '),
      max_enrollment: course.max_enrollment,
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
  .fetch table{
    border: 1px solid #d9d9d9;
    color: #0D1463;
    background-color: #668aeb;
    
  }
  .fetch thead {
    background-color: #344e96;
    color: #ffffff;
  }
  /* setup the spacing and the text alignment of the table headers and table cells */
  .fetch :is(th, td) {
    text-align: left;
    padding: 0.25rem 0.75rem;
    min-width: 10rem;
  }
  /* make even numbered rows an off-white color to make the table more legible */
  .fetch tr:nth-child(even) {
    background-color: #90aeff;
    color:#0D1463;
    
  }
  </style>

  