<template>
  <div>
    <div class="hello" v-if ="!loading">
      <h1>{{ msg }}</h1>
      <!-- <textarea class="input-text" v-model="url"></textarea>
      <div>
        <span class ="text-error" v-if ="haveError">Hãy nhập url của phim cần đánh giá</span>
      </div> -->
      <div class="form-control-total">

        <div class="form-control">
          <div class = "title"> Chọn thể loại</div>
          <el-select v-model="type" placeholder="Select">
          <el-option
            v-for="item in types"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        </div>
        <div class="form-control">
          <div class = "title"> Chọn model</div>
          <el-select v-model="model_train" placeholder="Select">
          <el-option
            v-for="item in model_trains"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        </div>
        <div class="form-control" v-if ="type == '1'">
          <div class = "title-content"> Nhập câu nhận xét của bạn</div>
          <el-input
            type="textarea"
            :rows="3"
            placeholder="Please input"
            v-model="customContent">
          </el-input>
        </div>
        <div class="form-control url-form" v-if="type == '2'">
          <div class = "title-content"> Nhập đường dẫn đến phim</div>
          <el-input
            placeholder="Please input"
            v-model="url"
            clearable>
          </el-input>
        </div>
      </div>
      <div>
        <button @click="getData"> Analysic </button>
      </div>
      
      <div v-show="showVisualize" class = "analysic">
        <div class ="pie-chart" >
          <apexchart type=pie width=600 :options="chartOptions" :series="series" />
        </div>
      </div>
      <div v-show="showVisualize" class = "analysic float-div">
        <div class="sumary">
          <div class="n1-div">Tổng số bình luận</div>
          <div>{{totalReview}}</div>
        </div>
        <div class="sumary">
          <div class="n1-div">Rating trung bình</div>
          <div>{{average_rating}}</div>
        </div>
        <div class="sumary">
          <div class="n1-div">Số bình luận tích cực</div>
          <div>500</div>
        </div>
        <div class="sumary">
          <div class="n1-div">Số bình luận tiêu cực</div>
          <div>500</div>
        </div>
      </div>
        <div v-show="showVisualize" class="table">
          <el-table
            :data="tableData"
            height="600"
            :row-class-name="tableRowClassName">
            style="width: 100%">
            <el-table-column
              prop="id"
              fixed
              label="ID"
              width="100">
            </el-table-column>
            <el-table-column
              prop="rating"
              label="Rating"
              width="100">
            </el-table-column>
            <el-table-column
              prop="content"
              label="Content"
              width="880">
            </el-table-column>
            <el-table-column
              prop="class"
              label="Classification">
              <i class="el-icon-star-on "></i>
            </el-table-column>
          </el-table>
        </div>
    </div>
    <div v-else >
       <square></square>
    </div>
  </div>
</template>

<script>
 import routes from '../router/index';
 import Visualize from './Visualize';
//  import Chart from 'apexcharts';
export default {
  name: 'HelloWorld',
  components: {
      Visualize,
      // Chart,
    },
  data () {
    return {
      msg: 'Hệ thống đánh giá bình luận phim',
      url: null,
      showVisualize : false,
      loading: false,
      haveError: false,
      series: [70,30],
      chartOptions: {
        labels: ['Positive', 'Negative'],
        fill: {
          colors: ['#E15278', '#84E9AB']
        },
        colors:['#E15278', '#84E9AB'],
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
      },
      tableData: [],
      average_rating: 0,
      totalReview: 0,
      types: [{
          value: '1',
          label: 'Nhập câu của bạn'
        }, {
          value: '2',
          label: 'Nhập url của trang IMDB'
        }],
        type: '',
        model_trains: [{
          value: 'Option1',
          label: 'Option1'
        }, {
          value: 'Option2',
          label: 'Option2'
        }, {
          value: 'Option3',
          label: 'Option3'
        }, {
          value: 'Option4',
          label: 'Option4'
        }, {
          value: 'Option5',
          label: 'Option5'
        }],
        model_train: '',
        customContent:"",
    }
  },
  methods: {
    tableRowClassName({row}){
      if (row.class) {
        return 'positive';
      } else {
        return 'negative';
      }
    },
    getData() {
      // this.url ="https://www.imdb.com/title/tt3417422/reviews?ref_=tt_urv";
      if (this.type == '2') {
        
        let arr = this.url.split('/');
        if (arr && arr[4]) {
          this.loading = true;
          this.showVisualize = true;
          this.getDataTable(arr[4]);
  
        } else {
          this.showVisualize = false;
          this.loading = false;
          this.haveError = true;
          return;
        }
      } else {
        this.loading = true;
        this.showVisualize = true;
        this.getDataTable('custom');
      }
    },
    getDataTable(type) {
      if (type == "custom") {
        let url = "http://localhost:8008/crawl/custom";
        this.$axios.post(url, {
          data : this.customContent,
          model: this.model_train
        }).then(res => {
          this.handleRequest(res);
        })
        .catch(e => {
          console.log(e);
          this.loading = false;
        })
      } else {
        if (type) {
          let url = "http://localhost:8008/crawl/?id=" + type + "&model="+this.model_train;
          this.$axios.get(url).then(res =>{
            this.handleRequest(res);
          })
          .catch(e => {
            console.log(e);
            this.loading = false;
          })
        }
      }
    },
    handleRequest(res) {
      this.tableData = res.data.data;
      let rating_tb = 0;
      this.totalReview = res.data.total;
      res.data.data.forEach(el => {
        if (el.rating) {
          rating_tb = rating_tb + parseInt(el.rating);
        }
      })
      this.average_rating = Math.round(rating_tb / res.data.total *100) /100;
      if  (this.average_rating < 0) this.average_rating = "None";
      this.loading = false;
    }
  },
  mounted() {
  },

}
</script>
<style>
.el-table--fit {
  border: 1px solid #EBEEF5;
}
.el-table__row td{
  border-right: 1px solid #EBEEF5;
}
.el-select {
  width: 40%;
  margin-bottom: 18px;
}
.el-textarea, .url-form .el-input--suffix {
  width: 40%;
  margin-bottom: 18px;
}
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
  margin-bottom: 80px;
}
.title {
  font-family: sans-serif;
  margin-left: -412px;
  margin-bottom: 6px;
}
.title-content {
  font-family: sans-serif;
  margin-left: -306px;
  margin-bottom: 6px;
}
textarea{
  padding-left: 10px;
  margin-bottom: 5px;
}
.text-error{
  color: red;
}
.float-div {
  margin-top: 100px;
  margin-bottom: 100px;
  background: #F5F5F5;
}
.n1-div {
  margin-top: 19px;
  margin-bottom: 5px;
}
i {
  font-size: 60px;
  margin-left: 54px;
}
.positive i{
  color: #E15278;
}
.negative i{
  color:#84E9AB;
}
.sumary {
    border:none;
    border-radius: 5px;
    padding: 5px;
    margin-left: 110px;
    margin-top: 50px;
    margin-bottom: 50px;
    background: #2cad91;
    min-width: 163px;
    min-height: 70px;
    color: white;
}
.span-text{
  margin-left: -133px;
}
.input-text {
  width: 40%;
  height: 53px;
  border-radius: 4px;
  border: 1px solid #2dac91;
  padding-top: 5px;
}
button {
  background-color: #2dac91;
  border: 1px solid #2dac91;
  width: 146px;
  margin-top: 15px;
  text-transform: uppercase;
  /* font-weight: 500; */
  font-size: 19px;
  height: 45px;
  color: white;
  border-radius: 4px;
}
.analysic{
  display: flex;
  flex-direction: row;
}
.pie-chart{
  /* width: 23%; */
  margin-left: 363px;
  margin-top:70px;
}
.table{
  width: 100%;
}
table {
  border-collapse: collapse;
  width: 100%;
}

table, th, td {
  border: 1px solid black;
}
</style>
