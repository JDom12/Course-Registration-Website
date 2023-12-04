<template>
    <main class="form">
        <h2>Delete a course</h2>
        <p>Please enter the name of the class you would like to delete</p>
        <form @submit.prevent="DeleteCourse" class="unregisterCourse">
            <label for="ClassName">Enter a Course Name:</label>
            <input type="text" id="ClassName" v-model="ClassName" />
  
            <button type="submit">Delete</button>
        </form>
  
        <p v-if="apiResponse">{{ apiResponse }}</p>
    </main>
</template>
  
<script setup>
    import { ref } from "vue";
    const ClassName = ref("");
    const apiResponse = ref("");
    
    function DeleteCourse() {
        const course_name = ClassName.value.trim();
    
        const endpointURL = 'https://7lymtbki38.execute-api.us-east-1.amazonaws.com/Stage_1';
        const path = '/classes'; 
        const url = `${endpointURL}${path}`;
    
        fetch(url, {
        method: 'DELETE', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'class_name' : course_name })
        })
        .then(response => response.json())
        .then(data => {
            try {
                apiResponse.value = JSON.parse(data.body); //remove quotes
            } catch (error) {
                apiResponse.value = data.body; //in case of failure
            }
    ClassName.value = ""; 
        })
        .catch(error => {
        console.error("Error Deleting Course", error);
        apiResponse.value = `Error deleting course: ${error.message}`;
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