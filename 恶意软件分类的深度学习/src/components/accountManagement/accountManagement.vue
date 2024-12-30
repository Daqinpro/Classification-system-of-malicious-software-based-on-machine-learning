<template>
  <div class="box"
    v-loading="loading"
    element-loading-text="正在修改中"
    element-loading-spinner="el-icon-loading">
    <div class="content">
      <el-form label-width="80px" :model="ruleForm" :rules="rules" ref="ruleForm">
        <el-form-item label="账户名">
          <el-input v-model="ruleForm.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="原密码" prop="oldpassword">
          <el-input v-model="ruleForm.oldpassword" type="password"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newpassword">
          <el-input v-model="ruleForm.newpassword" type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="newtwopassword">
          <el-input v-model="ruleForm.newtwopassword" type="password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="submitForm">立即修改</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    const validateNewPassword = (rule, value, callback) => {
      if (value !== this.ruleForm.newpassword) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    };

    return {
      loading: false,
      ruleForm: {
        username: '',
        oldpassword: '',
        newpassword: '',
        newtwopassword: ''
      },
      id: '',
      rules: {
        oldpassword: [
          { required: true, message: '请输入原密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
        ],
        newpassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
        ],
        newtwopassword: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { validator: validateNewPassword, trigger: 'blur' }
        ]
      }
    };
  },
  created() {
    this.ruleForm.username = JSON.parse(window.sessionStorage.getItem("currentUser")).username;
    this.id = JSON.parse(window.sessionStorage.getItem("currentUser")).id;
  },
  methods: {
    submitForm() {

      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          this.loading = true; // 开始加载
          this.$axios
            .post("user/change/password", {
              id: this.id,
              oldpassword: this.$md5(this.ruleForm.oldpassword),
              newpassword: this.$md5(this.ruleForm.newpassword)
            })
            .then(res => {
              if (res.data.code == 200) {
                this.$message.success(res.data.msg);
                window.sessionStorage.removeItem("token");
                window.sessionStorage.removeItem("currentUser");
                this.$router.push("/login");
              }
              else {
                this.$message.warning(res.data.msg);
                this.ruleForm.oldpassword=''
                this.ruleForm.newpassword=''
                this.ruleForm.newtwopassword=''
                this.loading = false;
              }
            })
            .catch(() => {
              this.$message.error(res.data.msg);
              this.loading = false; // 结束加载
            });
        } else {
          this.$message.error('请输入正确信息');
          this.loading = false; // 结束加载
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.ruleForm.resetFields();
    }
  }
}
</script>

<style scoped lang="less">
.box {
  width: 100%;
  height: 100%;
  .title {
    display: flex;
    align-items: center;
    width: 100%;
    height: 50px;
    font-size: 1.3vw;
  }
  .content {
    display: flex;
    justify-content: center;
    width: 100%;
    height: calc(100% - 50px);
    background-color: #fffbff;
    border-radius: 10px;
  }
  /deep/.el-input__inner {
    width: 100%;
  }
  /deep/.el-form {
    margin-top: 4%;
    border-radius: 10px;
    width: 30%;
    height: 50%;
  }
  /deep/.el-form-item__content {
    text-align: center;
  }
  /deep/.el-button {
    width: 50%;
  }
}
</style>
