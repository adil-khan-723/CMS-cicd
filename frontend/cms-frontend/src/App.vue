<template>
  <div id="app">
    <transition name="entrance" mode="out-in">
      <EntranceAnimation 
        v-if="showEntrance"
        aria-live="polite"
      />
    </transition>
    
    <transition name="fade" mode="out-in">
      <router-view v-if="!showEntrance" />
    </transition>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import EntranceAnimation from '@/views/EntranceAnimation.vue'

export default {
  name: 'App',
  components: { EntranceAnimation },
  setup() {
    const showEntrance = ref(!sessionStorage.getItem('hasSeenAnimation'))

    onMounted(() => {
      try {
        if (showEntrance.value) {
          document.body.classList.add('entrance-animation-active')
          sessionStorage.setItem('hasSeenAnimation', 'true')
          setTimeout(() => {
            showEntrance.value = false
            document.body.classList.remove('entrance-animation-active')
          }, 3500)
        }
      } catch (e) {
        console.error('Animation error:', e)
        showEntrance.value = false
      }
    })

    return { showEntrance }
  }
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 3s ease-in-out;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.entrance-leave-active {
  transition: all 0.8s cubic-bezier(0.19, 1, 0.22, 1);
}
.entrance-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

body.entrance-animation-active {
  overflow: hidden;
}
</style>