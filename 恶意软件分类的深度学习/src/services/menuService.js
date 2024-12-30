// src/services/menuService.js
import axios from 'axios';

export const menuService = {
  getMenus(id) {
    return axios.get('menu/get_menus', {
      params: {
        id: id
      }
    }).then(res => {
      if (res.data.code == 200) {
        return res.data.data;
      }
      return [];
    });
  }
};
