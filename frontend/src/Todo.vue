<template>
  <div id="app">
    <h1>To-Do List</h1>
    <index label="lalala" :done="false"></index>
  </div>
</template>

<script>
import Index from './components/index.vue';

export default {
  name: 'App',
  components: {
    Index
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
