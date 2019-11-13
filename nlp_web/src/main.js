// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Apexchart from 'vue-apexcharts'
import axios from 'axios'
import VueSpinners from 'vue-spinners'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);

Vue.use(VueSpinners)

Vue.prototype.$axios = axios
Vue.config.productionTip = false
Vue.use(Apexchart);
Vue.component('apexchart', Apexchart)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
