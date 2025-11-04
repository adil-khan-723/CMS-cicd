<template>
  <div class="post-creator">
    <!-- Header Section -->
    <div class="creator-header">
      <div class="logo" @click="$router.push('/')">blooog</div>
      <div class="header-actions">
        <button 
          class="publish-btn" 
          @click="publishPost" 
          :disabled="publishing"
          v-if="showEditor"
        >
          <svg class="icon" viewBox="0 0 24 24"><path d="M5 4v2h14V4H5zm0 10h4v6h6v-6h4l-7-7-7 7z"/></svg>
          <span v-if="publishing">Publishing...</span>
          <span v-else>Publish</span>
        </button>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="creator-content">
      <transition name="slide-fade" mode="out-in">
        <!-- First Page: Post Details -->
        <div v-if="!showEditor" class="post-details" key="form">
          <h1>Create New Post</h1>
          
          <div class="form-group">
            <label>Post Title</label>
            <input 
              v-model="post.title" 
              placeholder="Your amazing post title..."
              :class="{ 'error-input': errors.title }"
            >
            <span v-if="errors.title" class="error-text">Please enter a title</span>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Category</label>
              <div class="custom-select">
                <select v-model="post.category" :class="{ 'error-input': errors.category }">
                  <option value="" disabled selected>Select category</option>
                  <option value="Technology">Technology</option>
                  <option value="Design">Design</option>
                  <option value="Business">Business</option>
                  <option value="Lifestyle">Lifestyle</option>
                </select>
                <div class="select-arrow"></div>
              </div>
              <span v-if="errors.category" class="error-text">Please select a category</span>
            </div>

            <div class="form-group">
              <label>Author</label>
              <input 
                v-model="post.author" 
                placeholder="Your name"
                :class="{ 'error-input': errors.author }"
              >
              <span v-if="errors.author" class="error-text">Please enter your name</span>
            </div>
          </div>

          <div class="form-buttons">
            <button class="cancel-btn" @click="cancel">
              <svg class="icon" viewBox="0 0 24 24"><path d="M19 6.4L17.6 5 12 10.6 6.4 5 5 6.4 10.6 12 5 17.6 6.4 19 12 13.4 17.6 19 19 17.6 13.4 12z"/></svg>
              Cancel
            </button>
            <button class="continue-btn" @click="validateAndContinue">
              Continue
              <svg class="icon" viewBox="0 0 24 24"><path d="M12 4l-1.4 1.4L16.2 11H4v2h12.2l-5.6 5.6L12 20l8-8z"/></svg>
            </button>
          </div>
        </div>

        <!-- Second Page: Editor -->
        <div v-else class="editor-viewport" key="editor">
          <div class="editor-container">
            <div class="editor-header">
              <h2>{{ post.title }}</h2>
              <div class="post-meta">
                <span class="author">{{ post.author }}</span>
                <span class="category">{{ post.category }}</span>
              </div>
            </div>

            <div class="quill-wrapper">
              <quillEditor 
                v-model:content="post.content" 
                :options="editorOptions"
                ref="editor"
              />
            </div>

            <div class="editor-buttons">
              <button class="back-btn" @click="showEditor = false">
                <svg class="icon" viewBox="0 0 24 24"><path d="M20 11H7.8l5.6-5.6L12 4l-8 8 8 8 1.4-1.4L7.8 13H20v-2z"/></svg>
                Back
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- Success Notification -->
    <transition name="fade-up">
      <div v-if="showSuccess" class="success-notice">
        <svg class="icon" viewBox="0 0 24 24"><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>
        Post published successfully!
      </div>
    </transition>
  </div>
</template>

<script>
import { quillEditor } from 'vue3-quill'
import 'quill/dist/quill.snow.css'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// Import Quill directly for module registration
import Quill from 'quill'

// Font whitelist configuration
const Font = Quill.import('formats/font')
Font.whitelist = [
  'arial', 
  'comic-sans', 
  'courier-new', 
  'georgia', 
  'helvetica', 
  'lucida', 
  'times-new-roman', 
  'verdana'
]
Quill.register(Font, true)

export default {
  components: {
    quillEditor
  },
  setup() {
    const router = useRouter()
    const showEditor = ref(false)
    const publishing = ref(false)
    const showSuccess = ref(false)
    const editor = ref(null)

    const post = ref({
      title: '',
      category: '',
      author: '',
      content: ''
    })

    const errors = ref({
      title: false,
      category: false,
      author: false
    })

    const editorOptions = {
      theme: 'snow',
      placeholder: 'Write your post content here...',
      modules: {
        toolbar: [
          [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
          [{ 'size': ['10px', '12px', '14px', '16px', '18px', '20px', '24px', '28px', '32px', '36px', false] }],
          [{ 'font': Font.whitelist }],
          ['bold', 'italic', 'underline', 'strike'],
          [{ 'color': [] }, { 'background': [] }],
          [{ 'script': 'sub'}, { 'script': 'super' }],
          [{ 'header': 1 }, { 'header': 2 }],
          [{ 'list': 'ordered'}, { 'list': 'bullet' }],
          [{ 'indent': '-1'}, { 'indent': '+1' }],
          [{ 'direction': 'rtl' }],
          [{ 'align': [] }],
          ['blockquote', 'code-block'],
          ['link', 'image', 'video'],
          ['formula'],
          ['clean']
        ]
      }
    }

    const validateAndContinue = () => {
      errors.value = {
        title: !post.value.title.trim(),
        category: !post.value.category.trim(),
        author: !post.value.author.trim()
      }

      if (!errors.value.title && !errors.value.category && !errors.value.author) {
        showEditor.value = true
      }
    }

    const publishPost = () => {
      publishing.value = true
      // Simulate API call
      setTimeout(() => {
        publishing.value = false
        showSuccess.value = true
        setTimeout(() => router.push('/dashboard'), 2000) // Changed from '/' to '/dashboard'
      }, 1500)
    }

    const cancel = () => {
      if (post.value.title || post.value.content) {
        if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
          router.push('/')
        }
      } else {
        router.push('/')
      }
    }

    return {
      post,
      errors,
      showEditor,
      publishing,
      showSuccess,
      editor,
      editorOptions,
      validateAndContinue,
      publishPost,
      cancel
    }
  }
}
</script>

<style scoped>
/* Base Styles */
.post-creator {
  min-height: 100vh;
  background-color: #121212;
  color: #e0e0e0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  display: flex;
  flex-direction: column;
}

/* Header Styles */
.creator-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background-color: #1e1e1e;
  border-bottom: 1px solid #333;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  font-size: 32px;
  font-weight: 800;
  color: #ff6600;
  cursor: pointer;
  font-family: 'Poppins', sans-serif;
  text-transform: lowercase;
  letter-spacing: 1px;
}

.logo:hover {
  opacity: 0.9;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* Icon Styles */
.icon {
  width: 18px;
  height: 18px;
  fill: currentColor;
  vertical-align: middle;
  margin-right: 8px;
}

/* Button Styles */
button {
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  font-size: 14px;
}

.publish-btn {
  background-color: #ff6600;
  color: white;
}

.publish-btn:hover:not(:disabled) {
  background-color: #e65c00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 102, 0, 0.2);
}

.publish-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Main Content */
.creator-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 30px auto;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
}

/* Post Details Form */
.post-details {
  background-color: #1e1e1e;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.post-details h1 {
  font-size: 28px;
  margin-bottom: 30px;
  font-weight: 700;
  color: white;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 500;
  color: #e0e0e0;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  background-color: #2a2a2a;
  border: 1px solid #333;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #ff6600;
  box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.2);
}

.error-input {
  border-color: #ff4757 !important;
}

.error-text {
  color: #ff4757;
  font-size: 14px;
  margin-top: 8px;
  display: block;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-row .form-group {
  flex: 1;
}

/* Custom Select */
.custom-select {
  position: relative;
}

.custom-select select {
  width: 100%;
  padding: 14px 16px;
  background-color: #2a2a2a;
  border: 1px solid #333;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  appearance: none;
  cursor: pointer;
}

.custom-select select:focus {
  outline: none;
  border-color: #ff6600;
  box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.2);
}

.select-arrow {
  position: absolute;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #e0e0e0;
  pointer-events: none;
}

/* Form Buttons */
.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 30px;
}

.cancel-btn {
  background-color: #2a2a2a;
  color: #e0e0e0;
  border: 1px solid #333;
}

.cancel-btn:hover {
  background-color: #333;
}

.continue-btn {
  background-color: #ff6600;
  color: white;
}

.continue-btn:hover {
  background-color: #e65c00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 102, 0, 0.2);
}

/* Editor Viewport */
.editor-viewport {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 180px);
  overflow: hidden;
}

.editor-container {
  background-color: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.editor-header {
  padding: 20px 30px;
  border-bottom: 1px solid #333;
  flex-shrink: 0;
}

.editor-header h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: white;
}

.post-meta {
  display: flex;
  gap: 16px;
  color: #e0e0e0;
  font-size: 14px;
}

.post-meta .category {
  background-color: #ff6600;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.quill-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 200px;
  overflow: hidden;
}

/* Quill Editor Customization with all tools */
.ql-container.ql-snow {
  border: none;
  background-color: #2a2a2a;
  color: white;
  flex: 1;
  display: flex;
  flex-direction: column;
  font-family: inherit;
}

.ql-editor {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  font-size: 16px;
  line-height: 1.6;
}

/* Enhanced Toolbar with all tools */
.ql-toolbar.ql-snow {
  border: none;
  border-bottom: 1px solid #333;
  background-color: #ffffff;
  padding: 8px;
  display: flex;
  flex-wrap: wrap;
}

.ql-snow .ql-stroke {
  stroke: #333;
}

.ql-snow .ql-fill {
  fill: #333;
}

.ql-snow .ql-picker {
  color: #333;
}

.ql-snow .ql-picker-options {
  background-color: #ffffff;
  border: 1px solid #ddd;
  color: #333;
}

/* Style all buttons in the toolbar */
.ql-snow .ql-toolbar button,
.ql-snow .ql-toolbar .ql-picker-label {
  background: white;
  border-radius: 4px;
  margin: 0 2px;
  padding: 3px 5px;
  height: 28px;
}

.ql-snow .ql-toolbar button:hover,
.ql-snow .ql-toolbar .ql-picker-label:hover {
  background: #f0f0f0;
}

.ql-snow .ql-toolbar button.ql-active {
  background: #e0e0e0;
}

/* Font size dropdown with pixel values */
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="10px"]::before {
  content: '10px';
  font-size: 10px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="12px"]::before {
  content: '12px';
  font-size: 12px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="14px"]::before {
  content: '14px';
  font-size: 14px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="16px"]::before {
  content: '16px';
  font-size: 16px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="18px"]::before {
  content: '18px';
  font-size: 18px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="20px"]::before {
  content: '20px';
  font-size: 20px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="24px"]::before {
  content: '24px';
  font-size: 24px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="28px"]::before {
  content: '28px';
  font-size: 28px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="32px"]::before {
  content: '32px';
  font-size: 32px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-item[data-value="36px"]::before {
  content: '36px';
  font-size: 36px !important;
}

.ql-snow .ql-picker.ql-size .ql-picker-label[data-value]::before,
.ql-snow .ql-picker.ql-size .ql-picker-item[data-value]::before {
  content: attr(data-value) !important;
}

/* Font family dropdown */
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="arial"]::before {
  content: 'Arial';
  font-family: 'Arial';
}

.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="comic-sans"]::before {
  content: 'Comic Sans';
  font-family: 'Comic Sans MS';
}

.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="courier-new"]::before {
  content: 'Courier New';
  font-family: 'Courier New';
}

.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="georgia"]::before {
  content: 'Georgia';
  font-family: 'Georgia';
}

.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="helvetica"]::before {
  content: 'Helvetica';
  font-family: 'Helvetica';
}

.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="lucida"]::before {
  content: 'Lucida';
  font-family: 'Lucida Console';
}

.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="times-new-roman"]::before {
  content: 'Times New Roman';
  font-family: 'Times New Roman';
}

.ql-snow .ql-picker.ql-font .ql-picker-item[data-value="verdana"]::before {
  content: 'Verdana';
  font-family: 'Verdana';
}

.ql-snow .ql-picker.ql-font .ql-picker-label[data-value]::before,
.ql-snow .ql-picker.ql-font .ql-picker-item[data-value]::before {
  content: attr(data-value) !important;
}

/* Success Notice */
.success-notice {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #1e1e1e;
  color: white;
  padding: 14px 24px;
  border-radius: 8px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1000;
  border: 1px solid #2ed573;
}

.success-notice .icon {
  fill: #2ed573;
}

/* Animations */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.5s ease;
}
.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}

/* Loading Spinner */
.publish-btn .icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .creator-header {
    padding: 16px;
    flex-direction: column;
    gap: 16px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .creator-content {
    padding: 0 16px;
  }
  
  .post-details {
    padding: 24px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
  
  .form-buttons {
    flex-direction: column;
  }
  
  button {
    width: 100%;
    justify-content: center;
  }
  
  .editor-header {
    padding: 16px;
  }
  
  .editor-buttons {
    padding: 16px;
  }
  
  /* Adjust toolbar for mobile */
  .ql-toolbar.ql-snow {
    padding: 4px;
  }
  
  .ql-snow .ql-toolbar button,
  .ql-snow .ql-toolbar .ql-picker-label {
    padding: 2px 3px;
    height: 24px;
    margin: 0 1px;
  }
}
</style>