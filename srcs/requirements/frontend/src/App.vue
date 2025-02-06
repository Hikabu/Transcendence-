<template>
  <!-- Navigation -->
  <nav>
    <router-link to="/">Login</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link v-if="isAuthenticated" to="/game">Game</router-link>
    <a v-else class="disabled-link">Game</a>
    <template v-if="isAuthenticated">
      | <button @click="handleLogout">Logout</button>
    </template>
  </nav>

  <!-- Game view with overlays -->
  <div class="game-container">
    <div class="no-cursor-overlay" :class="{ 'no-cursor-overlay_active': isCursorDisabled }"></div>
    <div class="grain-overlay"></div>
    <main class="main">
      <section class="container">
        <Menu
          :is-open="isMenuOpen"
          @on-close="closeMenu"
          @on-menu-option-select="handleMenuOptionSelect"
        />
        <Game :settings="gameSettings" @on-close-menu="closeMenu" />
      </section>
    </main>
  </div>

  <!-- Optional: additional routed content -->
  <main class="layout">
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

import { Game, Menu } from 'features';
import { provideGameSocket } from 'features/Game/composables/useGameSocket.js';
import {
  QUICK_START_GAME_MODE,
  QUICK_START_GAME_SETTINGS,
} from 'features/Game/config/constants.js';
import { MENU_ITEMS_KEYS } from 'features/Menu/config/constants.js';
import { i18n } from './main.js';
import { provideLang } from './shared/composables';

// Provide language and game socket connection.
provideLang(i18n);
provideGameSocket(import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/pong/');

/* ========= Game logic ========= */
const isCursorDisabled = ref(false);
const isMenuOpen = ref(true);
const gameSettings = ref(undefined);

let lastMousePosition = { x: 0, y: 0 };
let isTrackingMouse = false;
const closeMenuTimeoutId = ref(null);

const disableCursor = () => {
  isCursorDisabled.value = true;
};

const enableCursor = () => {
  isCursorDisabled.value = false;
};

const enableCursorOnMouseTravel = (event) => {
  if (!lastMousePosition.x) {
    lastMousePosition.x = event.clientX;
    return;
  }
  if (!lastMousePosition.y) {
    lastMousePosition.y = event.clientY;
    return;
  }
  const distanceThreshold = 10 * 10; // squared threshold distance
  const dx = event.clientX - lastMousePosition.x;
  const dy = event.clientY - lastMousePosition.y;
  const squaredDistance = dx * dx + dy * dy;
  if (squaredDistance >= distanceThreshold) {
    enableCursor();
    window.removeEventListener('mousemove', enableCursorOnMouseTravel);
    isTrackingMouse = false;
  }
};

const startMouseTracking = (event) => {
  if (!isTrackingMouse) {
    lastMousePosition = { x: event.clientX, y: event.clientY };
    window.addEventListener('mousemove', enableCursorOnMouseTravel);
    isTrackingMouse = true;
  }
};

const closeMenu = (delay) => {
  const close = () => {
    isMenuOpen.value = false;
  };
  if (delay && typeof delay === 'number') {
    closeMenuTimeoutId.value = setTimeout(close, delay);
  } else {
    close();
  }
};

const handleMenuOptionSelect = (optionKey) => {
  if (optionKey === MENU_ITEMS_KEYS.QUICK_START) {
    gameSettings.value = QUICK_START_GAME_SETTINGS;
    closeMenu(500);
  }
};

const handleKeyDown = (event) => {
  startMouseTracking(event);
  disableCursor();

  if (event.code === 'Escape') {
    if (gameSettings.value && gameSettings.value.mode === QUICK_START_GAME_MODE) {
      gameSettings.value = undefined;
    }
    isMenuOpen.value = !isMenuOpen.value;
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
  if (closeMenuTimeoutId.value) {
    clearTimeout(closeMenuTimeoutId.value);
  }
});

/* ========= Authentication logic ========= */
const router = useRouter();
const isAuthenticated = ref(false);

const checkAuthStatus = async () => {
  try {
    const response = await axios.get('/api/auth-status/');
    isAuthenticated.value = response.data.isAuthenticated;
    console.log('Auth status checked');
  } catch (error) {
    isAuthenticated.value = false;
  }
};

checkAuthStatus();

const handleLogout = async () => {
  try {
    await axios.post('/api/logout/');
    isAuthenticated.value = false;
    router.push('/');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
</script>

<style scoped>
/* ----- Game Related Styles ----- */
@keyframes noise {
  0% {
    transform: translate3d(0, 9rem, 0);
  }
  10% {
    transform: translate3d(-1rem, -4rem, 0);
  }
  20% {
    transform: translate3d(-8rem, 2rem, 0);
  }
  30% {
    transform: translate3d(9rem, -9rem, 0);
  }
  40% {
    transform: translate3d(-2rem, 7rem, 0);
  }
  50% {
    transform: translate3d(-9rem, -4rem, 0);
  }
  60% {
    transform: translate3d(2rem, 6rem, 0);
  }
  70% {
    transform: translate3d(7rem, -8rem, 0);
  }
  80% {
    transform: translate3d(-9rem, 1rem, 0);
  }
  90% {
    transform: translate3d(6rem, -5rem, 0);
  }
  100% {
    transform: translate3d(-7rem, 0, 0);
  }
}

.no-cursor-overlay {
  pointer-events: none;
  cursor: none;
  position: absolute;
  z-index: 900;
  display: none;
  width: 100%;
  height: 100%;
}

.no-cursor-overlay_active {
  pointer-events: all;
}

.grain-overlay {
  pointer-events: none;
  position: fixed;
  z-index: 900;
  top: 0;
  left: 0;
  transform: translateZ(0);
  width: 100%;
  height: 100%;
}

.grain-overlay::before {
  pointer-events: none;
  content: '';
  position: fixed;
  z-index: 9999;
  top: -10rem;
  left: -10rem;
  width: calc(100% + 20rem);
  height: calc(100% + 20rem);
  opacity: 0.15;
  background-image: url('https://upload.wikimedia.org/wikipedia/commons/5/5c/Image_gaussian_noise_example.png');
  animation: noise 1s steps(2) infinite;
}

.main {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, var(--dark-color) 50%, var(--light-color) 50%);
}

.container {
  position: relative;
  aspect-ratio: 4 / 3;
  height: 90%;
  border-radius: 12px;
}

.game-container {
  position: relative;
}

/* ----- Layout and Navigation Styles ----- */
.layout {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

nav {
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

nav a {
  text-decoration: none;
  color: #007bff;
  margin: 0 0.5rem;
  transition: color 0.3s ease;
}

nav a:hover {
  color: #0056b3;
  text-decoration: underline;
}

.disabled-link {
  color: #6c757d;
  cursor: not-allowed;
  margin: 0 0.5rem;
}

button {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background: #bb2d3b;
}
</style>
