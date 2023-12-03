<template>
    <main class="fetch">
        <h2>View and Edit your Courses</h2>
        <p>Load Schedule Information:</p>
        <form @submit.prevent="FetchCourse" class="FetchCourse">
            <label for="instructorID">Enter instructor name to load course:</label>
            <input type="text" id="instructorID" v-model="instructorID"/>
            <button type="submit">Load</button>
        </form>
            <h3>Course Information:</h3>
            <table v-if="displaycourse.length > 0">
                <thead>
                    <tr>
                        <th>Class Name</th>
                        <th>Class ID</th>
                        <th>Instructor</th>
                        <th>Room</th>
                        <th>Meeting Time</th> 
                        <th>Prerequisites</th>
                        <th>Search Tags</th>
                        <th>Max Enrollment</th>
                        <th>Available Seats</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="course in displaycourse" :key="course.class_id">
                        <td>{{ course.class_name }}</td>
                        <td>{{ course.class_id }}</td>
                        <td>{{ course.instructor }}</td>
                        <td><input type="text" v-model="course.room" placeholder="Room"></td>
                        <td><input type="text" v-model="course.meeting_time" placeholder="Meeting Time"></td>
                        <td><input type="text" v-model="course.pre_requisites" placeholder="Prerequisites"></td>
                        <td><input type="text" v-model="course.search_tags" placeholder="Search Tags"></td>
                        <td>{{ course.max_enrollment }}</td>
                        <td>{{ course.available_seats }}</td>
                        <td><button @click="submitCourse(course)">Submit</button></td>
                    </tr>
                </tbody>
            </table>
        <p v-if="message_submit"> {{ message_submit }}</p>
        <p v-if="message_fetch">{{ message_fetch }}</p>
    </main>
  </template>
  
  <script setup>
  import { ref, computed } from "vue";
  
  const newCourse = ref({
  class_name: '',
  class_id: '',
  instructor: '',
  room: '',
  meeting_time: '',
  pre_requisites: '',
  search_tags: '',
  max_enrollment: null,
  available_seats: null
  });
  
  const instructorID = ref("");
  const data = ref([]); 
  const message_fetch = ref("");
  const message_submit = ref("");
  
function FetchCourse() {
    const netID = instructorID.value.trim();
    const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
    const path = '/instructor'

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

function submitCourse() {
    console.log('Submitting course:', newCourse.value);
    
    const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1'; 
    const path = '/classes'
    const url = `${endpointURL}${path}`;
    const courseDataToUpdate = { ...newCourse.value };
    
    for (const key in courseDataToUpdate) {
        //additional logic for certain attributes stored in lists
        if (key == "pre_requisites" && courseDataToUpdate["pre_requisites"] !== ''){
        let split_string = newCourse.value[key].split(", ");
        courseDataToUpdate[key] = split_string;
        } 
        if (key == "room" && courseDataToUpdate["room"] !== ''){
        let split_string = newCourse.value[key].split(", ");
        courseDataToUpdate[key] = split_string;
        } 
        if (key == "search_tags" && courseDataToUpdate["search_tags"] !== ''){
        let split_string = newCourse.value[key].split(", ");
        courseDataToUpdate[key] = split_string;
        } 
        //pass in fetched data if nothing is to be changed
        else if (courseDataToUpdate[key] == '') {
        courseDataToUpdate[key] = data.value[0][key];
        }
    }
  
    fetch(url, {
        method: 'PUT', 
        headers: {
        'Content-Type': 'application/json',
        },
        body: JSON.stringify(courseDataToUpdate),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        message_fetch.value = "course sucessfuly updated";
    })
    .catch((error) => {
        console.error('Error:', error);
        message_fetch.value = `error updating course: ${error.message}`;
    });
    }
  
const displaycourse = computed(() => {
const courses = data.value.map((course) => {
    return {
    class_name: course.class_name,
    class_id: course.class_id,
    instructor: course.instructor,
    room: course.room.join(", "),
    meeting_time: course.meeting_time,
    pre_requisites: course.pre_requisites.join(", "),
    search_tags: course.search_tags.join(", "),
    max_enrollment: course.max_enrollment,
    available_seats: course.available_seats
    };
});
console.log(courses); 
return courses;
});
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