<template>
    <div class="entrance-animation">
      <div class="animation-content">
        <!-- Title (keeping original colors) -->
        <h1 class="main-title">
          <span class="title-letter" 
                v-for="(letter, index) in titleLetters" 
                :key="index" 
                :style="letterStyle(index)">
            {{ letter }}
          </span>
        </h1>
        
        <!-- Subtitle (keeping original colors) -->
        <h2 class="subtitle" :class="{ 'visible': showSubtitle }">
          Where Every Word Tells a Story and Creativity Knows No Bounds!
        </h2>
        
        <!-- Progress Bar (keeping original colors) -->
        <div class="progress-container">
          <div class="progress-bar" :style="{ width: loadingProgress + '%' }"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
  import { useRouter } from 'vue-router'
  
  export default {
    name: 'EntranceAnimation',
    setup() {
      const router = useRouter()
      const title = ref("blooog") // Lowercase title
      const showSubtitle = ref(false)
      const loadingProgress = ref(0)
      let loadingInterval = null
  
      const titleLetters = computed(() => title.value.split(''))
  
      const letterStyle = (index) => ({
        animationDelay: `${index * 0.1}s`,
        '--hue-offset': index * 15 // Keeping original color variation
      })
  
      const startLoading = () => {
        const startTime = Date.now()
        const duration = 2500 // 2.5 seconds total
        
        loadingInterval = setInterval(() => {
          const elapsed = Date.now() - startTime
          loadingProgress.value = Math.min(100, (elapsed / duration) * 100)
          
          if (elapsed >= duration) {
            clearInterval(loadingInterval)
            router.push({ name: 'home' })
          }
        }, 16) // ~60fps
      }
  
      onMounted(() => {
        document.body.classList.add('entrance-active')
        
        setTimeout(() => {
          showSubtitle.value = true
        }, 800)
        
        startLoading()
      })
  
      onBeforeUnmount(() => {
        if (loadingInterval) clearInterval(loadingInterval)
        document.body.classList.remove('entrance-active')
      })
  
      return {
        titleLetters,
        showSubtitle,
        loadingProgress,
        letterStyle
      }
    }
  }
  </script>
  
  <style scoped>
  .entrance-animation {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white; /* ONLY CHANGE: White background */
    z-index: 1000;
  }
  
  .animation-content {
    text-align: center;
    padding: 2rem;
    max-width: 800px;
  }
  
  .main-title {
    font-size: 4.5rem; /* Original font size */
    font-weight: 700; /* Original weight */
    margin-bottom: 1.5rem;
    text-transform: lowercase; /* For lowercase rendering */
  }
  
  .title-letter {
    display: inline-block;
    opacity: 0;
    transform: translateY(20px);
    animation: letter-drop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    color: hsl(calc(20 + var(--hue-offset)), 100%, 65%); /* Original color scheme */
  }
  
  @keyframes letter-drop {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  
  .subtitle {
    font-size: 1.4rem; /* Original font size */
    font-weight: 300; /* Original weight */
    line-height: 1.6;
    color: rgba(0, 0, 0, 0.85); /* Slightly darker for white background */
    margin: 0 auto 2.5rem;
    max-width: 600px;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.8s cubic-bezier(0.215, 0.61, 0.355, 1) 0.3s;
  }
  
  .subtitle.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  .progress-container {
    width: 100%;
    max-width: 300px; /* Original width */
    height: 4px; /* Original height */
    background: rgba(0, 0, 0, 0.1); /* Lighter track for white bg */
    border-radius: 2px;
    margin: 0 auto;
    overflow: hidden;
  }
  
  .progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #ff6600, #ff8c00); /* Original gradient */
    border-radius: 2px;
    transition: width 0.1s linear;
  }
  
  /* Responsive Adjustments (original sizes) */
  @media (max-width: 768px) {
    .main-title {
      font-size: 3rem;
    }
    
    .subtitle {
      font-size: 1.1rem;
    }
    
    .progress-container {
      max-width: 200px;
    }
  }
  </style>
  
  <style>
  body.entrance-active {
    overflow: hidden;
  }
  </style>