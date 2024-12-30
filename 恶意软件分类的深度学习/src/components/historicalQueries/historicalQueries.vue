<template>
  <div class="box"
    v-loading="loading"
    element-loading-text="正在加载中"
    element-loading-spinner="el-icon-loading"
  >

    <div class="search">
      <el-form :inline="true" class="demo-form-inline">
        <el-form-item label="备注">
          <el-input v-model="remark" placeholder="请输文件备注"></el-input>
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
      <!-- <div class="addView">
        <el-button type="primary" @click="openAddDrawer">新增</el-button>
        <el-button type="primary" @click="donwload">模板下载</el-button>
      </div> -->
    </div>
    <div class="table">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column type="index" label="序号" align="center"></el-table-column>
        <el-table-column prop="name" label="备注" align="center"></el-table-column>
        <el-table-column prop="file_id" label="id" align="center" width="250"></el-table-column>
        <el-table-column prop="Ramnit" label="Ramnit" align="center"></el-table-column>
        <el-table-column prop="Lollipop2" label="Lollipop2" align="center"></el-table-column>
        <el-table-column prop="Kelihos_ver3" label="Kelihos_ver3" align="center"></el-table-column>
        <el-table-column prop="Vundo" label="Vundo" align="center"></el-table-column>
        <el-table-column prop="Simda" label="Simda" align="center"></el-table-column>
        <el-table-column prop="Tracur" label="Tracur" align="center"></el-table-column>
        <el-table-column prop="Kelihos_ver1" label="Kelihos_ver1" align="center"></el-table-column>
        <el-table-column prop="Obfuscator_ACY" label="Obfuscator.ACY" align="center"></el-table-column>
        <el-table-column prop="Gatak" label="Gatak" align="center"></el-table-column>
        <!-- <el-table-column fixed="right" label="操作" align="center" width="200">
          <template slot-scope="scope">
            <div style="display: flex; justify-content: space-around;">
              <el-tag @click="handleView(scope.row)">查看</el-tag>
              <el-tag type="warning" @click="handleEdit(scope.row)">编辑</el-tag>
              <el-tag type="danger" @click="handelDelete(scope.row)">删除</el-tag>
            </div>
          </template>
        </el-table-column> -->
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
    <!-- <el-drawer
      :title="title"
      :visible.sync="addDrawer"
      direction="rtl"
      :size="'40%'"
      :before-close="handleClose"
    >
      <div class="addDrawerView">
        <el-form :model="formData" :rules="rules" ref="drawerForm" class="demo-form-inline">
          <el-form-item label="省份:" prop="province">
            <el-input v-model="formData.province" placeholder="请输入省份" style="width: 30%;" :disabled="viewDrawer"></el-input>
          </el-form-item>
          <el-form-item label="每票增加:">
            <el-input-number v-model="formData.eachIncreases" :min="0" :max="1000" style="margin-right: 5px;" :disabled="viewDrawer"></el-input-number>元
          </el-form-item>
          <el-form-item v-for="(item, index) in formData.priceSettings" :key="index">
            重量：
            <el-input-number v-model="item.startWeight" :min="0" :max="1000" label="重量1" :disabled="viewDrawer"></el-input-number> ——
            <el-input-number v-model="item.endWeight" :min="0.1" :max="1000" label="重量2" :disabled="viewDrawer" style="margin-right: 5px;" @change="validateWeights(item)"></el-input-number>kg
            价格：<el-input-number v-model="item.weightRangePrice" :min="0" :max="1000" label="价格" :disabled="viewDrawer" style="margin-right: 5px;"></el-input-number>元
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="addView" v-show="buttonShow">增加表单</el-button>
            <el-button type="primary" @click="delView" v-show="formData.priceSettings.length > 1 && buttonShow">删除表单</el-button>
          </el-form-item>
          <el-form-item style="display: flex; justify-content: center; margin-top: 10px;">
            <el-button type="primary" @click="submitData" v-show="!viewDrawer">确认</el-button>
          </el-form-item>
        </el-form>
      </div> -->
    <!-- </el-drawer> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      id: '',
      remark:'',
      tableData: [], // 初始化为空数组
      currentPage: 1,
      pageSize: 15,
      total: 0, // 初始化为0
    }
  },
  created() {
    this.id = JSON.parse(window.sessionStorage.getItem("currentUser")).id;
    this.getData(); // 在组件创建时调用getData方法
  },
  methods: {


    getData() {
      this.loading = true;
      this.$axios.get('sampleSnalysis/get/history', {
        params: {
          id: this.id,
          page: this.currentPage,
          size: this.pageSize,
          remark: this.remark

        }
      }).then(res => {
        if (res.data.code == 200) {
          this.loading = false;
          this.tableData = res.data.data; // 确保数据赋值给tableData
          this.total = res.data.total; // 确保数据赋值给total
        } else {
          this.loading = false;
          this.$message.error(res.data.msg);
        }
      }).catch(err => {
        this.loading = false;
        console.error('获取数据失败:', err); // 添加错误处理
      });
    },
    handleView(data) {
      this.addDrawer = true;
      this.viewDrawer = true;
      this.title = '查看';
      console.log(data.priceSettings);
      this.formData = data;
    },
    handelSearch() {
      if (this.remark === '') {
        return
      }
      this.currentPage = 1; // 查询时重置为第一页
      this.getData();
    },
    handelReset() {
      if (this.remark === '') {
        return
      }
      this.currentPage = 1; // 重置时重置为第一页
      this.remark = ''
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
        // 上传文件
  uploadExcel(file) {
  // 检查文件类型是否为 Excel
  const isExcel = file.file.type === 'application/vnd.ms-excel' || file.file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
  const isLt2M = file.file.size / 1024 / 1024 < 2;
  if (!isExcel) {
    this.$message.error('只能上传 Excel 文件!');
    return false;
  }
  // 创建一个loading实例
    const loading = this.$loading({
      lock: true,
      text: '正在导入数据，请稍候...',
      spinner: 'el-icon-loading',
      background: 'rgba(0, 0, 0, 0.7)'
    });

    const fileReq = new FormData();
    fileReq.append('excel', file.file);
    fileReq.append('id', this.id);
    this.$axios.post('provinceprice/import/provinceprice', fileReq).then(res => {
      if (res.data.code === 200) {
        loading.close();
        this.$message.success(res.data.msg);
        this.getData();
      } else {
        loading.close();
        this.$message.error(`上传失败,错误信息为:${res.data.msg}`);
      }
    }).catch(err => {
      loading.close();
      this.$message.error(`上传失败,错误信息为:${err}`);
    });
  },
  // 下载模板
  donwload(){
    this.loading=true;
    this.$axios.get('paramsettings/download/template',{
      responseType: 'blob'
    }).then(res => {
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', '单价设置.xlsx');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      this.loading=false;
    }).catch(err => {
      this.loading=false;
      this.$message.error(`下载失败,错误信息为:${err}`);
    })
  }
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
      right: 12%;;
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

    position: fixed;
    width: 97%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 1%;
  }
}
</style>
