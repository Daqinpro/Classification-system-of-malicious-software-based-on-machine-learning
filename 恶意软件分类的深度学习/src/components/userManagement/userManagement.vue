<template>
  <div class="box"
    v-loading="loading"
    element-loading-text="正在加载中"
    element-loading-spinner="el-icon-loading"
  >

    <div class="search">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="账号">
          <el-input v-model="username" placeholder="请输入账号"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handelSearch">查询</el-button>
          <el-button type="primary" @click="handelReset">重置</el-button>
        </el-form-item>
      </el-form>
      <!-- <div class="upload">
        <el-upload action="#"
                :http-request="uploadExcel"
                :show-file-list="false"
            >
              <el-button type="primary">导入Excel</el-button>
            </el-upload>
      </div> -->
      <div class="addView">
        <el-button type="primary" @click="openAddDrawer">新增</el-button>
      </div>
    </div>
    <div class="table">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column type="index" label="序号" align="center"></el-table-column>
        <!-- <el-table-column prop="name" label="姓名" align="center"></el-table-column> -->
        <el-table-column prop="username" label="账号" align="center"></el-table-column>
        <el-table-column prop="role" label="角色名称" align="center">
          <template slot-scope="scope">
            {{ scope.row.role === 2 ? '管理员' : '用户' }}
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
              <el-tag @click="resetPassword(scope.row)">密码重置</el-tag>
              <el-tag type="warning" @click="handleEdit(scope.row)">编辑</el-tag>
              <el-tag type="danger" @click="handelDelete(scope.row)">删除</el-tag>
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
          <el-form-item label="账号:"  prop="username">
            <el-input v-model="formData.username" placeholder="请输入QQ邮箱" style="width: 40%;" :disabled="enditView"></el-input>
          </el-form-item>
          <el-form-item label="密码:"  prop="password" v-show="!enditView">
            <el-input v-model="formData.password" placeholder="请输入密码" style="width: 40%;" ></el-input>
          </el-form-item>
          <el-form-item label="角色:"  prop="role">
            <el-select v-model="formData.role" placeholder="请选择角色名称" >
            <el-option label="用户" :value="1"></el-option>
            <el-option label="管理员" :value="2"></el-option>
          </el-select>
          </el-form-item>
          <el-form-item label="状态:"  prop="state">
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
export default {
  data() {
    return {
      loading: false,
      editDatas: [],
      addDrawer: false,
      enditView: false,
      id: '',
      username:'',
      formData: {
        username:'',
        role:'',
        state:'',
        password:''
      },
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { pattern: /^[1-9]\d{4,10}@qq\.com$/, message: "请输入正确的QQ邮箱地址", trigger: ["blur", "change"] }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色名称', trigger: 'change' }
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
          this.getData(); // 刷新数据
          this.viewDrawer = false;
          this.enditView = false;
          this.formData={}
          this.$refs.drawerForm.resetFields(); // 重置表单字段

        })
        .catch(_ => {});
    },
    // 打开新增弹窗
    openAddDrawer() {
      this.buttonShow = true;
      this.addDrawer = true;
      this.title = "新增用户";
    },
    addData() {
      this.$refs.drawerForm.validate((valid) => {
        if (valid) {
          const loading = this.$loading({
            lock: true,
            text: '正在添加中...',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          // 密码md5加密
          this.formData.password = this.$md5(this.formData.password);
          this.$axios.post('user/add/user', {
            form: this.formData
          }).then(res => {
            if (res.data.code == 200) {
              this.$message.success('新增成功');
              loading.close();
              this.addDrawer = false;
              this.$refs.drawerForm.resetFields(); // 重置表单字段
              this.formData = {};
              this.getData(); // 刷新数据
            } else {
              loading.close();
              this.formData.password = '';
              this.$message.error(res.data.msg);
            }
          })
        } else {
          return false;
        }
      });
    },
    submitData() {
    if (this.enditView === false) {
      // 添加时，确保密码有校验规则
      this.rules.password = [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ];
    } else {
      // 编辑时，移除密码的校验规则
      this.rules.password = [];
    }
    this.$refs.drawerForm.validate((valid) => {
      if (valid) {
        if (this.enditView === false) {
          this.addData();
        } else {
          this.editData();
        }
      } else {
        return false;
      }
    });
  },
    getData() {
      this.loading = true;
      this.$axios.get('user/get/users', {
        params: {
          id:this.id,
          username:this.username,
          page: this.currentPage,
          size: this.pageSize
        }
      }).then(res => {
        this.loading = false;
        this.tableData = res.data.data;
        this.total = res.data.total;
      })
    },

    // 删除
    handelDelete(row) {
      this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post('user/delete/user', {
          id: row.id
        }).then(res => {
          if (res.data.code === 200) {
            this.$message.success(res.data.msg);
            this.getData();
          } else {
            this.$message.error(res.data.msg);
          }
        })
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
    editData() {
      this.$refs.drawerForm.validate(valid => {
        if (valid) {
          this.$axios.post('user/update/user', {
            form: this.formData
          }).then(res => {
            if (res.data.code === 200) {
              this.$message.success(res.data.msg);
              this.getData();
              this.addDrawer = false;
              this.enditView = false;
            } else {
              this.$message.error(res.data.msg);
            }
          });
        }
      });
    },
    resetPassword(row){
      this.$confirm('此操作将重置密码, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post('user/update/password', {
          id: row.id
        }).then(res => {
          if (res.data.code === 200) {
            this.$message.success(res.data.msg);
          }else {
            this.$message.error(res.data.msg);
          }
        })
      })
    },
    handelSearch() {
      if (this.username === '') {
        return
      }
      this.currentPage = 1; // 查询时重置为第一页
      this.getData();
    },
    handelReset() {
      if (this.username === '') {
        return
      }
      this.currentPage = 1; // 重置时重置为第一页
      this.username = ''
      this.getData();
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
