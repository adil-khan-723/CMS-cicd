import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import '@/assets/styles.css';
import { checkUserExists } from "@/api";

window.checkUserExists = checkUserExists;
const originalWarn = console.warn;
console.warn = function(...args) {
  if (args[0]?.includes('DOMNodeInserted')) return;
  originalWarn.apply(console, args);
};

createApp(App).use(store).use(router).mount('#app')
