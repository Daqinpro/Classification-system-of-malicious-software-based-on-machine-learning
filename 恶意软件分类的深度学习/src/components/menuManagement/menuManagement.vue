<template>
  <div class="box"
    v-loading="loading"
    element-loading-text="正在加载中"
    element-loading-spinner="el-icon-loading"
  >

    <div class="table">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column type="index" label="序号" align="center"></el-table-column>
        <el-table-column prop="name" label="菜单名称" align="center"></el-table-column>
        <el-table-column prop="path" label="菜单路径" align="center"></el-table-column>
        <el-table-column prop="icon" label="图标" align="center">
          <template slot-scope="scope">
            <i :class="scope.row.icon"></i>
          </template>
        </el-table-column>
        <el-table-column prop="state" label="状态" align="center">
          <template slot-scope="scope">
            {{scope.row.state==1?'启用':'禁用'}}
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" align="center" width="200">
          <template slot-scope="scope">
            <div style="display: flex; justify-content: space-around;">
              <el-tag type="warning" @click="handleEdit(scope.row)">编辑</el-tag>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-size="pageSize"
        layout="total,prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </div>
    <el-drawer
      :title="title"
      :visible.sync="addDrawer"
      direction="rtl"
      :size="'30%'"
      :before-close="handleClose"
    >
      <div class="addDrawerView">
        <el-form :model="formData" :rules="rules" ref="drawerForm" class="demo-form-inline">
          <el-form-item label="菜单名称:"  prop="name">
            <el-input v-model="formData.name" placeholder="菜单名称" style="width: 40%;"></el-input>
          </el-form-item>
          <el-form-item label="菜单路径:"  prop="path" >
            <el-input v-model="formData.path" placeholder="菜单路径" :disabled="true" style="width: 40%;">
          </el-input>
          </el-form-item>
          <el-form-item label="图标选则:"  prop="icon">
            <el-select v-model="formData.icon" placeholder="请选择图标">
            <el-option
              v-for="icon in icons"
              :key="icon.value"
              :label="icon.label"
              :value="icon.value"
            >
              <span style="display: flex; align-items: center;">
                <i :class="icon.iconClass" style="margin-right: 8px;"></i>
                {{ icon.label }}
              </span>
            </el-option>
          </el-select>
          </el-form-item>
          <el-form-item label="状态选则:"  prop="state">
            <el-select v-model="formData.state" placeholder="请选择启用状态">
            <el-option label="启用" :value="1"></el-option>
            <el-option label="禁用" :value="0"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item style="display: flex; justify-content: center; margin-top: 10px;">
            <el-button type="primary" @click="submitData">提交</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { menuService } from '@/services/menuService';
export default {

  data() {
    return {
      icons: [
        { value: 'el-icon-edit', label: '编辑', iconClass: 'el-icon-edit' },
        { value: 'el-icon-share', label: '分享', iconClass: 'el-icon-share' },
        { value: 'el-icon-delete', label: '删除', iconClass: 'el-icon-delete' },
        { value: 'el-icon-setting', label: '设置', iconClass: 'el-icon-setting' },
        { value: 'el-icon-user', label: '用户', iconClass: 'el-icon-user' },
        { value: 'el-icon-message', label: '消息', iconClass: 'el-icon-message' },
        { value: 'el-icon-search', label: '搜索', iconClass: 'el-icon-search' },
        { value: 'el-icon-loading', label: '加载', iconClass: 'el-icon-loading' },
        { value: 'el-icon-success', label: '成功', iconClass: 'el-icon-success' },
        { value: 'el-icon-warning', label: '警告', iconClass: 'el-icon-warning' },
        { value: 'el-icon-error', label: '错误', iconClass: 'el-icon-error' },
        { value: 'el-icon-info', label: '信息', iconClass: 'el-icon-info' },
        { value: 'el-icon-date', label: '日期', iconClass: 'el-icon-date' },
        { value: 'el-icon-s-home', label: '首页', iconClass: 'el-icon-s-home' },
        { value: 'el-icon-s-custom', label: '用户', iconClass: 'el-icon-s-custom' },
        { value: 'el-icon-s-order', label: '订单', iconClass: 'el-icon-s-order' },
        { value: 'el-icon-s-tools', label: '工具', iconClass: 'el-icon-s-tools' },
        { value: 'el-icon-folder-checked', label: '文件夹', iconClass: 'el-icon-folder-checked' },
        { value: 'el-icon-edit-outline', label: '大纲', iconClass: 'el-icon-edit-outline' },
        { value: 'el-icon-s-management', label: '管理', iconClass: 'el-icon-s-management' },
        { value: 'el-icon-menu', label: '菜单', iconClass: 'el-icon-menu' },


        // 添加更多图标
      ],
      loading: false,
      editDatas: [],
      addDrawer: false,
      enditView: false,
      id: '',
      username:'',
      formData: {
        name:'',
        path:'',
        state:'',
        icon:''
      },
      rules: {
        name: [
          { required: true, message: '请输入菜单名称', trigger: 'blur' },
          { min: 2, max: 5, message: '长度在 2 到 5 个字符', trigger: 'blur' }
        ],
        path: [
          { required: true, message: '请输入路径', trigger: 'blur' }
        ],
        icon: [
          { required: true, message: '请选择图标', trigger: 'change' }
        ],
        state: [
          { required: true, message: '请选择启用状态', trigger: 'change' }
        ]
      },
      tableData: [], // 初始化为空数组
      currentPage: 1,
      pageSize: 12,
      total: 0, // 初始化为0
      title: ''
    }
  },
  created() {
    this.id = JSON.parse(window.sessionStorage.getItem("currentUser")).id;
    this.getData(); // 在组件创建时调用getData方法
  },
  methods: {

    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
          // this.getData(); // 刷新数据
          this.viewDrawer = false;
          this.enditView = false;
          this.formData={}
          this.$refs.drawerForm.resetFields(); // 重置表单字段

        })
        .catch(_ => {});
    },

    getData() {
      this.loading = true;
      this.$axios.get('menu/get/menus', {
        params: {
          id:this.id,
          page: this.currentPage,
          size: this.pageSize
        }
      }).then(res => {
        this.loading = false;
        this.tableData = res.data.data;
        this.total = res.data.total;

      })
    },

    // 编辑
    handleEdit(row) {
      this.addDrawer = true;
      this.enditView = true;
      this.title = '编辑用户';
      this.formData = { ...row }; // 使用深拷贝
      this.editDatas = row;
    },
    deepEqual(obj1, obj2) {
    return JSON.stringify(obj1) === JSON.stringify(obj2);
  },
    submitData() {
      if (this.deepEqual(this.editDatas, this.formData)) {
          this.$message.error('数据未修改');
          this.addDrawer = false;
          this.enditView = false;
          return;
        }
      this.$refs.drawerForm.validate(valid => {
        if (valid) {
          this.$axios.post('menu/edit/menu', {
            form: this.formData
          }).then(res => {
            if (res.data.code === 200) {
              this.$message.success(res.data.msg);
              this.getData();
               location.reload();
              this.addDrawer = false;
              this.enditView = false;
            } else {
              this.$message.error(res.data.msg);
            }
          });
        }
      });
    },
    handleSizeChange(newSize) {
      this.pageSize = newSize;
      this.getData();
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.getData();
    },
  }
}
</script>

<style scoped lang="less">
.box {
  width: 100%;
  height: 100%;
  .search {
    display: flex;
    position: relative;
    .upload{
      position: absolute;
      right: 5.5%;;
    }
    .addView {
      position: absolute;
      right: 1%;
    }
  }
  .table {
    width: 100%;
    height: 85%;
  }
  /deep/.el-drawer.rtl {
    padding: 10px;
    .addDrawerView {
      width: 100%;
      height: 100%;
    }
  }

  /deep/.el-button--primary:focus, .el-button--primary:hover {
    background: #409EFF;
    border-color: #409EFF;
    color: #FFF;
  }

  /deep/.el-button:focus, .el-button:hover {
    color: #FFF;
    border-color: #409EFF;
    background-color: #409EFF;
  }
  /deep/ .el-drawer__body::-webkit-scrollbar {
    display: none;
  }
  /deep/.el-pagination {
    position: absolute;
    left: 45%;
    bottom: 1%;
  }
}
</style>
