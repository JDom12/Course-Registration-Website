<template>
    <main class="fetch">
      <h2>Student Schedule</h2>
      <p>
        Please enter your studentID to load your course schedule 
      </p>
      <table v-if="displaycourse.length > 0">
        <thead>
          <tr>
            <th>Class Name</th>
            <th>Class ID</th>
            <th>Intructor</th>
            <th>Room</th>
            <th>Meeting Time</th> 
            <th>Remaining Seats</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in displaycourse" :key="course.class_name">
            <td>{{ course.class_name }}</td>
            <td>{{ course.class_id }}</td>
            <td>{{ course.instructor }}</td>
            <td>{{ course.room }}</td>
            <td>{{ course.meeting_time }}</td>
            <td>{{ course.available_seats }}</td>
          </tr>
        </tbody>
      </table>
    </main>
</template>

<script setup>
import { ref,computed } from "vue";
import { useAuth0} from "@auth0/auth0-vue";
const auth0 = useAuth0();
const user = auth0.user;
const studentName = user._rawValue.name;
const data = ref([]);


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
    .then(responseData => {
      data.value = JSON.parse(responseData.body); 
    })
    .catch(error => {
      console.error('There was an error fetching the classes:', error);
    });
  };
}
const displaycourse = computed(() =>
    data.value.map((course) => {
      return {
      class_name: course.class_name,
      class_id: course.class_id,
      instructor: course.instructor,
      room: course.room.join(', '),
      meeting_time: course.meeting_time,
      available_seats: course.available_seats
      };
    })
)
studentLogin();
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
