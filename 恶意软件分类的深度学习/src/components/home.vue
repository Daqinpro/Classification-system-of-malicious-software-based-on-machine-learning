<template>
  <div class="box"
  v-loading="loading"
    element-loading-text="正在加载中"
    element-loading-spinner="el-icon-loading"
  >
    <div class="head">
      <div class="headTitle">
        <h1>恶意软件分类学习系统</h1>
      </div>
      <div class="nav">
        <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          background-color="#ffffff"
          text-color="#222222"
          active-text-color="#008EFF"
          unique-opened
          style="display: flex; height: 100%;"
        >
          <el-menu-item :index="item.path" v-for="item in menusData" :key="item.id" @click="handleMenuClick(item)">
            <i :class="item.icon"></i>
            <span slot="title">{{ item.name }}</span>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="loginOut">
        <el-button type="primary"@click="handleLogout">退出登录</el-button>
        <!-- <img src="../assets/home/退出.png" alt="退出" @click="handleLogout"/> -->
      </div>
    </div>
    <div class="main">
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { menuService } from '@/services/menuService';
export default {
  data() {
    return {
      loading: false,
      activeIndex: '',
      name: '',
      id: '',
      menusData: [],
    };
  },
  created() {
    this.id = JSON.parse(window.sessionStorage.getItem("currentUser")).id;
    this.activeIndex = this.$route.path;
    this.getMenus();
  },
  watch: {
    $route(to) {
      this.activeIndex = to.path;
    }
  },
  methods: {
    // 获取菜单
    getMenus() {
      this.loading=true;
      this.$axios.get('menu/get_menus', {
        params: {
          id: this.id
        }
      }).then(res => {
        if (res.data.code == 200) {
          this.loading=false;
          this.menusData = res.data.data;
        }
        else {
          this.loading=false;
          this.$message.error(res.data.msg);
        }
      })
    },
    // 处理菜单点击事件
    handleMenuClick(item) {
      if (this.activeIndex !== item.path) {
        this.activeIndex = item.path;
        this.$router.push(item.path);
      }
    },
    // 退出
    handleLogout() {
      window.sessionStorage.removeItem("token");
      window.sessionStorage.removeItem("currentUser");
      this.$router.push("/login");
    },
  }
}
</script>

<style scoped lang="less">
.box {
  width: 100%;
  height: 100%;
  user-select: none;
  .head {
    display: flex;
    align-items: center;
    width: 100%;
    height: 6.5%;
    .headTitle {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 30%;
      height: 100%;
      line-height: 100%;
      background-image: url('../assets/home/抬头.png');
      background-size: 100% 100%;
      background-position: center;
      background-repeat: no-repeat;
      h1 {
        color: #FFFFFF;
        font: normal 400 2vw "HuXiaoBo-NanShen";
      }
    }

    .nav {
      margin-left: 50px;
      height: 100%;
      margin-right: 80px;
      span {
        font: normal 20px "微软雅黑";
      }
    }

    .loginOut {
      display: flex;
      align-items: center;
      height: 100%;

      p {
        font-family: PingFang SC;
        font-weight: bold;
        font-size: 18px;
        color: #222222;
        margin-right: 27px;
        margin-left: 11px;
      }
      img {
        cursor: pointer;
      }
    }
  }

  .main {
    width: 100%;
    height: 93%;
    // background-color: #008EFF;
    .content {
      padding: 1% 1% 0 1%;
      height: 98%;
      overflow: hidden;
      // background-color: aqua;
    }
  }

  /deep/ .el-submenu__title {
    height: 100%;
    font-size: 16px;
    color: #222222;
    font-weight: bold;
    font-family: PingFang SC;
  }

}
</style>
