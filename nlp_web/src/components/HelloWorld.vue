<template>
  <div>
    <div class="hello" v-if ="!loading">
      <h1>{{ msg }}</h1>
      <input class="input-text" v-model="url"/>
      <div>
        <span class ="text-error" v-if ="haveError">Please type url</span>
      </div>
      <div>
        <button @click="getData"> Analysic </button>
      </div>
      <div v-show="showVisualize" class = "analysic">
        <div class ="pie-chart" >
          <apexchart type=pie width=380 :options="chartOptions" :series="series" />
        </div>
        <div class="table">
          <!-- <table>
            <thead>
              <tr>
                <th class ="text-left">ID</th>
                <th class ="text-left">Rating</th>
                <th class ="text-left">Content</th>
                <th class ="text-left">Classify</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in dataTable">
                <td>{{item.rating}}</td>
                <td>{{item.rating}}</td>
                <td>{{item.rating}}</td>
                <td>{{item.rating}}</td>
              </tr>
            </tbody>
          </table> -->


          <el-table
            :data="tableData"
            height="500"
            style="width: 100%">
            <el-table-column
              prop="date"
              label="Date"
              width="100">
            </el-table-column>
            <el-table-column
              prop="name"
              label="Name"
              width="480">
            </el-table-column>
            <el-table-column
              prop="address"
              label="Address">
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
      msg: 'Please type url of film',
      url: null,
      showVisualize : false,
      loading: false,
      haveError: false,
      series: [50,50],
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
      tableData: [{
          date: '2016-05-03',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles'
        }, {
          date: '2016-05-02',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles'
        }, {
          date: '2016-05-04',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles'
        }, {
          date: '2016-05-01',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles'
        }, {
          date: '2016-05-08',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles'
        }, {
          date: '2016-05-06',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles'
        }, {
          date: '2016-05-07',
          name: 'Tom',
          address: 'No. 189, Grove St, Los Angeles'
        }],
    }
  },
  methods: {
    getData() {
      this.url ="https://www.imdb.com/title/tt4777008/reviews?ref_=tt_urv";
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
          console.log(res);
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
.text-error{
  color: red;
}
.input-text {
  width: 40%;
  height: 30px;
  border-radius: 4px;
  border: 1px solid #2dac91;
  padding-top: 5px;
}
button {
  background-color: #2dac91;
  border: 1px solid #2dac91;
  width: 80px;
  margin-top: 5px;
  text-transform: uppercase;
  /* font-weight: 500; */
  height: 33px;
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
