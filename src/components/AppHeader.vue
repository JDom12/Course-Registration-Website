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
  color: #ffffff; 
  text-align: center; 
  font-family: 'Arial', sans-serif; 
  font-size: 24px; 
  margin-left: 500px; 
  padding: 0; 
}
.app-header {
  display: flex; /* Enable items to be on same line */
  align-items: center; /* Vertically align items in the middle */
}
</style>