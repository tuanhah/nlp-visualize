<template>
  <div>
    <div class="hello" v-if ="!loading">
      <h1>{{ msg }}</h1>
      <input class="input-text" v-model="url"/>
      <div>
        <span class ="text-error" v-if ="haveError">Hãy nhập url của phim cần đánh giá</span>
      </div>
      <div>
        <button @click="getData"> Analysic </button>
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
      <div v-show="showVisualize" class = "analysic">
        <div class ="pie-chart" >
          <apexchart type=pie width=380 :options="chartOptions" :series="series" />
          <span class='span-text'>Tỉ lệ bình luận trong phim</span>
        </div>
        <div class="table">
          <el-table
            :data="tableData"
            height="600"
            style="width: 100%">
            <el-table-column
              prop="id"
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
            </el-table-column>
          </el-table>
        </div>
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
      msg: 'Hệ thống đánh giá phim dựa theo trang IMDB',
      url: null,
      showVisualize : false,
      loading: false,
      haveError: false,
      series: [70,30],
      chartOptions: {
        labels: ['Positive', 'Negative'],
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
    }
  },
  methods: {
    getData() {
      // this.url ="https://www.imdb.com/title/tt3417422/reviews?ref_=tt_urv";
      if (! this.url) {
        this.showVisualize = false;
        this.loading = false;
        this.haveError = true;
        return;
      }
      let arr = this.url.split('/');
      if (arr && arr[4]) {
        this.haveError = false;
        this.loading = true;
        this.showVisualize = true;
        this.getDataTable(arr[4]);

      } else {
        this.showVisualize = false;
        this.loading = false;
        this.haveError = true;
        return;
      }
    },
    getDataTable(id) {
      if (id) {
        let url = "http://localhost:8008/crawl/?id=" + id;
        this.$axios.get(url).then(res =>{
          this.tableData = res.data.data;
          let rating_tb = 0;
          this.totalReview = res.data.total;
          res.data.data.forEach(el => {
            if (el.rating) {
              rating_tb = rating_tb + parseInt(el.rating);
            }
          });
          console.log(rating_tb);
          console.log(res.data.total);
          this.average_rating = Math.round(rating_tb / res.data.total *100) /100;;
          this.loading = false;
        })
        .catch(e => {
          console.log(e);
          this.loading = false;
        })
      }
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
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
input {
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
.sumary {
    border:none;
    border-radius: 5px;
    padding: 5px;
    margin-left: 222px;
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
  height: 45px;
  color: white;
  border-radius: 4px;
}
.analysic{
  display: flex;
  flex-direction: row;
}
.pie-chart{
  width: 23%;
}
.table{
  width: 77%;
}
table {
  border-collapse: collapse;
  width: 100%;
}

table, th, td {
  border: 1px solid black;
}
</style>
