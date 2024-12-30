<template>
  <div class="login"
    v-loading="loading"
    element-loading-text="正在加载中"
    element-loading-spinner="el-icon-loading"
    >

    <!-- 登录盒子 -->
    <div class="login_box" v-show="loginBox">
      <!-- 输入框盒子 -->
      <div class="input_box">
        <div class="top">用户登录</div>
        <div class="bottom">
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" @keyup.enter.native="login('ruleForm')">
            <el-form-item label="账户名" prop="name">
              <el-input
                prefix-icon="el-icon-user"
                v-model="ruleForm.name"
                placeholder="请填写您的账户"
              ></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                prefix-icon="el-icon-lock"
                v-model="ruleForm.password"
                show-password
                placeholder="请填写登录密码"
              >
              </el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="auth_code">
              <el-input
                prefix-icon="el-icon-more-outline"
                v-model="ruleForm.auth_code"
                placeholder="请输入验证码"
              >
                <template slot="append">
                  <div id="code"></div>
                </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="login('ruleForm')" :loading="loading">立即登录</el-button>
              <div style="display: flex; justify-content: right; margin-top: 10px;" ><p style="width: 75px;cursor: pointer;" @click="toEnroll('ruleForm')">注册账号？</p></div>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <!-- 注册盒子 -->
    <div class="login_box" v-show="!loginBox">
      <!-- 输入框盒子 -->
      <div class="input_box">
        <div class="top">用户注册</div>
        <div class="bottom">
          <el-form :model="enrollForm" :rules="enrollRules" ref="enrollForm" @keyup.enter.native="login('enrollForm')">
            <el-form-item label="邮箱" prop="name">
              <el-input
                prefix-icon="el-icon-user"
                v-model="enrollForm.name"
                placeholder="请填写您的QQ邮箱"
              ></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input
                prefix-icon="el-icon-lock"
                v-model="enrollForm.password"
                show-password
                placeholder="请填写您的登录密码"
              >
              </el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="auth_code">
              <el-input
                prefix-icon="el-icon-more-outline"
                v-model="enrollForm.auth_code"
                placeholder="请输入获取的验证码"
              >
              <template slot="append">
              <div
                v-if="countdown === 0"
                @click="startCountdown('enrollForm')"
                style="width: 120px;height: 41px;display: flex;justify-content: center;align-items: center; cursor: pointer;color: #ff5000;font-size: 16px;">
                获取验证码
              </div>
              <div
                v-else
                style="width: 120px;height: 41px;display: flex;justify-content: center;align-items: center; color: #ff5000;font-size: 16px;">
                {{ countdown }} 秒后重新获取
              </div>
            </template>
              </el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="enroll('enrollForm')" :loading="loading">立即注册</el-button>
              <div style="display: flex; justify-content: right; margin-top: 10px;" ><p style="width: 75px;cursor: pointer;" @click="toLogin('enrollForm')">返回登录？</p></div>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { GVerify } from "../../static/code";

export default {
  data() {
    // 登录验证码输入框验证是否输入正确
    let codeBoolean = (rule, value, callback) => {
      let bool = this.verifyCode.validate(value);
      if (!bool) {
        callback(new Error("验证码不正确，请核对后重新输入"));
        this.verifyCode.refresh();
      } else {
        callback();
      }
    };

    return {
      countdown: 0,
      timer: null,
      loginBox:true,
      loading: false,
      // 验证码方法
      verifyCode: "",
      ruleForm: {
        name: "",
        password: "",
        auth_code: "",
      },
      rules: {
        name: [{ required: true, message: "请输入QQ邮箱", trigger: "blur" },
        { pattern: /^[1-9]\d{4,10}@qq\.com$/, message: "请输入正确的QQ邮箱地址", trigger: ["blur", "change"] }
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        auth_code: [
          { required: true, message: "请输入验证码", trigger: "blur" },
          { validator: codeBoolean, trigger: "blur" }
        ],
      },
      enrollForm: {
        name: "",
        password: "",
        auth_code: "",
      },
      enrollRules: {
        name: [{ required: true, message: "请输入QQ邮箱", trigger: "blur" },
        { pattern: /^[1-9]\d{4,10}@qq\.com$/, message: "请输入正确的QQ邮箱地址", trigger: ["blur", "change"] }
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        auth_code: [
          { required: true, message: "请输入验证码", trigger: "blur" },

        ]
      }
    };
  },
  created() {
  },
  mounted() {
    // 验证码
    this.verifyCode = new GVerify("code");
  },
  methods: {
    // 登录按钮
    login(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.loading = true; // 开始加载
          this.$axios.post("user/login", {
                username: this.ruleForm.name,
                password: this.$md5(this.ruleForm.password),
            }).then(res => {
              if (res.data.code === 200) {
                this.loading = false; // 结束加载
                window.sessionStorage.setItem("token", res.data.token);
                window.sessionStorage.setItem("currentUser", JSON.stringify(res.data.user));
                this.$router.push("/home");
              } else if(res.data.code === 450){
                this.loading = false; // 结束加载
                this.verifyCode.refresh();
                this.$message.warning(res.data.msg);
                this.loginBox=false;
                this.ruleForm={
                  name: '',
                  password: '',
                  auth_code: '',
                }
              } else {
                this.loading = false; // 结束加载
                this.verifyCode.refresh();
                this.$message.warning(res.data.msg);
              }

            })
            .catch(error => {
              this.loading = false; // 结束加
              this.$message.error(res.data.msg);
            });
        } else {
          this.loading = false; // 结束加
          return false;
        }
      });
    },
    // 登录
    toLogin(enrollForm){
      this.loginBox = true;
      this.$refs[enrollForm].resetFields();
      this.enrollForm={
        name: "",
        password: "",
        auth_code: "",
      }

    },
    // 注册
    toEnroll(enrollForm){
      this.loginBox = false;
      this.$refs[enrollForm].resetFields();
    },
    startCountdown(enrollForm) {
    // 先验证邮箱字段
    this.$refs['enrollForm'].validateField('name', valid => {
      if (!valid) {
        // 如果邮箱字段有效，则发送请求并开始倒计时
        this.$axios.post("user/get_code", {
          username: this.enrollForm.name
        }).then(res => {
          if (res.data.code === 200) {
            this.$message.success("验证码发送成功");
            this.countdown = 30;
            this.timer = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown--;
          } else {
            clearInterval(this.timer);
          }
        }, 1000);
          } else {
            this.$message.warning(res.data.msg);
          }
        });
      } else {
        // 如果邮箱字段无效，提示用户
        this.$message.warning("请输入有效的QQ邮箱");
      }
    });
  },
    beforeDestroy() {
    // 清除定时器以防止内存泄漏
    clearInterval(this.timer);

  },
  enroll(enrollForm){
    this.$refs[enrollForm].validate(valid => {
        if (valid) {
          this.loading = true; // 开始加载
          this.$axios.post("user/register", {
                username: this.enrollForm.name,
                password: this.$md5(this.enrollForm.password),
                auth_code: this.enrollForm.auth_code
            }).then(res => {
              if (res.data.code === 200) {
                this.loading = false; // 结束加载
                this.$message.success(res.data.msg);
                this.loginBox=true;
              } else {
                this.loading = false; // 结束加载
                this.$message.warning(res.data.msg);
                this.enrollForm.auth_code=''
              }

            })
            .catch(error => {
              this.loading = false; // 结束加
              this.$message.error(res.data.msg);
            });
        } else {
          this.loading = false; // 结束加
          return false;
        }
      });
  }
  }

};
</script>

<style lang="less" scoped>
  .login {
    width: 100%;
    height: 100%;
    background: #e9f1fe;
    user-select: none;

    // 登录盒子
    .login_box {
      width: 100%;
      height: 100%;
      position: relative;
      display: flex;
      align-items: center;
      background-image: url("../assets/login/LOGIN.jpg");
      background-repeat: no-repeat;
      background-size: cover;
      background-position: center;
      overflow: hidden;
      // 输入框盒子
      .input_box {
        width: 442px;
        height: 500px;
        top: 140px;
        background: #fff;
        position: absolute;
        right: 10%;
        border-radius: 10px;

        .forget {
          display: flex;
          justify-content: right;
          margin-right: 10px;
          margin-top: 30px;
          cursor: pointer;
        }
        .top {
          width: 100%;
          height: 75px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 30px;
          color: #3358ca;
        }
        .bottom {
          width: 74%;
          height: 70%;
          margin-left: 13%;
          /deep/.el-form-item {
            margin-bottom: 0.9vw;
            .el-form-item__label {
              line-height: 35px;
            }
            .el-input__inner {
              height: 43px;
            }
            input::placeholder {
              font-size: 13px;
            }
            .el-input__prefix {
              color: black;
              line-height: 43px;
            }
            .el-button {
              width: 100%;
              background: #3358ca;
              margin-top: 15px;
              border: none;
            }
            .el-input-group__append {
              padding: 0;
              #code {
                width: 100px;
                height: 41px;
                overflow: hidden;
                #imgVerify {
                  width: 100%;
                  height: 100%;
                }
              }
            }
          }
        }
      }
    }
  }

</style>
