<template>
  <div class="box"
       v-loading="loading"
       element-loading-text="正在加载中"
       element-loading-spinner="el-icon-loading"
  >
    <div class="search">
      <el-form :inline="true" :model="formData" :rules="rules" ref="form" class="demo-form-inline">
        <el-form-item label="备注" prop="name">
          <el-input v-model="formData.name" placeholder="请输入备注"></el-input>
        </el-form-item>
      </el-form>
      <div class="upload">
        <el-upload action="#"
                   :http-request="uploadExcel"
                   :show-file-list="false"
                   :before-upload="beforeUpload">
          <el-button type="primary">导入样本</el-button>
        </el-upload>
      </div>
    </div>
    <div class="table">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column type="index" label="序号" align="center"></el-table-column>
        <el-table-column prop="name" label="备注" align="center"></el-table-column>
        <el-table-column prop="url" label="文件下载" align="center">
          <template slot-scope="scope">
            <div @click="getSampleFileUrl(scope.row.url)" style="cursor: pointer;color: red;">下载</div>
            <!-- <a :href="getSampleFileUrl(scope.row.url)" style=" color: #222222;">{{baseURL+'/media/sampleFiles/'+scope.row.url}}</a> -->
          </template>
        </el-table-column>
        <el-table-column
      label="操作"
      width="300"
      align="center"
      >
      <template slot-scope="scope">
        <el-button @click="handleDel(scope.row)" type="primary" size="small">删除</el-button>
        <el-button @click="handleEdit(scope.row)" type="primary" size="small">编辑</el-button>
        <el-button @click="handleAnalyse(scope.row)" type="primary" size="small">分析</el-button>
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

    <div class="bottom">
      <div class="charts">
        <div ref="barChart" style="width: 50%; height:320px; float: left;"></div>
        <div ref="pieChart" style="width: 50%; height: 320px; float: right;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  data() {
    return {
      baseURL: this.droneUrl,
      loading: false,
      formData: {
        name: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入备注信息', trigger: 'blur' }
        ]
      },
      tableData: [], // 初始化为空数组
      currentPage: 1,
      pageSize: 6,
      total: 0, // 初始化为0
      barChartData: [],
      pieChartData: []
    }
  },
  created() {
    this.id = JSON.parse(window.sessionStorage.getItem("currentUser")).id;
    this.getData();
  },
  mounted() {
    this.initBarChart();
    this.initPieChart();
  },
  methods: {
    getSampleFileUrl(url) {
      // 下载
      const path= `${this.baseURL}/media/sampleFiles/${url}`
      window.open(path);
    },
    // 获取数据
    getData() {
      this.loading = true;
      this.$axios.get('sampleSnalysis/get_data', {
        params: {
          id: this.id,
          page: this.currentPage,
          size: this.pageSize,
        }
      }).then(res => {
        if (res.data.code == 200) {
          this.loading = false;
          this.tableData = res.data.data; // 确保数据赋值给tableData
          this.total = res.data.total; // 确保数据赋值给total
        }
      }).catch(err => {
        this.loading = false;
        console.error('获取数据失败:', err);
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
    beforeUpload(file) {
      return new Promise((resolve, reject) => {
        this.$refs.form.validateField('name', (errorMessage) => {
          if (errorMessage) {
            this.$message.error('请输入备注');
            reject(false);
          } else {
            resolve(true);
          }
        });
      });
    },
    uploadExcel(file) {
      // 检查文件类型是否为 Excel 或 csv 文件
      const isExcel = file.file.type === 'application/vnd.ms-excel' || file.file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || file.file.type === 'text/csv';
      const isLt2M = file.file.size / 1024 / 1024 < 2;
      if (!isExcel) {
        this.$message.error('只能上传 Excel 或 csv 文件!');
        return false;
      }
      // 创建一个 loading 实例
      const loading = this.$loading({
        lock: true,
        text: '正在导入数据，请稍候...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });

      const fileReq = new FormData();
      fileReq.append('excel', file.file);
      fileReq.append('name', this.formData.name);
      fileReq.append('id', this.id);
      this.$axios.post('sampleSnalysis/upload', fileReq).then(res => {
        if (res.data.code === 200) {
          loading.close();
          this.formData.name=''
          this.$message.success(res.data.msg);
          this.getData();
        }
      }).catch((err) => {
        loading.close();
        this.$message.error(`上传失败,错误信息为:${err}`);
      });
    },
    // 删除
    handleDel(row) {
      this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.post('sampleSnalysis/delete', {
          id: row.id
        }).then(res => {
          if (res.data.code === 200) {
            this.$message.success(res.data.msg);
            this.getData();
          }
        })
      })
    },
    // 分析
    handleAnalyse(row) {
      const loading = this.$loading({
        lock: true,
        text: '正在分析中...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      this.$axios.post('sampleSnalysis/analyse', {
        url: this.baseURL + '/media/sampleFiles/' + row.url,
        file_id: row.id,
        id: this.id
      }).then(res => {
        if (res.data.code === 200) {
          // 关闭加载提示
          loading.close();
          this.$message.success(res.data.msg);

          // 深拷贝数据以去除响应式包装
          this.barChartData = JSON.parse(JSON.stringify(Object.entries(res.data.data).map(([name, value]) => ({ name, value }))));
          this.pieChartData = JSON.parse(JSON.stringify(Object.entries(res.data.data).map(([name, value]) => ({ name, value }))));
          this.updateBarChart();
          this.updatePieChart();
        } else {
          // 关闭加载提示
          loading.close();
          this.$message.error(`分析失败,错误信息为:${res.data.msg}`);
        }
      }).catch(err => {
        loading.close();
        this.$message.error(`分析失败,错误信息为:${err}`);
      });
    },

    initBarChart() {
      this.barChart = echarts.init(this.$refs.barChart);
      const option = {
        title: {
          text: '恶意软件分类柱状图',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: {  // 添加这行配置
            show: true,
            interval: 0,  // 强制显示所有标签
            rotate: 45    // 如果标签过长可以旋转显示
          }
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: '数量',
            type: 'bar',
            data: []
          }
        ]
      };
      this.barChart.setOption(option);
    },
    updateBarChart() {
      const option = this.barChart.getOption();
      option.xAxis[0].data = this.barChartData.map(item => item.name);
      option.series[0].data = this.barChartData.map(item => item.value);
      option.series[0].label = {  // 添加这行配置
          show: true,
          position: 'top'
        };
      console.log(option);

      this.barChart.setOption(option);
    },
    initPieChart() {
      this.pieChart = echarts.init(this.$refs.pieChart);
      const option = {
        title: {
          text: '恶意软件分类饼图',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: []
        },
        series: [
          {
            name: '分析结果',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      this.pieChart.setOption(option);
    },
    updatePieChart() {
      const option = this.pieChart.getOption();
      option.legend.data = this.pieChartData.map(item => item.name);
      option.series[0].data = this.pieChartData;
      option.series[0].label = {
          show: true,
          formatter: '{b}: {c} ({d}%)'
        };
      this.pieChart.setOption(option);
    },
    // 编辑
    handleEdit(row){
      this.$prompt('备注', '备注编辑', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^.{1,}$/,
          inputErrorMessage: '请输入内容',
          inputValue: row.name
        }).then(({ value }) => {
          if (value===row.name){
            return this.$message.warning('内容未修改');
          }else{
            this.loading = true;
            this.$axios.post('sampleSnalysis/update/remark', {
              id: row.id,
              name: value
            }).then(res => {
              if (res.data.code === 200) {
                this.loading = false;
                this.$message.success(res.data.msg);
                this.getData();
              }else {
                this.loading = false;
                this.$message.error(res.data.msg);
              }
            })
          }
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
    .upload {
      position: absolute;
      right: 1%;
    }
    .addView {
      position: absolute;
      right: 1%;
    }
  }
  .table {
    width: 100%;
    height: 50%;
    // background-color: #409EFF;
  }
  .bottom {
    margin-top: 35px;
    height: 38%;
    width: 100%;
  }
  /deep/.el-table {
    height: 100%;
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
    width: 97%;
    margin-top: 5px;
    position: fixed;
    text-align: center;
  }
}
</style>
