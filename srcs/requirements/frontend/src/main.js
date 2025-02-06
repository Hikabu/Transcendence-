import './style.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
// import { useAuthStore } from './store/auth'
import App from './App.vue'
import axios from 'axios' // http requests 
import router from './router'
import '@dzangolab/vue-country-flag-icon/dist/CountryFlag.css';
import './vendor/normalize.css';
import './vendor/fonts/lexend_exa/lexend_exa.css';
import './styles.css';
import './assets/styles/global.css';

import CountryFlag from '@dzangolab/vue-country-flag-icon';
import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';

import App from './App.vue';
import en from './locales/en.json';
import ru from './locales/ru.json';
import th from './locales/th.json';
import { svgComponents } from './shared/lib';

// axios.defaults.baseURL = 'http://127.0.0.1:80' // automatically prepend URL to the request path.

const app = createApp(App);

Object.entries(svgComponents).forEach(([name, component]) => {
  // noinspection JSCheckFunctionSignatures
  app.component(name, component);
});

app.component('CountryFlag', CountryFlag);

app.use(i18n);
app.mount('#app');
