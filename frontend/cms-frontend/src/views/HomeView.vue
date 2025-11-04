<template>
  <div class="blogger-homepage">
    <!-- Header Section -->
    <header class="header" :class="{ 'scrolled': isScrolled }">
      <nav class="nav-container">
        <div class="logo-section">
          <a href="#" class="logo">blooog</a>
        </div>
        <div class="nav-links">
          <transition name="slide-fade">
            <button v-if="isScrolled" class="create-post-btn" @click="redirectToLogin">Create Blog</button>
          </transition>
          <button class="sign-in-btn" @click="redirectToLogin">Sign In/Sign Up</button>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <div class="hm">
      <section class="hero-section">
        <div class="hero-content">
          <h1 class="main-heading">Publish your passions, your way</h1>
          <p class="sub-heading">Create a unique and beautiful blog easily.</p>
          <button class="cta-button" @click="redirectToLogin">CREATE YOUR BLOG</button>
        </div>
      </section>
    </div>

    <!-- Additional Sections -->
    <div class="infoDiv1 info-div" data-animation="fade-up">
      <section class="info-section">
        <h2 class="info-heading">Choose the perfect design</h2>
        <p class="info-description">Create a beautiful blog that fits your style. Choose from a selection of easy-to-use templates.</p>
      </section>
    </div>

    <div class="infoDiv2 info-div" data-animation="fade-left">
      <section class="info-section">
        <h2 class="info-heading">Get a domain</h2>
        <p class="info-description">Give your blog the perfect home. Get a blogspot.com domain or buy a custom domain in just a few clicks.</p>
      </section>
    </div>

    <div class="infoDiv4 info-div" data-animation="fade-right">
      <section class="info-section">
        <h2 class="info-heading">Know your audience</h2>
        <p class="info-description">Find out which posts are a hit with Blogger's built-in analytics to understand your audience better.</p>
      </section>
    </div>

    <div class="infoDiv5 info-div" data-animation="fade-up">
      <section class="info-section">
        <h2 class="info-heading">Hang onto your memories</h2>
        <p class="info-description">Save the moments that matter. Blogger lets you store thousands of posts and photos securely.</p>
      </section>
    </div>

    <!-- Removed Animation for infoDiv6 -->
    <div class="infoDiv6 info-div">
      <section class="info-section">
        <h2 class="info-heading">Join millions of others</h2>
        <p class="info-description">Whether sharing expertise or breaking news, you're in good company on Blogger.</p>
        <button class="cta-button" @click="redirectToLogin">CREATE YOUR BLOG</button>
      </section>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  name: 'BloggerHomepage',
  data() {
    return {
      isScrolled: false,
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    this.observeInfoDivs();
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 0;
    },
    redirectToLogin() {
      this.router.push('/login');
    },
    observeInfoDivs() {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const animationType = entry.target.dataset.animation;
              if (animationType) {
                entry.target.classList.add('active', animationType);
              } else {
                entry.target.classList.add('active'); // For infoDiv6, no animation
              }
            }
          });
        },
        { threshold: 0.3 } // Trigger when 30% of the element is visible
      );

      document.querySelectorAll('.info-div').forEach((el) => observer.observe(el));
    }
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Arial', sans-serif;
}

/* Header Styles - Always Transparent */
.header {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: transparent !important;
  box-shadow: none !important;
  z-index: 1000;
  transition: all 0.3s ease;
}

/* Nav Container */
.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
}

/* Logo */
.logo {
  font-size: 2rem;
  font-weight: 800;
  color: #ff5722;
  text-decoration: none;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

/* Navigation Links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  position: relative;
}

/* Buttons */
.create-post-btn {
  background-color: #ff5722;
  color: white;
  border: none;
  padding: 0.8rem 1.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.sign-in-btn {
  color: white;
  background-color: #ff5722;
  border: 2px solid #ff5722;
  padding: 0.8rem 1.8rem;
  border-radius: 7px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  white-space: nowrap;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Button Hover Effects */
.create-post-btn:hover,
.sign-in-btn:hover {
  background-color: #e04a1c;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Scrolled State - Buttons Only */
.header.scrolled .create-post-btn {
  opacity: 1;
}

.header.scrolled .sign-in-btn {
  background-color: #ff5722;
  color: white;
}

/* Hero Section */
.hm {
  min-height: 100vh;
  background-image: url('@/assets/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding-top: 100px;
}

.hero-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: calc(100vh - 100px);
  padding: 0 2rem;
  animation: fadeInUp 1.5s ease-out;
}

.main-heading {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  color: white;
  line-height: 1.2;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 1.5s ease-out;
}

.sub-heading {
  font-size: 1.5rem;
  color: white;
  margin-bottom: 3rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  max-width: 700px;
  animation: fadeInUp 2s ease-out;
}

.cta-button {
  width: 300px;
  background-color: #ff5722;
  color: white;
  border: none;
  padding: 1.2rem 2.8rem;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  animation: fadeInUp 2.5s ease-out;
}

.cta-button:hover {
  background-color: #e04a1c;
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

/* Info Sections */
.info-div {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 1s ease, transform 1s ease;
}

.info-div.active.fade-up {
  opacity: 1;
  transform: translateY(0);
  animation: fadeUp 1s ease-out;
}

.info-div.active.fade-left {
  opacity: 1;
  transform: translateX(0);
  animation: fadeLeft 1s ease-out;
}

.info-div.active.fade-right {
  opacity: 1;
  transform: translateX(0);
  animation: fadeRight 1s ease-out;
}

.info-div.active {
  opacity: 1;
  transform: translateY(0); /* Default behavior for infoDiv6 */
}

.info-section {
  padding: 5rem 2rem;
  text-align: center;
}

.info-heading {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.info-description {
  font-size: 1.1rem;
  color: #555;
  margin: 0 auto 2rem;
  max-width: 800px;
  line-height: 1.6;
}

/* Background Divs with Visible Images */
.infoDiv1 {
  min-height: 70vh;
  background-image: url('@/assets/bg2.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  position: relative;
}

.infoDiv2 {
  min-height: 70vh;
  background-image: url('@/assets/bg3.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  position: relative;
}

.infoDiv4 {
  min-height: 70vh;
  background-image: url('@/assets/bg4.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  position: relative;
}

.infoDiv5 {
  min-height: 70vh;
  background-image: url('@/assets/bg5.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  position: relative;
}

.infoDiv6 {
  min-height: 70vh;
  background-image: url('@/assets/bg6.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  position: relative;
}

/* Text Alignment */
.infoDiv1 > section,
.infoDiv4 > section {
  margin-left: auto;
  text-align: right;
  margin-right: 5%;
}

.infoDiv2 > section,
.infoDiv5 > section {
  margin-right: auto;
  text-align: left;
  margin-left: 5%;
}

.infoDiv6 > section {
  margin: 0 auto;
  text-align: center;
}

/* Responsive Styles */
@media (max-width: 992px) {
  .nav-container {
    padding: 1.2rem;
  }

  .main-heading {
    font-size: 2.5rem;
  }

  .sub-heading {
    font-size: 1.3rem;
  }
}

@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
  }

  .logo {
    font-size: 1.8rem;
  }

  .nav-links {
    gap: 1rem;
  }

  .create-post-btn,
  .sign-in-btn {
    padding: 0.7rem 1.2rem;
    font-size: 0.9rem;
  }

  .hero-section {
    padding-top: 80px;
    height: calc(100vh - 80px);
  }

  .main-heading {
    font-size: 2rem;
  }

  .sub-heading {
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }

  .cta-button {
    width: 100%;
    max-width: 280px;
    padding: 1rem 2rem;
  }

  [class^="infoDiv"] > section {
    width: 90%;
    padding: 2rem;
    text-align: center !important;
    margin: 2rem auto !important;
  }

  .info-heading {
    font-size: 1.8rem;
  }

  .info-description {
    font-size: 1rem;
  }
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Transitions */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>