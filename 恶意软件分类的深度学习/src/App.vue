<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style lang='less'>
* {
  margin: 0;
  padding: 0;
}
html,
body,
#app {
  width: 100%;
  height: 100%;
  font-family: "PingFang SC";
  z-index: 9999;
  user-select: none;
  // -webkit-filter: grayscale(100%);
}
li {
  list-style: none;
}
// 弹窗
.el-dialog__header {
  background: #3358ca;
  span {
    font-size: 0.95vw;
    color: white;
  }
  .el-dialog__headerbtn .el-dialog__close {
    color: white;
  }
}
.el-dialog__body {
  background: #f6f9fe;
}
.el-popover {
  min-width: 139px !important;
}
// 输入框
input::placeholder {
  color: rgb(122, 122, 122) !important;
  font-family: "PingFang SC";
}
// 地图标点弹窗
.amap-marker-label {
  padding: 5px;
  font-weight: bolder;
  color: #fff;
  border: none;
  border-radius: 5px;
  background: #3358ca;
}
// 隐藏高德logo
.amap-logo {
  display: none !important;
}
// 时间选择器
.el-date-range-picker {
  z-index: 10000 !important;
}
// 分页
.el-pagination.is-background .el-pager li {
  height: 30px;
  background: #fff;
  border: 1px solid rgb(226, 226, 226);
  &.active {
    background: #3358ca !important;
  }
}
.el-pagination .btn-prev {
  color: #606266 !important;
  background: #fff !important;
  border: 1px solid rgb(226, 226, 226) !important;
}
.el-pagination .btn-next {
  color: #606266 !important;
  background: #fff !important;
  border: 1px solid rgb(226, 226, 226) !important;
}
</style>
