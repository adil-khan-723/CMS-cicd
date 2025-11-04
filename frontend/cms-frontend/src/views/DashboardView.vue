<template>
  <div class="dashboard" :class="{ 'dark-mode': isDarkMode }">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="logo-section">
        <h1 class="logo">blooog</h1>
      </div>

      <div class="user-section">
        <p class="username">Welcome, <strong>{{ username }}</strong></p>
        <button class="new-post" @click="$router.push('/new-post')">
          <i class="fas fa-plus"></i> NEW POST
        </button>
      </div>

      <div class="menu-section">
        <nav>
          <ul>
            <li v-for="(item, index) in menuItems" :key="index" :class="{ active: activeIndex === index }"
              @click="setActive(index, item.name)">
              <i :class="item.icon"></i>
              <span class="menu-text">{{ item.name }}</span>
              <span v-if="item.name === 'Theme'" class="theme-toggle" @click.stop="toggleTheme">
                <i :class="isDarkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
              </span>
            </li>
          </ul>
        </nav>

        <!-- Anonymous Toggle -->
        <div class="anonymous-toggle-container">
          <label class="anonymous-toggle">
            <input type="checkbox" v-model="showAnonymous">
            <span class="slider round"></span>
          </label>
          <span class="anonymous-label">{{ showAnonymous ? 'Anonymous' : 'Normal' }} Posts</span>
        </div>
      </div>

      <!-- Logout Button -->
      <button class="logout" @click="showLogoutModal = true">
        <i class="fas fa-sign-out-alt"></i> Logout
      </button>
    </aside>

    <!-- Main Content -->
    <main class="content">
      <!-- Loading Bar and Transition -->
      <div v-if="isLoading" class="transition-container">
        <div class="loading-bar">
          <div class="loading-progress" :style="{ width: loadingProgress + '%' }"></div>
        </div>
        <div class="loading-text">{{ loadingText }}</div>
      </div>

      <!-- Posts Section -->
      <transition name="fade" mode="out-in">
        <div v-if="activeSection === 'Posts' && !isLoading">
          <DashboardPosts 
            :isDarkMode="isDarkMode" 
            :showAnonymous="showAnonymous"
            @update-posts="handlePostsUpdate"
          />
        </div>
      </transition>

      <!-- Manage Posts Section -->
      <transition name="fade" mode="out-in">
        <div v-if="activeSection === 'Manage Posts' && !isLoading">
          <ManagePosts 
            :isDarkMode="isDarkMode" 
            :showAnonymous="showAnonymous"
            @update-posts="handlePostsUpdate"
          />
        </div>
      </transition>

      <!-- Theme Section -->
      <transition name="fade" mode="out-in">
        <div v-if="activeSection === 'Theme' && !isLoading" class="theme-section">
          <h2>Theme Settings</h2>
          <div class="theme-toggle-large" @click="toggleTheme">
            <i :class="isDarkMode ? 'fas fa-sun' : 'fas fa-moon'"></i>
            <span>{{ isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode' }}</span>
          </div>
        </div>
      </transition>
    </main>

    <!-- Logout Confirmation Modal -->
    <div v-if="showLogoutModal" class="modal-overlay">
      <div class="modal">
        <h2>Are you sure you want to logout?</h2>
        <p>You will be redirected to the homepage.</p>
        <div class="modal-buttons">
          <button class="cancel" @click="showLogoutModal = false">Cancel</button>
          <button class="confirm" @click="handleLogout">Logout</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserDetails, logoutUser } from "../api";
import DashboardPosts from "./dashboard_components/DashboardPosts.vue";
import ManagePosts from "./dashboard_components/ManagePosts.vue";

export default {
  name: "DashboardView",
  components: { DashboardPosts, ManagePosts },

  data() {
    return {
      username: "",
      activeIndex: 0,
      activeSection: "Posts",
      showLogoutModal: false,
      allPosts: [], // Stores all posts from API
      isDarkMode: false,
      isLoading: false,
      loadingProgress: 0,
      loadingText: "Loading Posts...",
      showAnonymous: false, // Toggle state for anonymous posts
      menuItems: [
        { name: "Posts", icon: "fas fa-file-alt" },
        { name: "Manage Posts", icon: "fas fa-list" },
        { name: "Theme", icon: "fas fa-paint-brush" },
      ],
    };
  },

  computed: {
    // Filter posts based on anonymous toggle
    filteredPosts() {
      if (!this.showAnonymous) {
        return this.allPosts.filter(post => !post.is_anonymous);
      }
      return this.allPosts;
    }
  },

  watch: {
    showAnonymous() {
      // This will trigger child components to update via their props
    }
  },

  async created() {
    this.activeIndex = 0;
    const token = localStorage.getItem("access_token");

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      this.isDarkMode = true;
    }

    if (!token) {
      this.$router.replace("/login");
      return;
    }

    try {
      const user = await getUserDetails(token);
      if (user && user.username) {
        this.username = user.username;
      } else {
        this.$router.replace("/login");
      }
    } catch (error) {
      this.$router.replace("/login");
    }
  },

  methods: {
    handlePostsUpdate(posts) {
      this.allPosts = posts;
    },

    setActive(index, section) {
      if (this.activeIndex === index) return;
      
      this.isLoading = true;
      this.loadingProgress = 0;
      
      // Set loading text based on the section
      switch(section) {
        case 'Posts':
          this.loadingText = "Loading your posts...";
          break;
        case 'Manage Posts':
          this.loadingText = "Preparing post management...";
          break;
        case 'Theme':
          this.loadingText = "Loading theme settings...";
          break;
        default:
          this.loadingText = "Loading...";
      }
      
      // Simulate loading progress
      const interval = setInterval(() => {
        this.loadingProgress += 10;
        if (this.loadingProgress >= 100) {
          clearInterval(interval);
          this.activeIndex = index;
          this.activeSection = section;
          setTimeout(() => {
            this.isLoading = false;
          }, 300);
        }
      }, 50);
    },

    handleLogout() {
      logoutUser();
      this.$router.replace("/");
    },

    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
      // Save preference to localStorage
      localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
    }
  }
};
</script>

<style scoped>
/* General Layout */
.dashboard {
  display: flex;
  height: 100vh;
  background-color: #f4f4f4;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.dashboard.dark-mode {
  background-color: #121212;
  color: #e0e0e0;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background-color: white;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  padding: 20px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.dark-mode .sidebar {
  background-color: #1e1e1e;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3);
}

/* Logo Section */
.logo-section {
  text-align: left;
  margin-bottom: 50px;
}

.logo {
  color: #ff6600;
  font-size: 42px;
  font-weight: 900;
  letter-spacing: 1px;
}

/* User Section */
.user-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 50px;
}

.username {
  color: gray;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 25px;
}

.dark-mode .username {
  color: #a0a0a0;
}

/* New Post Button */
.new-post {
  width: 100%;
  background-color: #ff6600;
  color: white;
  border: none;
  padding: 14px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  text-align: left;
  padding-left: 15px;
  transition: background 0.3s ease;
}

.new-post:hover {
  background-color: #e55d00;
}

/* Menu Section */
.menu-section {
  margin-top: 15px;
}

nav ul {
  list-style: none;
  padding: 0;
  margin-left: 5px;
}

nav ul li {
  display: flex;
  align-items: center;
  color: #333;
  margin: 10px 0;
  font-size: 17px;
  font-weight: bold;
  cursor: pointer;
  padding: 12px;
  border-radius: 5px;
  transition: all 0.3s ease;
  position: relative;
}

.dark-mode nav ul li {
  color: #e0e0e0;
}

nav ul li i {
  margin-right: 10px;
  font-size: 18px;
}

.menu-text {
  flex-grow: 1;
}

.theme-toggle {
  margin-left: 10px;
  color: #ff6600;
}

/* Active State */
nav ul li.active {
  background-color: rgba(255, 102, 0, 0.2);
  color: #ff6600;
  font-weight: bold;
}

.dark-mode nav ul li.active {
  background-color: rgba(255, 102, 0, 0.3);
}

/* Hover Effect */
nav ul li:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.dark-mode nav ul li:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

/* Anonymous Toggle Styles */
.anonymous-toggle-container {
  display: flex;
  align-items: center;
  margin-top: 30px;
  padding: 10px 15px;
  border-radius: 8px;
  background-color: rgba(255, 102, 0, 0.1);
  transition: background-color 0.3s ease;
}

.dark-mode .anonymous-toggle-container {
  background-color: rgba(255, 102, 0, 0.2);
}

.anonymous-toggle {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
  margin-right: 10px;
}

.anonymous-toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #ff6600;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.anonymous-label {
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.dark-mode .anonymous-label {
  color: #e0e0e0;
}

/* Logout Button */
.logout {
  width: 100%;
  background-color: #ff6600;
  color: white;
  border: none;
  padding: 14px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  margin-top: auto;
  text-align: left;
  padding-left: 15px;
  transition: background 0.3s ease;
}

.logout:hover {
  background-color: #e55d00;
}

/* Main Content */
.content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  background-color: white;
  transition: background-color 0.3s ease;
  position: relative;
}

.dark-mode .content {
  background-color: #121212;
}

/* Transition Container */
.transition-container {
  width: 100%;
  padding: 20px 0;
  text-align: center;
}

.loading-bar {
  width: 100%;
  height: 6px;
  background-color: rgba(255, 102, 0, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 15px;
}

.loading-progress {
  height: 100%;
  background-color: #ff6600;
  border-radius: 3px;
  transition: width 0.1s linear;
}

.loading-text {
  color: #ff6600;
  font-weight: bold;
  font-size: 18px;
}

.dark-mode .loading-text {
  color: #ff8c42;
}

/* Theme Section */
.theme-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.theme-toggle-large {
  display: flex;
  align-items: center;
  padding: 15px 25px;
  background-color: rgba(255, 102, 0, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.theme-toggle-large:hover {
  background-color: rgba(255, 102, 0, 0.2);
}

.theme-toggle-large i {
  font-size: 24px;
  margin-right: 15px;
  color: #ff6600;
}

.dark-mode .theme-toggle-large {
  background-color: rgba(255, 102, 0, 0.2);
}

.dark-mode .theme-toggle-large:hover {
  background-color: rgba(255, 102, 0, 0.3);
}

/* Transition Effects */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Enhanced Modal Styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(7px);
  z-index: 1000;
}

.modal {
  background: #ffffff;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
  max-width: 420px;
  width: 90%;
  animation: fadeIn 0.3s ease-in-out;
}

.dark-mode .modal {
  background: #2d2d2d;
  color: #e0e0e0;
}

.modal h2 {
  margin-bottom: 15px;
  font-size: 20px;
  color: #333;
}

.dark-mode .modal h2 {
  color: #e0e0e0;
}

.modal p {
  margin-bottom: 25px;
  font-size: 16px;
  color: #555;
}

.dark-mode .modal p {
  color: #b0b0b0;
}

.modal-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.modal-buttons button {
  padding: 12px 20px;
  border: none;
  cursor: pointer;
  border-radius: 6px;
  font-size: 15px;
  font-weight: bold;
  transition: 0.3s;
  width: 45%;
}

/* Cancel Button - Muted */
.cancel {
  background: #ddd;
  color: #333;
}

.dark-mode .cancel {
  background: #444;
  color: #e0e0e0;
}

.cancel:hover {
  background: #bbb;
}

.dark-mode .cancel:hover {
  background: #555;
}

/* Confirm Button - Using Existing Dashboard Accent */
.confirm {
  background: #e04350;
  color: white;
}

.confirm:hover {
  background: #ff7700;
}

/* Fade-in Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>