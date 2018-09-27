<template>
  <div id="app">
    <nav>
      <h2 class="site-title">Short Shared Stories</h2>
      <ul>
        <li><router-link to="/">Recent Stories</router-link></li>
        <li><router-link to="/yours">Your Stories</router-link></li>
        <li><router-link to="/write">Write</router-link></li>
      </ul>
    </nav>
    <router-view/>
  </div>
</template>
<script>
import './main.css';
export default {};
</script>
