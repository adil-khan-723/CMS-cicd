<template>
  <div class="auth-container">
    <div class="background-pattern"></div>
    <div class="site-logo">blooog</div>
    <div class="auth-content">
      <!-- Left Panel - Ultra Enhanced Visual Section -->
      <div class="visual-panel">
        <!-- Background Elements -->
        <div class="visual-overlay"></div>
        <div class="gradient-mesh"></div>
        <!-- Main Content -->
        <div class="quote-container">
          <transition name="quote-fade" mode="out-in">
            <div :key="currentQuote.text">
              <div class="quote-mark">"</div>
              <h1 class="quote-text">{{ currentQuote.text }}</h1>
              <div class="quote-author">
                <div class="author-line"></div>
                <span>{{ currentQuote.author }}</span>
              </div>
            </div>
          </transition>
        </div>
        <!-- Decorative Elements -->
        <div class="floating-abstract-shapes">
          <div class="abstract-shape shape-1"></div>
          <div class="abstract-shape shape-2"></div>
          <div class="abstract-shape shape-3"></div>
        </div>
        <div class="ink-elements">
          <div class="ink-splatter splat-1"></div>
          <div class="ink-splatter splat-2"></div>
          <div class="ink-drip"></div>
        </div>
        <div class="floating-pens">
          <div class="pen-icon">
            <svg viewBox="0 0 24 24">
              <path fill="rgba(255,255,255,0.15)"
                d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
            </svg>
          </div>
        </div>
        <div class="corner-elements">
          <div class="corner-line line-1"></div>
          <div class="corner-line line-2"></div>
          <div class="corner-dot"></div>
        </div>
        <div class="floating-words">
          <span class="word-1">create</span>
          <span class="word-2">inspire</span>
          <span class="word-3">share</span>
        </div>
      </div>
      <!-- Right Panel - Login Form -->
      <div class="form-panel">
        <div class="form-container">
          <div class="form-header">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="logo-icon">
              <path fill="#FF6B35"
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
            </svg>
            <h2>Welcome Back</h2>
            <p>Sign in to access your content</p>
          </div>
          <form @submit.prevent="handleAuth" class="auth-form">
            <div class="input-group">
              <input type="text" v-model="username" placeholder=" " required @blur="checkUserOnBlur" />
              <label>Username</label>
            </div>
            <div class="input-group">
              <input type="password" v-model="password" placeholder=" " required />
              <label>Password</label>
            </div>
            <!-- Forgot Password Link -->
            <div class="forgot-password-container">
              <a href="#" @click.prevent="showForgotPassword = true">Forgot Password?</a>
            </div>
            <button type="submit" class="auth-button">
              {{ buttonText }}
            </button>
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>
          </form>
        </div>
      </div>
    </div>
    <!-- Forgot Password Modal -->
    <div v-if="showForgotPassword" class="forgot-password-modal">
      <div class="forgot-password-card">
        <button class="close-button" @click="closeForgotPassword">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <div class="card-header">
          <h3>Reset Password</h3>
          <p>Enter your username to reset your password</p>
        </div>
        <div v-if="!usernameExists" class="username-check">
          <div class="input-group">
            <input type="text" v-model="forgotUsername" placeholder=" " required />
            <label>Username</label>
          </div>
          <button @click="checkUsername" class="auth-button">
            Check Username
          </button>
          <div v-if="forgotError" class="error-message">
            {{ forgotError }}
          </div>
        </div>
        <div v-if="usernameExists" class="password-reset">
          <div class="input-group">
            <input type="password" v-model="newPassword" placeholder=" " required />
            <label>New Password</label>
          </div>
          <div class="input-group">
            <input type="password" v-model="confirmPassword" placeholder=" " required />
            <label>Confirm Password</label>
          </div>
          <button @click="resetForgotPassword" class="auth-button">
            Reset Password
          </button>
          <div v-if="resetSuccess" class="success-message">
            Password reset successfully! You can now login with your new password.
          </div>
          <div v-if="forgotError" class="error-message">
            {{ forgotError }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { loginUser, signupUser, checkUserExists, getUserProfile, resetPassword as resetPasswordApi } from "@/api";
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      username: "",
      password: "",
      isExistingUser: null,
      errorMessage: "",
      currentQuote: {
        text: "My unmatched perspicacity, coupled with my sheer indefatigability, makes me a feared opponent in any realm of human endeavor",
        author: "Andrew Tate"
      },
      quoteInterval: null,
      quotes: [
        { text: "My unmatched perspicacity, coupled with my sheer indefatigability, makes me a feared opponent in any realm of human endeavor", author: "Andrew Tate" },
        { text: "Writing is the painting of the voice", author: "Voltaire" },
        { text: "The art of writing is the art of discovering what you believe", author: "Gustave Flaubert" },
        { text: "Start writing, no matter what. The water does not flow until the faucet is turned on", author: "Louis L'Amour" },
        { text: "We write to taste life twice, in the moment and in retrospect", author: "Anaïs Nin" },
        { text: "A writer is someone for whom writing is more difficult than it is for other people", author: "Thomas Mann" },
        { text: "Fill your paper with the breathings of your heart", author: "William Wordsworth" },
        { text: "There is no greater agony than bearing an untold story inside you", author: "Maya Angelou" },
        { text: "You can make anything by writing", author: "C.S. Lewis" },
        { text: "Writing is the only way I have to explain my own life to myself", author: "Pat Conroy" },
        { text: "A word after a word after a word is power", author: "Margaret Atwood" },
        { text: "The role of a writer is not to say what we all can say, but what we are unable to say", author: "Anaïs Nin" },
        { text: "Write what should not be forgotten", author: "Isabel Allende" },
        { text: "Writing is an exploration. You start from nothing and learn as you go", author: "E.L. Doctorow" },
        { text: "To survive, you must tell stories", author: "Umberto Eco" },
        { text: "Writing is really a way of thinking—not just feeling but thinking about things that are disparate, unresolved, mysterious, problematic or just sweet", author: "Toni Morrison" },
        { text: "The scariest moment is always just before you start", author: "Stephen King" },
        { text: "A blog is only as interesting as the interest shown in others", author: "Lee Odden" },
        { text: "Blogging is a conversation, not a code", author: "Mike Butcher" },
        { text: "Every great blog begins with a single post", author: "Unknown" },
        { text: "Content is the reason search began in the first place", author: "Lee Odden" },
        { text: "Blogging is like work, but without coworkers thwarting you at every turn", author: "Scott Adams" },
        { text: "Creativity is intelligence having fun", author: "Albert Einstein" },
        { text: "The world always seems brighter when you've just made something that wasn't there before", author: "Neil Gaiman" },
        { text: "Art enables us to find ourselves and lose ourselves at the same time", author: "Thomas Merton" },
        { text: "Every artist was first an amateur", author: "Ralph Waldo Emerson" },
        { text: "Creativity takes courage", author: "Henri Matisse" },
        { text: "Art is not what you see, but what you make others see", author: "Edgar Degas" },
        { text: "The desire to create is one of the deepest yearnings of the human soul", author: "Dieter F. Uchtdorf" },
        { text: "To practice any art, no matter how well or badly, is a way to make your soul grow", author: "Kurt Vonnegut" },
        { text: "Art washes away from the soul the dust of everyday life", author: "Pablo Picasso" },
        { text: "Creativity is contagious, pass it on", author: "Albert Einstein" },
        { text: "The artist's world is limitless. It can be found anywhere, far from where he lives or a few feet away", author: "Paul Strand" },
        { text: "A blog is not a diary. It's a conversation with the world", author: "Unknown" },
        { text: "Write what disturbs you, what you fear, what you have not been willing to speak about", author: "Natalie Goldberg" },
        { text: "The difference between the almost right word and the right word is the difference between the lightning bug and the lightning", author: "Mark Twain" },
        { text: "One day I will find the right words, and they will be simple", author: "Jack Kerouac" },
        { text: "Either write something worth reading or do something worth writing", author: "Benjamin Franklin" },
        { text: "You never have to change anything you got up in the middle of the night to write", author: "Saul Bellow" },
        { text: "A writer is a world trapped in a person", author: "Victor Hugo" },
        { text: "Words are a lens to focus one's mind", author: "Ayn Rand" },
        { text: "The first draft is just you telling yourself the story", author: "Terry Pratchett" },
        { text: "Write hard and clear about what hurts", author: "Ernest Hemingway" },
        { text: "The purpose of a writer is to keep civilization from destroying itself", author: "Albert Camus" },
        { text: "A word is not the same with one writer as with another. One tears it from his guts. The other pulls it out of his overcoat pocket", author: "Charles Peguy" },
        { text: "Writing is an act of faith, not a trick of grammar", author: "E.B. White" }
      ],
      lastQuoteIndex: 0,
      showForgotPassword: false,
      forgotUsername: '',
      newPassword: '',
      confirmPassword: '',
      usernameExists: false,
      forgotError: '',
      resetSuccess: false
    };
  },
  computed: {
    buttonText() {
      if (this.isExistingUser === null) return "Continue";
      return this.isExistingUser ? "Sign In" : "Create Account";
    }
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  created() {
    setTimeout(() => {
      this.getRandomQuote();
      this.quoteInterval = setInterval(this.getRandomQuote, 5000);
    }, 5000);
  },
  beforeUnmount() {
    clearInterval(this.quoteInterval);
  },
  methods: {
    getRandomQuote() {
      let randomIndex;
      do {
        randomIndex = Math.floor(Math.random() * this.quotes.length);
      } while (randomIndex === this.lastQuoteIndex && this.quotes.length > 1);
      this.lastQuoteIndex = randomIndex;
      this.currentQuote = this.quotes[randomIndex];
    },
    async checkUserOnBlur() {
      if (!this.username) {
        this.isExistingUser = false;
        return;
      }
      try {
        const response = await checkUserExists(this.username);
        this.isExistingUser = response.exists;
      } catch (error) {
        console.error("Error checking user:", error);
        this.isExistingUser = false;
      }
    },
    async handleAuth() {
      this.errorMessage = "";
      if (!this.username) {
        this.errorMessage = "Please enter a username.";
        return;
      }
      if (this.isExistingUser === null) {
        await this.checkUserOnBlur();
      }
      if (this.isExistingUser) {
        await this.login();
      } else {
        await this.signup();
      }
    },
    async login() {
      try {
        const response = await loginUser(this.username, this.password);
        if (response.token) {
          localStorage.setItem("access_token", response.token);
          await this.fetchUserProfile();
        } else {
          this.errorMessage = "Invalid credentials. Please try again.";
        }
      } catch (error) {
        this.errorMessage = "Invalid credentials. Please try again.";
      }
    },
    async signup() {
      try {
        const response = await signupUser(this.username, this.password);
        if (response.success) {
          localStorage.setItem("access_token", response.token);
          await this.fetchUserProfile();
        } else {
          this.errorMessage = "Signup failed. Please try again.";
        }
      } catch (error) {
        this.errorMessage = "Signup failed. Please try again.";
      }
    },
    async fetchUserProfile() {
      try {
        const response = await getUserProfile();
        if (response.username) {
          localStorage.setItem("username", response.username);
          this.router.push("/dashboard");
        } else {
          this.errorMessage = "Error retrieving user profile.";
        }
      } catch (error) {
        console.error("Profile fetch error:", error);
      }
    },
    async checkUsername() {
      if (!this.forgotUsername) {
        this.forgotError = "Please enter a username.";
        return;
      }
      try {
        const response = await checkUserExists(this.forgotUsername);
        this.usernameExists = response.exists;
        if (!response.exists) {
          this.forgotError = "Username not found.";
        } else {
          this.forgotError = "";
        }
      } catch (error) {
        console.error("Error checking username:", error);
        this.forgotError = "Error checking username. Please try again.";
      }
    },
    async resetForgotPassword() {
      if (!this.newPassword || !this.confirmPassword) {
        this.forgotError = "Please enter and confirm your new password.";
        return;
      }
      if (this.newPassword !== this.confirmPassword) {
        this.forgotError = "Passwords do not match.";
        return;
      }
      try {
        const response = await resetPasswordApi(this.forgotUsername, this.newPassword);
        if (response.success) {
          this.resetSuccess = true;
          this.forgotError = "";

          // Redirect to the login page after a short delay
          setTimeout(() => {
            this.closeForgotPassword(); // Close the modal
            this.router.push("/login"); // Redirect to the login page
          }, 3000);
        } else {
          this.forgotError = response.message || "Password reset failed.";
        }
      } catch (error) {
        console.error("Error resetting password:", error);
        this.forgotError = "Error resetting password. Please try again.";
      }
    },
    closeForgotPassword() {
      this.showForgotPassword = false; // Hide the modal
      this.forgotUsername = '';       // Clear username field
      this.newPassword = '';          // Clear new password field
      this.confirmPassword = '';      // Clear confirm password field
      this.usernameExists = false;    // Reset username existence check
      this.forgotError = '';          // Clear error messages
      this.resetSuccess = false;      // Clear success flag
    }
  }
};
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');

/* Base Styles */
.auth-container {
  display: flex;
  min-height: 100vh;
  background-color: #f8f9fa;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}

.site-logo {
  position: absolute;
  top: 30px;
  right: 40px;
  font-family: 'Inter', sans-serif;
  font-size: 34px;
  font-weight: 1000;
  letter-spacing: 2px;
  color: #FF6B35;
  z-index: 10;
}

.background-pattern {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: radial-gradient(#e0e0e0 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.4;
  z-index: 0;
}

.auth-content {
  display: flex;
  width: 100%;
  min-height: 100vh;
  z-index: 1;
}

/* Enhanced Visual Panel */
.visual-panel {
  flex: 1;
  background: linear-gradient(135deg, #FF6B35 0%, #E55627 100%);
  padding: 4rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.visual-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect fill="none" width="100" height="100"/><path fill="rgba(255,255,255,0.03)" d="M30,30 Q50,10 70,30 T90,50 Q70,70 50,90 T10,50 Q30,30 50,10 T90,50"/></svg>');
  background-size: 60px 60px;
  opacity: 0.4;
}

.gradient-mesh {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background:
    radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.05) 0%, transparent 20%),
    radial-gradient(circle at 80% 70%, rgba(255, 255, 255, 0.05) 0%, transparent 20%);
  z-index: 0;
}

/* Quote Container */
.quote-container {
  max-width: 500px;
  margin: 0 auto;
  color: white;
  position: relative;
  z-index: 2;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  min-height: 300px;
}

.quote-mark {
  font-size: 6rem;
  line-height: 1;
  color: rgba(255, 255, 255, 0.15);
  position: absolute;
  top: -1.5rem;
  left: -1rem;
  font-family: 'Playfair Display', serif;
}

.quote-text {
  font-size: 2.5rem;
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: 2rem;
  position: relative;
  font-family: 'Playfair Display', serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  min-height: 120px;
  display: flex;
  align-items: center;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-line {
  width: 50px;
  height: 2px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 100%);
}

.quote-author span {
  font-size: 1.1rem;
  letter-spacing: 0.1em;
  color: rgba(255, 255, 255, 0.9);
  font-family: 'Inter', sans-serif;
  font-weight: 500;
}

/* Quote Transition Animation */
.quote-fade-enter-active,
.quote-fade-leave-active {
  transition: all 0.8s ease;
}

.quote-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.quote-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.quote-fade-enter-to,
.quote-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* Abstract Shapes - Enhanced visibility and movement */
.floating-abstract-shapes {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}

.abstract-shape {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(2px);
  animation: float 15s ease-in-out infinite;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.shape-1 {
  width: 250px;
  height: 250px;
  top: 10%;
  right: 5%;
  animation-delay: 0s;
}

.shape-2 {
  width: 180px;
  height: 180px;
  bottom: 10%;
  left: 5%;
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  animation-delay: 3s;
}

.shape-3 {
  width: 120px;
  height: 120px;
  top: 60%;
  right: 20%;
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  animation-delay: 6s;
}

/* Ink Elements - Enhanced visibility and movement */
.ink-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}

.ink-splatter {
  position: absolute;
  background-size: contain;
  background-repeat: no-repeat;
  opacity: 0.12;
  filter: blur(0.8px);
}

.splat-1 {
  width: 200px;
  height: 200px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><path fill="rgba(0,0,0,0.2)" d="M50,30c10-25,40-25,50,0c15,30-10,60,0,90c10,30,40,20,40,40c0,20-40,10-60,0S30,135,30,105C30,75,40,55,50,30z"/></svg>');
  top: 10%;
  left: 5%;
  animation: float 20s linear infinite reverse;
}

.splat-2 {
  width: 150px;
  height: 150px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><path fill="rgba(0,0,0,0.2)" d="M100,30c25,0,40,25,40,50c0,25-15,50-30,70c-15,20-30,40-10,50c20,10,40-20,50-10c10,10-10,30-30,20s-30-30-40-50C70,120,50,90,50,60C50,30,75,30,100,30z"/></svg>');
  bottom: 10%;
  right: 5%;
  animation: float 25s linear infinite;
}

.ink-drip {
  position: absolute;
  width: 80px;
  height: 120px;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 120"><path fill="rgba(0,0,0,0.12)" d="M40,0c10,0,20,10,20,20c0,20-20,40-20,60c0,20-20,40-20,60c0,20,10,20,20,20s20-10,20-20c0-10-10-20-10-30c0-10,10-20,10-30C60,30,40,10,40,0z"/></svg>');
  top: 70%;
  left: 15%;
  animation: float 12s ease-in-out infinite;
}

/* Floating Pens - Enhanced visibility */
.floating-pens {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 2;
}

.pen-icon {
  position: absolute;
  width: 40px;
  height: 40px;
  animation: float 15s ease-in-out infinite;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.pen-icon:nth-child(1) {
  top: 30%;
  left: 15%;
  animation-delay: 2s;
}

/* Corner Elements - Enhanced visibility */
.corner-elements {
  position: absolute;
  width: 100px;
  height: 100px;
  bottom: 30px;
  right: 30px;
  z-index: 2;
}

.corner-line {
  position: absolute;
  background: rgba(255, 255, 255, 0.25);
}

.line-1 {
  width: 60px;
  height: 1px;
  bottom: 0;
  right: 0;
}

.line-2 {
  width: 1px;
  height: 60px;
  bottom: 0;
  right: 0;
}

.corner-dot {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  bottom: -4px;
  right: -4px;
}

/* Floating Words - Enhanced visibility and movement */
.floating-words {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}

.floating-words span {
  position: absolute;
  font-family: 'Playfair Display', serif;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.15);
  font-size: 1.5rem;
  animation: float 25s linear infinite;
}

.word-1 {
  top: 20%;
  right: 10%;
  animation-delay: 0s;
}

.word-2 {
  top: 60%;
  left: 10%;
  animation-delay: 8s;
}

.word-3 {
  top: 40%;
  right: 20%;
  animation-delay: 16s;
}

/* Enhanced Animations */
@keyframes float {

  0%,
  100% {
    transform: translate(0, 0) rotate(0deg);
  }

  20% {
    transform: translate(15px, 20px) rotate(3deg);
  }

  40% {
    transform: translate(30px, 10px) rotate(-5deg);
  }

  60% {
    transform: translate(10px, 25px) rotate(7deg);
  }

  80% {
    transform: translate(-10px, 15px) rotate(-3deg);
  }
}

/* Form Panel */
.form-panel {
  width: 450px;
  background-color: white;
  display: flex;
  align-items: center;
  padding: 2rem;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.05);
}

.form-container {
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
}

.form-header {
  text-align: center;
  margin-bottom: 3rem;
}

.logo-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1.5rem;
}

.form-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: #6b7280;
  font-size: 0.9375rem;
}

/* Form Elements */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.input-group {
  position: relative;
  margin-bottom: 1.5rem;
}

.input-group input {
  width: 100%;
  padding: 12px 0;
  border: none;
  border-bottom: 1px solid #e5e7eb;
  font-size: 1rem;
  background: transparent;
  transition: all 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-bottom-color: #FF6B35;
}

.input-group label {
  position: absolute;
  left: 0;
  top: 12px;
  color: #9ca3af;
  font-size: 1rem;
  transition: all 0.3s ease;
  pointer-events: none;
}

.input-group input:focus+label,
.input-group input:not(:placeholder-shown)+label {
  transform: translateY(-24px) scale(0.85);
  color: #FF6B35;
}

.auth-button {
  width: 100%;
  padding: 1rem;
  background-color: #FF6B35;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.auth-button:hover {
  background-color: #E55627;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 107, 53, 0.3);
}

.error-message {
  color: #e74c3c;
  font-size: 0.875rem;
  text-align: center;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background-color: #FFF1EB;
  border-radius: 6px;
}

/* Forgot Password Styles */
.forgot-password-container {
  text-align: right;
  margin-top: -1rem;
  margin-bottom: 1rem;
}

.forgot-password-container a {
  color: #FF6B35;
  font-size: 0.875rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password-container a:hover {
  color: #E55627;
}

/* Forgot Password Modal Styles */
.forgot-password-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.forgot-password-card {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  position: relative;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  color: #6b7280;
  transition: color 0.2s;
}

.close-button:hover {
  color: #FF6B35;
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.card-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
}

.card-header p {
  color: #6b7280;
  font-size: 0.9375rem;
}

.username-check,
.password-reset {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.success-message {
  color: #10B981;
  font-size: 0.875rem;
  text-align: center;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background-color: #ECFDF5;
  border-radius: 6px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .visual-panel {
    display: none;
  }

  .form-panel {
    width: 100%;
    justify-content: center;
  }

  .site-logo {
    top: 20px;
    right: 20px;
  }
}

@media (max-width: 480px) {
  .forgot-password-card {
    width: 90%;
    padding: 1.5rem;
  }
}

/* Page Transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.5s ease;
}

.page-enter,
.page-leave-to {
  opacity: 0;
}
</style>