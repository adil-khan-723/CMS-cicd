<template>
    <div class="theme-toggle">
      <h2>Theme Settings</h2>
      <button @click="toggleTheme">
        Switch to {{ isDarkMode ? "Light" : "Dark" }} Mode
      </button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isDarkMode: localStorage.getItem("theme") === "dark",
      };
    },
    mounted() {
      this.applyTheme();
    },
    methods: {
      toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        localStorage.setItem("theme", this.isDarkMode ? "dark" : "light");
        this.applyTheme();
      },
      applyTheme() {
        document.body.classList.toggle("dark-mode", this.isDarkMode);
      },
    },
  };
  </script>
  
  <style scoped>
  .theme-toggle {
    padding: 20px;
    text-align: center;
  }
  
  button {
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    font-size: 16px;
    background: var(--button-bg);
    color: var(--button-text);
  }
  
  button:hover {
    opacity: 0.8;
  }
  </style>
  