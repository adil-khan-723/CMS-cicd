<template>
  <div class="posts-wrapper" :class="{ 'dark-mode': props.isDarkMode }">
    <!-- Loading bar -->
    <div v-if="isLoading" class="loading-bar">
      <div class="loading-progress"></div>
    </div>

    <!-- Error message -->
    <div v-if="error" class="error-message">
      <i class="fas fa-exclamation-triangle"></i> {{ error }}
    </div>

    <!-- Success message -->
    <div v-if="showSuccess" class="success-message">
      <i class="fas fa-check-circle"></i> {{ successMessage }}
    </div>

    <!-- Header -->
    <div class="header-container">
      <h2 class="posts-title">{{ showAnonymous ? 'Anonymous Posts' : 'Your Posts' }}</h2>
      <div class="toggle-container">
        <span class="view-label">View By</span>
        <button @click="toggleView" class="toggle-btn">
          <i :class="viewMode === 0 ? 'fas fa-th-large' : 'fas fa-list'"></i>
        </button>
      </div>
    </div>

    <!-- Posts container -->
    <div class="posts-container">
      <!-- No posts message -->
      <div v-if="!isLoading && filteredBlogs.length === 0" class="no-posts">
        <i class="far fa-newspaper"></i> No {{ showAnonymous ? 'anonymous' : '' }} posts available
      </div>

      <!-- Card View -->
      <div v-if="viewMode === 0" class="card-view">
        <div v-for="blog in filteredBlogs" :key="blog.id" class="post-card">
          <h3 class="post-title">{{ blog.title }}</h3>
          
          <!-- Post Meta - Show only in normal mode -->
          <div class="post-meta" v-if="!showAnonymous">
            <span v-if="blog.category" class="post-category">Category: {{ blog.category }}</span>
            <span class="post-author">Author: {{ blog.author || 'Unknown' }}</span>
          </div>
          
          <button class="read-more-btn" @click="openModal(blog.id)">
            <i class="fas fa-book-open"></i> Read More
          </button>
        </div>
      </div>

      <!-- List View -->
      <div v-if="viewMode === 2" class="list-view">
        <div v-for="blog in filteredBlogs" :key="blog.id" class="post-list-item">
          <div class="list-content">
            <h3 class="post-title">{{ blog.title }}</h3>
            
            <!-- Post Meta - Show only in normal mode -->
            <div class="post-meta" v-if="!showAnonymous">
              <span v-if="blog.category" class="post-category">
                <i class="fas fa-tag"></i> {{ blog.category }}
              </span>
              <span class="post-author">
                <i class="fas fa-user"></i> {{ blog.author || 'Unknown' }}
              </span>
            </div>
            
            <!-- Read More Button moved inside list-content -->
            <button class="read-more-btn" @click="openModal(blog.id)">
              <i class="fas fa-book-open"></i> Read More
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Search Box -->
    <div class="search-container">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search posts by title or content..." 
          class="search-input"
          @keyup.enter="searchPosts"
        />
        <button @click="searchPosts" class="search-button">
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="expandedPost !== null" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content" v-if="currentPost">
        <button class="close-btn" @click="closeModal">&times;</button>
        <div class="modal-header">
          <h2 class="modal-title">{{ currentPost.title }}</h2>
          <div class="modal-meta">
            <p v-if="!showAnonymous"><i class="fas fa-user"></i> <strong>{{ currentPost.author || 'Unknown Author' }}</strong></p>
            <p><i class="fas fa-tag"></i> <strong>{{ currentPost.category || 'Uncategorized' }}</strong></p>
            <p><i class="far fa-calendar-alt"></i> <strong>{{ formatDate(currentPost.created_at) }}</strong></p>
          </div>
        </div>
        <div class="modal-body">
          <p>{{ currentPost.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, watch } from 'vue';
import { ref, onMounted, computed } from "vue";
import api from "@/api.js";
import '@fortawesome/fontawesome-free/css/all.min.css';

const props = defineProps({
  isDarkMode: {
    type: Boolean,
    default: false
  },
  showAnonymous: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update-posts']);

// State management
const blogs = ref([]);
const expandedPost = ref(null);
const viewMode = ref(0);
const searchQuery = ref('');
const isLoading = ref(false);
const error = ref(null);
const showSuccess = ref(false);
const successMessage = ref('');

// Format date for display
const formatDate = (dateString) => {
  if (!dateString) return 'Unknown date';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

// Watch for changes in showAnonymous prop
watch(() => props.showAnonymous, (newVal) => {
  fetchBlogs(newVal);
});

// Computed properties
const filteredBlogs = computed(() => {
  if (!searchQuery.value) return blogs.value;
  const query = searchQuery.value.toLowerCase();
  return blogs.value.filter(blog => 
    (blog.title && blog.title.toLowerCase().includes(query)) ||
    (!props.showAnonymous && blog.author && blog.author.toLowerCase().includes(query)) ||
    (blog.content && blog.content.toLowerCase().includes(query)) ||
    (blog.category && blog.category.toLowerCase().includes(query))
  );
});

const currentPost = computed(() => {
  return expandedPost.value !== null ? 
    blogs.value.find(blog => blog.id === expandedPost.value) : 
    null;
});

// Fetch blogs from the appropriate API endpoint
const fetchBlogs = async (showAnonymous = false) => {
  isLoading.value = true;
  error.value = null;
  
  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No authentication token found");

    const endpoint = showAnonymous ? "posts/" : "blogposts/";

    const response = await api.get(endpoint, {
      headers: { Authorization: `Bearer ${token}` },
    });

    blogs.value = response.data.map(post => ({
      id: post.id,
      title: post.title || 'Untitled Post',
      author: post.author || post.user?.username || 'Unknown',
      category: post.category || 'Uncategorized',
      content: post.content || post.body || '',
      created_at: post.created_at || post.date || null,
      is_anonymous: post.is_anonymous || false,
      ...post
    }));

    emit('update-posts', blogs.value);

    if (blogs.value.length === 0) {
      error.value = `No ${showAnonymous ? 'anonymous' : ''} posts found`;
    } else {
      showSuccess.value = true;
      successMessage.value = `${blogs.value.length} ${showAnonymous ? 'anonymous' : ''} posts loaded`;
      setTimeout(() => showSuccess.value = false, 3000);
    }
  } catch (err) {
    console.error("Error fetching posts:", err);
    error.value = err.response?.data?.detail || 
                 err.message || 
                 "Failed to load posts. Please try again later.";
  } finally {
    isLoading.value = false;
  }
};

// View methods
const openModal = (blogId) => {
  expandedPost.value = blogId;
  document.body.style.overflow = 'hidden';
};

const closeModal = () => {
  expandedPost.value = null;
  document.body.style.overflow = '';
};

const searchPosts = () => {
  // Handled by computed property
};

const toggleView = () => {
  viewMode.value = viewMode.value === 0 ? 2 : 0;
};

// Initialize
onMounted(() => {
  fetchBlogs(props.showAnonymous);
});
</script>

<style scoped>
/* Loading bar styles */
.loading-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #f0f0f0;
  z-index: 1000;
  overflow: hidden;
}

.loading-progress {
  height: 100%;
  width: 0;
  background-color: #ff6600;
  animation: loading 1.5s ease-in-out infinite;
}

@keyframes loading {
  0% {
    width: 0;
    transform: translateX(0);
  }
  50% {
    width: 80%;
    transform: translateX(0);
  }
  100% {
    width: 100%;
    transform: translateX(100%);
  }
}

.dark-mode .loading-bar {
  background-color: #2d2d2d;
}

.dark-mode .loading-progress {
  background-color: #ff8c00;
}

/* Base styles */
.posts-wrapper {
  margin-top: 20px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  height: 80vh;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: relative;
}

.posts-wrapper.dark-mode {
  background: #1e1e1e;
  color: #e0e0e0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* Message styles */
.error-message {
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #f8d7da;
  color: #721c24;
}

.success-message {
  padding: 10px 15px;
  margin: 10px 0;
  background: #d4edda;
  color: #155724;
  border-radius: 5px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dark-mode .error-message {
  background: #3c0a0d;
  color: #ff6b6b;
}

.dark-mode .success-message {
  background: #1a3a1f;
  color: #7dff9d;
}

/* Header */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.posts-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: inherit;
  margin: 0;
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.view-label {
  font-size: 0.9rem;
  color: #666;
}

.dark-mode .view-label {
  color: #aaa;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-btn:hover {
  background: rgba(255, 102, 0, 0.1);
}

.toggle-btn i {
  font-size: 1.2rem;
  color: #ff6600;
}

.dark-mode .toggle-btn i {
  color: #ff8c00;
}

/* Posts Container */
.posts-container {
  overflow-y: auto;
  flex-grow: 1;
  margin-bottom: 15px;
  padding-right: 5px;
}

/* Scrollbar */
.posts-container::-webkit-scrollbar {
  width: 8px;
}

.posts-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.dark-mode .posts-container::-webkit-scrollbar-track {
  background: #2d2d2d;
}

.posts-container::-webkit-scrollbar-thumb {
  background: #ff6600;
  border-radius: 4px;
}

.dark-mode .posts-container::-webkit-scrollbar-thumb {
  background: #ff8c00;
}

.posts-container::-webkit-scrollbar-thumb:hover {
  background: #e55a00;
}

.dark-mode .posts-container::-webkit-scrollbar-thumb:hover {
  background: #ff7700;
}

/* Card View */
.card-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 5px;
}

.post-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.dark-mode .post-card {
  background: #2d2d2d;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
}

/* Post Meta */
.post-meta {
  margin: 8px 0;
  font-size: 0.9em;
  color: #666;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.post-meta i {
  margin-right: 5px;
  width: 15px;
  text-align: center;
}

.post-category,
.post-author {
  display: flex;
  align-items: center;
}

.dark-mode .post-meta {
  color: #aaa;
}

/* Read More Button */
.read-more-btn {
  background: #ff6600;
  color: white;
  border: none;
  padding: 10px 18px; /* Slightly larger padding */
  border-radius: 6px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px; /* Added margin top */
  width: fit-content; /* Only take needed width */
  align-self: flex-start; /* Align to start */
}

.read-more-btn:hover {
  background: #e55a00;
  transform: translateY(-2px);
}

.read-more-btn i {
  font-size: 0.9rem;
}

/* List View */
.list-view {
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 5px;
}

.post-list-item {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column; /* Changed to column layout */
}

.list-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px; /* Added gap between elements */
}

.dark-mode .post-list-item {
  background: #2d2d2d;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

/* Search Container */
.search-container {
  display: flex;
  justify-content: center;
  padding: 15px 0;
}

.search-box {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 30px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.dark-mode .search-box {
  background: #2d2d2d;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
}

.search-input {
  flex: 1;
  padding: 12px 20px;
  border: none;
  outline: none;
  font-size: 1rem;
  background: transparent;
}

.dark-mode .search-input {
  color: #e0e0e0;
}

.search-input::placeholder {
  color: #aaa;
}

.dark-mode .search-input::placeholder {
  color: #888;
}

.search-button {
  background: #ff6600;
  color: white;
  border: none;
  padding: 12px 20px;
  cursor: pointer;
}

.search-button:hover {
  background: #e55a00;
}

.search-button i {
  font-size: 1rem;
}

/* No Posts Message */
.no-posts {
  color: #888;
  font-style: italic;
  text-align: center;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.no-posts i {
  font-size: 2rem;
  opacity: 0.5;
}

.dark-mode .no-posts {
  color: #aaa;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  width: 60%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.2);
}

.dark-mode .modal-content {
  background-color: #2d2d2d;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.4);
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #ff6600;
  font-weight: bold;
  position: absolute;
  top: 15px;
  right: 20px;
  padding: 0;
  margin: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #e55a00;
}

.modal-header {
  margin-top: 20px;
  margin-bottom: 20px;
  padding-right: 30px;
}

.modal-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

.dark-mode .modal-title {
  color: #f0f0f0;
}

.modal-meta {
  margin: 10px 0;
  font-size: 0.95em;
  color: #555;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.modal-meta p {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.modal-meta i {
  font-size: 0.9em;
  width: 20px;
  text-align: center;
}

.dark-mode .modal-meta {
  color: #aaa;
}

.modal-body {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.7;
  white-space: pre-line;
}

.dark-mode .modal-body {
  color: #ddd;
}

/* Responsive Design */
@media (max-width: 992px) {
  .modal-content {
    width: 75%;
  }
}

@media (max-width: 768px) {
  .modal-content {
    width: 90%;
    padding: 20px;
  }
  
  .card-view {
    grid-template-columns: 1fr;
  }

  .header-container {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .modal-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 576px) {
  .posts-wrapper {
    padding: 15px;
    height: 85vh;
  }

  .post-list-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .read-more-btn {
    width: 100%;
  }

  .modal-header {
    margin-top: 10px;
  }
}
</style>