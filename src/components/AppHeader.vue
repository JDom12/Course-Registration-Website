<template>
  <header class="app-header">
    <img src="/husky_qa.jpeg" alt="Logo" class="logo">
    <h1>{{ title }}</h1>
  </header>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  title: String 
});
</script>

<style>

.app-header h1 {
  color: #ffffff; /* Change to your preferred color */
  text-align: center; /* Adjust text alignment as needed */
  font-family: 'Arial', sans-serif; /* Change to your preferred font */
  font-size: 24px; /* Adjust font size as needed */
  margin-left: 500px; /* Adjust or remove margin */
  padding: 0; /* Adjust or add padding as needed */
}
.app-header {
  display: flex; /* Enables Flexbox layout */
  align-items: center; /* Vertically align items in the middle */
  /* Add additional styling as needed */
}
</style>