import { createApp } from 'vue'
import App from './App.vue'
import tooltip from "./directives/tooltip.js";

const app = createApp(App);
app.config.globalProperties.$apiUrl = "xxx";
app.config.globalProperties.$url = "xxx";
app.directive("tooltip", tooltip);
app.mount('#app');
