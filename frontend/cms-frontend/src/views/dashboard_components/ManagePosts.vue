<template>
  <div class="posts-wrapper" :class="{ 'dark-mode': props.isDarkMode }">
    <!-- Loading and Error States -->
    <div v-if="isLoading" class="loading-message">
      <i class="fas fa-spinner fa-spin"></i> Loading posts...
    </div>
    <div v-if="error" class="error-message">
      <i class="fas fa-exclamation-triangle"></i> {{ error }}
    </div>

    <!-- Success Message -->
    <div v-if="showSuccess" class="success-message">
      <i class="fas fa-check-circle"></i> Post updated successfully!
    </div>

    <!-- Heading and Toggle Button -->
    <div class="header-container">
      <h2 class="posts-title">Manage Posts</h2>
      <div class="toggle-container">
        <span class="view-label">View By</span>
        <button @click="toggleView" class="toggle-btn">
          <i :class="viewMode === 0 ? 'fas fa-th-large' : 'fas fa-list'"></i>
        </button>
      </div>
    </div>

    <!-- Message when no blogs are available -->
    <div v-if="!isLoading && filteredBlogs.length === 0" class="no-posts">
      <i class="far fa-newspaper"></i> No blogs available
    </div>

    <!-- Posts Container (scrollable) -->
    <div class="posts-container">
      <!-- Card View -->
      <div v-if="viewMode === 0" class="card-view">
        <div v-for="blog in filteredBlogs" :key="blog.id" class="post-card">
          <h3 class="post-title">{{ blog.title }}</h3>
          <div class="post-meta" v-if="!blog.is_anonymous && !props.showAnonymous">
            <span v-if="blog.category" class="post-category">Category: {{ blog.category }}</span>
            <span class="post-author">Author: {{ blog.author }}</span>
          </div>
          <div class="action-buttons">
            <button class="read-more-btn" @click="openModal(blog.id)">Read More</button>
            <button class="edit-btn" @click="startEditing(blog.id)" v-if="!props.showAnonymous && !blog.is_anonymous">
              Edit
            </button>
            <button class="delete-btn" @click="confirmDelete(blog.id)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-if="viewMode === 2" class="list-view">
        <div v-for="blog in filteredBlogs" :key="blog.id" class="post-list-item">
          <div class="post-content">
            <h3 class="post-title">{{ blog.title }}</h3>
            <div class="post-meta" v-if="!blog.is_anonymous && !props.showAnonymous">
              <span v-if="blog.category" class="post-category">Category: {{ blog.category }}</span>
              <span class="post-author">Author: {{ blog.author }}</span>
            </div>
          </div>
          <div class="action-buttons">
            <button class="read-more-btn" @click="openModal(blog.id)">Read More</button>
            <button class="edit-btn" @click="startEditing(blog.id)" v-if="!props.showAnonymous && !blog.is_anonymous">
              Edit
            </button>
            <button class="delete-btn" @click="confirmDelete(blog.id)">
              <i class="fas fa-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Search Box -->
    <div class="search-container">
      <div class="search-box">
        <input type="text" v-model="searchQuery" placeholder="Search posts by title or content..." class="search-input"
          @keyup.enter="searchPosts" />
        <button @click="searchPosts" class="search-button">
          <i class="fas fa-search"></i>
        </button>
      </div>
    </div>

    <!-- View Modal -->
    <div :class="['modal-overlay', { active: currentPostId !== null }]" @click.self="closeModal">
      <div class="modal-content" v-if="currentPost">
        <button class="close-btn" @click="closeModal">&times;</button>
        <div class="modal-header">
          <h2 class="modal-title">{{ currentPost.title }}</h2>
          <div class="modal-meta" v-if="!currentPost.is_anonymous && !props.showAnonymous">
            <span v-if="currentPost.category" class="modal-category">Category: {{ currentPost.category }}</span>
            <span class="modal-author">Author: {{ currentPost.author }}</span>
          </div>
        </div>
        <div class="modal-body">
          <p>{{ currentPost.content }}</p>
        </div>
      </div>
    </div>

    <!-- Edit Modal (only accessible in normal mode) -->
    <div :class="['edit-modal-overlay', { active: editingPost !== null && !props.showAnonymous }]"
      @click.self="cancelEditing">
      <div class="edit-modal-content" v-if="editingPost && !props.showAnonymous">
        <button class="close-btn" @click="cancelEditing">&times;</button>
        <div class="modal-header">
          <h2>Edit Post</h2>
          <p class="post-type-label" v-if="!props.showAnonymous">(Normal Post)</p>
        </div>

        <!-- Error Message -->
        <div v-if="editError" class="error-message">
          <i class="fas fa-exclamation-triangle"></i> {{ editError }}
        </div>

        <div class="input-group">
          <label>Title</label>
          <input type="text" v-model="editingPost.title" />
        </div>

        <div class="input-group">
          <label>Content</label>
          <textarea v-model="editingPost.content" rows="10"></textarea>
        </div>

        <div class="input-group" v-if="!props.showAnonymous">
          <label>Category</label>
          <input type="text" v-model="editingPost.category" />
        </div>

        <div class="input-group" v-if="!props.showAnonymous">
          <label>Author</label>
          <input type="text" v-model="editingPost.author" />
        </div>

        <div class="button-group">
          <button class="cancel" @click="cancelEditing" :disabled="isSaving">
            Cancel
          </button>
          <button class="save" @click="savePost" :disabled="isSaving">
            <span v-if="!isSaving">Save Changes</span>
            <span v-else><i class="fas fa-spinner fa-spin"></i> Saving...</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div :class="['delete-modal-overlay', { active: showDeleteModal }]" @click.self="cancelDelete">
      <div class="delete-modal-content">
        <div class="modal-header">
          <h2>Confirm Deletion</h2>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this post? This action cannot be undone.</p>
        </div>
        <div class="button-group">
          <button class="cancel" @click="cancelDelete">Cancel</button>
          <button class="delete-confirm" @click="deletePost">Delete</button>
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

// State
const blogs = ref([]);
const currentPostId = ref(null);
const editingPost = ref(null);
const viewMode = ref(0);
const searchQuery = ref('');
const isLoading = ref(false);
const isSaving = ref(false);
const error = ref(null);
const editError = ref(null);
const showSuccess = ref(false);
const showDeleteModal = ref(false);
const postToDelete = ref(null);

// Computed
const filteredBlogs = computed(() => {
  if (!searchQuery.value) return blogs.value;
  const query = searchQuery.value.toLowerCase();
  return blogs.value.filter(blog =>
    (blog.title && blog.title.toLowerCase().includes(query)) ||
    (blog.content && blog.content.toLowerCase().includes(query)) ||
    (!blog.is_anonymous && !props.showAnonymous && blog.category && blog.category.toLowerCase().includes(query)) ||
    (!blog.is_anonymous && !props.showAnonymous && blog.author && blog.author.toLowerCase().includes(query))
  );
});

const currentPost = computed(() => {
  return blogs.value.find(blog => blog.id === currentPostId.value);
});

// Fetch blogs from appropriate endpoint
const fetchBlogs = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("No authentication token found");

    const endpoint = props.showAnonymous
      ? "posts/"
      : "blogposts/";

    const response = await api.get(endpoint, {
      headers: { Authorization: `Bearer ${token}` },
    });

    blogs.value = response.data.map(post => ({
      id: post.id,
      title: post.title || 'Untitled Post',
      author: props.showAnonymous ? '' : (post.is_anonymous ? '' : (post.author || post.user?.username || 'Unknown')),
      category: props.showAnonymous ? '' : (post.is_anonymous ? '' : (post.category || 'Uncategorized')),
      content: post.content || post.body || '',
      is_anonymous: post.is_anonymous || false,
      ...post
    }));

    emit('update-posts', blogs.value);

    if (blogs.value.length === 0) {
      error.value = `No ${props.showAnonymous ? 'anonymous' : ''} posts found`;
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

// Watch for changes in showAnonymous prop
watch(() => props.showAnonymous, () => {
  fetchBlogs();
});

// Modal functions
const openModal = (postId) => {
  currentPostId.value = postId;
  document.body.style.overflow = 'hidden';
};

const closeModal = () => {
  currentPostId.value = null;
  document.body.style.overflow = '';
};

// Edit functions (only available in normal mode)
const startEditing = (postId) => {
  if (props.showAnonymous) return; // Don't allow editing in anonymous mode

  const post = blogs.value.find(p => p.id === postId);
  if (post && !post.is_anonymous) {
    editingPost.value = {
      ...post,
      category: props.showAnonymous ? '' : (post.category || ''),
      author: props.showAnonymous ? '' : (post.author || post.user?.username || 'Unknown')
    };
    document.body.style.overflow = 'hidden';
  }
};

const cancelEditing = () => {
  editingPost.value = null;
  editError.value = null;
  document.body.style.overflow = '';
};

const savePost = async () => {
  if (!editingPost.value || props.showAnonymous) return;

  if (!editingPost.value.title?.trim()) {
    editError.value = "Title is required";
    return;
  }

  isSaving.value = true;
  editError.value = null;

  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Authentication required");

    const requestData = {
      title: editingPost.value.title,
      content: editingPost.value.content,
      category: props.showAnonymous ? '' : (editingPost.value.category || ''),
      author: props.showAnonymous ? '' : (editingPost.value.author || ''),
      is_anonymous: false
    };

    const endpoint = `blogposts/${editingPost.value.id}/`;

    const response = await api.put(
      endpoint,
      requestData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    // Update local state
    const index = blogs.value.findIndex(p => p.id === editingPost.value.id);
    if (index !== -1) {
      blogs.value[index] = {
        ...blogs.value[index],
        title: response.data.title,
        content: response.data.content,
        category: props.showAnonymous ? '' : (response.data.category || editingPost.value.category),
        author: props.showAnonymous ? '' : (response.data.author || editingPost.value.author)
      };
    }

    showSuccess.value = true;
    setTimeout(() => showSuccess.value = false, 3000);
    editingPost.value = null;
    document.body.style.overflow = '';

  } catch (err) {
    console.error("Error updating post:", err);
    editError.value = err.response?.data?.detail ||
      err.message ||
      "Failed to update post. Please try again.";
  } finally {
    isSaving.value = false;
  }
};

// Delete functions
const confirmDelete = (postId) => {
  postToDelete.value = postId;
  showDeleteModal.value = true;
  document.body.style.overflow = 'hidden';
};

const cancelDelete = () => {
  postToDelete.value = null;
  showDeleteModal.value = false;
  document.body.style.overflow = '';
};

const deletePost = async () => {
  if (!postToDelete.value) return;

  try {
    const token = localStorage.getItem("access_token");
    if (!token) throw new Error("Authentication required");

    // Find the post to determine its type
    const post = blogs.value.find(p => p.id === postToDelete.value);
    if (!post) throw new Error("Post not found");

    // Use the correct endpoint based on current view mode (showAnonymous)
    const endpoint = props.showAnonymous
      ? `posts/${postToDelete.value}/`
      : `blogposts/${postToDelete.value}/`;

    await api.delete(endpoint, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Remove the deleted post from the local state
    blogs.value = blogs.value.filter(post => post.id !== postToDelete.value);
    showSuccess.value = true;
    setTimeout(() => showSuccess.value = false, 3000);
  } catch (err) {
    console.error("Error deleting post:", err);
    error.value = err.response?.data?.detail ||
      err.message ||
      "Failed to delete post. Please try again.";
  } finally {
    cancelDelete();
  }
};

// UI functions
const toggleView = () => {
  viewMode.value = viewMode.value === 0 ? 2 : 0;
};

const searchPosts = () => {
  // Handled by computed property
};

// Initialize
onMounted(() => {
  fetchBlogs();
});
</script>

<style scoped>
.posts-wrapper {
  margin-top: 20px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  height: 80vh;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.posts-wrapper.dark-mode {
  background: #1e1e1e;
  color: #e0e0e0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* Header */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-shrink: 0;
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
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background: rgba(255, 102, 0, 0.1);
  transform: scale(1.1);
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
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
}

.dark-mode .post-card {
  background: #2d2d2d;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
}

.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.dark-mode .post-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.4);
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
  padding: 15px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-content {
  flex: 1;
}

.dark-mode .post-list-item {
  background: #2d2d2d;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.post-list-item:hover {
  transform: translateX(3px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.dark-mode .post-list-item:hover {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.4);
}

/* Title Styling */
.post-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
  word-break: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 3em;
  line-height: 1.5em;
}

.dark-mode .post-title {
  color: #f0f0f0;
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

.post-category,
.post-author {
  display: block;
}

.dark-mode .post-meta {
  color: #aaa;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.read-more-btn,
.edit-btn,
.delete-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.read-more-btn {
  background: #ff6600;
  color: white;
}

.edit-btn {
  background: #ffa500;
  color: white;
}

.delete-btn {
  background: #dc3545;
  color: white;
  padding: 8px 12px;
}

.read-more-btn:hover {
  background: #e55a00;
  transform: scale(1.05);
}

.edit-btn:hover {
  background: #e69500;
  transform: scale(1.05);
}

.delete-btn:hover {
  background: #c82333;
  transform: scale(1.05);
}

/* Search Container */
.search-container {
  display: flex;
  justify-content: center;
  padding: 15px 0;
  flex-shrink: 0;
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
  transition: all 0.3s ease;
}

.dark-mode .search-box {
  background: #2d2d2d;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
}

.search-box:focus-within {
  box-shadow: 0 5px 15px rgba(255, 102, 0, 0.2);
  transform: scale(1.01);
}

.dark-mode .search-box:focus-within {
  box-shadow: 0 5px 15px rgba(255, 140, 0, 0.3);
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
  transition: all 0.3s ease;
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
.modal-overlay,
.edit-modal-overlay,
.delete-modal-overlay {
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
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.modal-overlay.active,
.edit-modal-overlay.active,
.delete-modal-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

.modal-content,
.edit-modal-content,
.delete-modal-content {
  position: relative;
  background-color: #fff;
  padding: 30px;
  border-radius: 12px;
  width: 60%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  transform: scale(0.95);
  opacity: 0;
  transition: all 0.3s ease;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.2);
}

.dark-mode .modal-content,
.dark-mode .edit-modal-content,
.dark-mode .delete-modal-content {
  background-color: #2d2d2d;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.4);
}

.modal-overlay.active .modal-content,
.edit-modal-overlay.active .edit-modal-content,
.delete-modal-overlay.active .delete-modal-content {
  transform: scale(1);
  opacity: 1;
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
  transition: all 0.3s ease;
}

.close-btn:hover {
  color: #e55a00;
  transform: scale(1.1);
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
}

.modal-category,
.modal-author {
  display: block;
  margin: 5px 0;
}

.post-type-label {
  font-size: 0.9em;
  color: #666;
  margin-top: 5px;
  font-style: italic;
}

.dark-mode .post-type-label {
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

/* Edit Modal Specific */
.edit-modal-content {
  width: 80%;
  max-width: 800px;
}

.delete-modal-content {
  width: 80%;
  max-width: 500px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.dark-mode .input-group label {
  color: #e0e0e0;
}

.input-group input,
.input-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.dark-mode .input-group input,
.dark-mode .input-group textarea {
  background-color: #3d3d3d;
  border-color: #4d4d4d;
  color: #f0f0f0;
}

.input-group textarea {
  min-height: 200px;
  resize: vertical;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.button-group button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.button-group .cancel {
  background: #ccc;
  color: #333;
}

.dark-mode .button-group .cancel {
  background: #555;
  color: #e0e0e0;
}

.button-group .save {
  background: #ff6600;
  color: white;
}

.button-group .delete-confirm {
  background: #dc3545;
  color: white;
}

.button-group .cancel:hover {
  background: #bbb;
}

.dark-mode .button-group .cancel:hover {
  background: #666;
}

.button-group .save:hover {
  background: #e55a00;
}

.button-group .delete-confirm:hover {
  background: #c82333;
}

/* Loading and Error Messages */
.loading-message,
.error-message {
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.loading-message {
  background: #fff3cd;
  color: #856404;
}

.error-message {
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

.dark-mode .loading-message {
  background: #332701;
  color: #ffd700;
}

.dark-mode .error-message {
  background: #3c0a0d;
  color: #ff6b6b;
}

.dark-mode .success-message {
  background: #1a3a1f;
  color: #7dff9d;
}

/* Responsive Design */
@media (max-width: 992px) {

  .modal-content,
  .edit-modal-content,
  .delete-modal-content {
    width: 75%;
  }
}

@media (max-width: 768px) {

  .modal-content,
  .edit-modal-content,
  .delete-modal-content {
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

  .action-buttons {
    flex-direction: column;
    width: 100%;
  }

  .read-more-btn,
  .edit-btn {
    width: 100%;
  }

  .modal-header {
    margin-top: 10px;
  }
}
</style>