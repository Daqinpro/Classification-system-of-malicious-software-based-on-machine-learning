import Vue from 'vue'
import axios from "axios"
import router from '../../router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import { jwtDecode } from 'jwt-decode';

Vue.use(ElementUI);

axios.defaults.withCredentials = false;
// 类型Join 格式  字符utf-8
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8';

// 请求拦截器
axios.interceptors.request.use(config => {
  config.headers.Authorization = window.sessionStorage.getItem('token');
  return config;
}, error => {
  return Promise.reject(error);
});

// 响应拦截器
axios.interceptors.response.use(response => {
  if (response.status === 200) {
    if (response.data.status === 5005) {
      ElementUI.Message({
        message: "token验证失败，请重新登录验证！",
        type: 'warning'
      });
      router.push('/');
      return Promise.reject(response.data); // 拒绝当前请求，防止继续执行后续逻辑
    }
    return response;
  } else {
    return Promise.reject(response);
  }
}, error => {
  if (error.response) {
    switch (error.response.status) {
      case 401:
        ElementUI.Message({
          message: "Token过期，请重新登录！",
          type: 'warning'
        });
        router.push('/');
        break;
      default:
        ElementUI.Message({
          message: error.response.data.message || '请求失败',
          type: 'warning'
        });
    }
  } else {
    ElementUI.Message({
      message: '网络连接错误，请检查您的网络设置！',
      type: 'error'
    });
  }
  return Promise.reject(error);
});

export default axios;
