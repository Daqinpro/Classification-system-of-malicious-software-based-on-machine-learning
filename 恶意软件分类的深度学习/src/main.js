import Vue from "vue";
import App from "./App";
import router from "./router";

Vue.config.productionTip = false;

// md5
import md5 from "js-md5";
Vue.prototype.$md5 = md5;

// echarts
import echarts from "echarts";
Vue.prototype.$echarts = echarts;

// axios
import axios from "axios";
Vue.prototype.$axios = axios;
axios.defaults.baseURL = "http://jitsafe.be.kuaidi.icu:8803";
// 全局变量
Vue.prototype.droneUrl = "http://jitsafe.be.kuaidi.icu:8803";

import "../src/components/utils/hader";

// jwt
import { jwtDecode } from "jwt-decode";

// 全局设置用户信息参数
const token = window.sessionStorage.getItem("token");
if (typeof token === 'string' && token.length > 0) {
  Vue.prototype.user = jwtDecode(token);
} else {
  Vue.prototype.user = null; // 或者设置为默认值
}

new Vue({
  el: "#app",
  router,
  components: { App },
  template: "<App/>"
});
