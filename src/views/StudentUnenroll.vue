<template>
    <main class="form">
        <h2>Unregister from a Course</h2>
        <p>Please enter the courseID for the course you wish to unregister from.</p>
        <form @submit.prevent="unregisterCourse" class="unregisterCourse">
            <label for="courseid">Enter Course ID:</label>
            <input type="text" id="courseid" v-model="courseName" />
  
            <button type="submit">Unregister</button>
        </form>
  
        <p v-if="apiResponse">{{ apiResponse }}</p>
    </main>
</template>
  
<script setup>
    import { ref } from "vue";
    import { useAuth0} from "@auth0/auth0-vue";
    const auth0 = useAuth0();
    const user = auth0.user;
    const studentName = user._rawValue.name;
    const courseName = ref("");
    const apiResponse = ref("");
    
    function unregisterCourse() {
        const netID = studentName;
        const class_name = courseName.value.trim();
    
        const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1';
        const path = '/DropCourse'; 
        const url = `${endpointURL}${path}`;
    
        fetch(url, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ netID, class_name })
        })
        .then(response => response.json())
        .then(data => {
        apiResponse.value = data.body;
        courseName.value = ""; 
        })
        .catch(error => {
        console.error("Error unregistering course:", error);
        apiResponse.value = `Error unregistering course: ${error.message}`;
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