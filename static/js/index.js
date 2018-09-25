

var routes = [
{
        path: '/change',
        name: 'change',
        component: {
            template: `
                <div class="container">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="list-group side-bar">
                                <router-link class="list-group-item" to="/">首页</router-link>
                                <router-link class="list-group-item" to="/search_left_ticket">余票查询</router-link>
                                <router-link class="list-group-item active" to="/preplot_manage">订单管理</router-link>
                                <router-link class="list-group-item" to="/mine_info">我的信息</router-link>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="row clearfix">
                            
                                    <div class = "date-station">
                                          <select v-model="year" class="selectpicker show-tick" title="年份" data-live-search="true" data-size="20">
                                                <option>2018</option>
                                                <option>2017</option>
                                                <option>2016</option>
                                                <option>2015</option>
                                                <option>2013</option>
                                                <option>2012</option>
                                                <option>2011</option>
                                          </select>
                                          <label>年</label>
                                          <select v-model="month" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                               <option>1</option>
                                               <option>2</option>
                                               <option>3</option>
                                               <option>4</option>
                                               <option>5</option>
                                               <option>6</option>
                                               <option>7</option>
                                               <option>8</option>
                                               <option>9</option>
                                               <option>10</option>
                                               <option>11</option>
                                               <option>12</option>
                                          </select>
                                          <label>月</label>
                                          <select v-model="day" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                                <option>1</option>
                                                <option>2</option>
                                                <option>3</option>
                                                <option>4</option>
                                                <option>5</option>
                                                <option>6</option>
                                                <option>7</option>
                                                <option>8</option>
                                                <option>9</option>
                                                <option>10</option>
                                                <option>11</option>
                                                <option>12</option>
                                                <option>13</option>
                                                <option>14</option>
                                                <option>15</option>
                                                <option>16</option>
                                                <option>17</option>
                                                <option>18</option>
                                                <option>19</option>
                                                <option>20</option>
                                                <option>21</option>
                                                <option>22</option>
                                                <option>23</option>
                                                <option>24</option>
                                                <option>25</option>
                                                <option>26</option>
                                                <option>27</option>
                                                <option>28</option>
                                                <option>29</option>
                                                <option>30</option>
                                                <option>31</option>
                                          </select>
                                          <label>日</label>
                                          <label>始发站</label>
                                           <select v-model="startstation" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                               <option>北京站</option>
                                               <option>上海站</option>
                                               <option>威海站</option>
                                               <option>深圳站</option>
                                               <option>广州站</option>
                                               <option>烟台站</option>
                                               <option>济南站</option>
                                               <option>青岛站</option>
                                             
                                          </select>
                                           <label>终点站</label>
                                           <select v-model="endstation" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                               <option>北京站</option>
                                               <option>上海站</option>
                                               <option>威海站</option>
                                               <option>深圳站</option>
                                               <option>广州站</option>
                                               <option>烟台站</option>
                                               <option>济南站</option>
                                               <option>青岛站</option>
                                          </select>
                                          
                                       
                                          <button style="margin-left: 1000px;background-color: #1b9dec;width: 100px" @click="search" class="btn btn-block">查询</button>

                              </div>     
                              <div class="container">
                              
                                  <div>
                                        <table class="table table-hover" style="width: 1000px">
                                            <thead>
                                                <tr>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>到达站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>商务座</th>
                                                    <th>一等座</th>
                                                    <th>二等座</th>
                                                    <th>软卧</th>
                                                    <th>硬卧</th>
                                                    <th>软座</th>
                                                    <th>硬座</th>
                                                    <th>无座</th>
                                                    <th>操作</th>
                                                </th>
                                            </thead>
                                            <tbody>
                                                <tr v-for="(item,index) in search_data">
                                                    <td>{{ item['train_id'] }}</td>
                                                    <td>{{ startstation }}</td>
                                                    <td>{{ endstation }}</td>
                                                    <td>{{ item['departuretime'] }}</td>
                                                    <td>{{ item['arrivaltime'] }}</td>
                                                    <td>{{ item['businessclass']['num']}}</td>
                                                    <td>{{ item['firstclass']['num'] }}</td>
                                                    <td>{{ item['economyclass']['num'] }}</td>
                                                    <td>{{ item['softsleeper']['num'] }}</td>
                                                    <td>{{ item['hardsleeper']['num'] }}</td>
                                                    <td>{{ item['softseat']['num'] }}</td>
                                                    <td>{{ item['hardseat']['num'] }}</td>
                                                    <td>0</td>
                                                    <td><button @click="change(index)">改签</button></td>
                                                 </tr>
                                            </tbody>
                                        </table>
                                  </div>
                              
                        
                            <div class="container row" style="margin-top: 300px">
                            
                                 <table class="table table-hover" style="width: 1000px">
                                            <thead>
                                                <tr>
                                                    <th>日期</th>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>到达站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>单价</th>
                                                   
                                                </th>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                   
                                                    <td>{{ date }}</td>
                                                    <td>{{ train_id }}</td>
                                                    <td>{{ startstation }}</td>
                                                    <td>{{ endstation }}</td>
                                                    <td>{{ departuretime }}</td>
                                                    <td>{{ arrivaltime }}</td>
                                                    <td>{{ pay }}</td>
                                                    
                                                 </tr>
                                            </tbody>
                                        </table>
                                    <select v-model="seat_style" class="selectpicker show-tick" title="类型" data-live-search="true" data-size="20">
                                                <option>商务座</option>
                                                <option>一等座</option>
                                                <option>二等座</option>
                                                <option>软卧</option>
                                                <option>硬卧</option>
                                                <option>软座</option>
                                                <option>硬座</option>
                                    </select>
                                   
                              
                               
                            </div>
                            <div class="container row">
                             
                                    <form @submit.prevent="submit" style="width: 500px">
                                        
                                        <div class="form-group">
                                            <button type="submit" class="btn btn-primary btn-block">确认</button>
                                        </div>
                                    </form>
                                    
                            
                            </div>
                        </div>
                    </div>
                </div>
                
            `,


            data() {
                return {

                    year:"2018",
                    month:"5",
                    day:"1",

                    date: null,

                    train_id: null,

                    startstation: null,
                    endstation: null,
                    departuretime: null,
                    arrivaltime: null,
                    pay: null,
                    index_select:null,
                    seat_style:"硬座",
                    style:"hardseat",

                    passenger_id:null,

                    search_data:null,

                    old_preplot_id:null,
                    old_ticket_id:null,


                }
            },

            created(){
                this.old_preplot_id = this.$route.params['preplot_id'];
                this.old_ticket_id = this.$route.params['ticket_id']
                this.startstation=this.$route.params['startstation'];
                this.endstation = this.$route.params['endstation'];
                this.passenger_id = this.$route.params['passenger']


            },
            methods:{

                search(){

                 console.log('查询')
                 var self = this
                    $.ajax({
                        url:'/api/v1/searchdirect/',
                        type:'Post',
                        data:{
                          date:this.year+'-'+this.month+'-'+this.day,
                          startstation:this.startstation,
                          endstation:this.endstation,
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.search_data = data.data;
                                console.log(self.search_data.valueOf('train_id'))
                            }else {
                                alert(data.message)
                            }

                        }
                    })
                },

                change(index){
                    this.index_select = index;
                    this.train_id = this.search_data[index]['train_id']
                    console.log(this.train_id)
                    this.date = this.year+"-"+this.month+"-"+this.day;
                    console.log(this.date)
                    this.departuretime = this.search_data[index]['departuretime']
                    this.arrivaltime = this.search_data[index]['arrivaltime']
                    this.pay = this.search_data[index]['hardseat']['pay']
                },

                submit(){
                    var self = this
                    if(this.seat_style=="硬座"){
                       this.style="hardseat";
                    }

                     $.ajax({
                        url:'/api/v1/change',
                        type:'Post',
                        data: {
                            date: this.date,
                            train_id: this.train_id,
                            startstation: this.startstation,
                            endstation: this.endstation,
                            departuretime: this.departuretime,
                            arrivaltime: this.arrivaltime,
                            pay: this.pay,
                            carriage_id: this.search_data[this.index_select][this.style]['queue'][0]['carriage_id'],
                            seat: this.search_data[this.index_select][this.style]['queue'][0]['seat'],
                            passenger_id: this.passenger_id,
                            old_ticket_id:this.old_ticket_id,
                            old_preplot_id:this.old_preplot_id,
                             },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                alert(data.message)
                                self.$router.push({name: 'preplot_manage',});
                            }else {
                                alert(data.message)
                            }

                        }
                    })



                }
            },

        },

    },
    {
        path: '/order_ticket',
        name: 'order_ticket',
        component: {
            template: `
                <div class="container">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="list-group side-bar">
                                <router-link class="list-group-item" to="/">首页</router-link>
                                <router-link class="list-group-item active" to="/search_left_ticket">余票查询</router-link>
                                <router-link class="list-group-item" to="/preplot_manage">订单管理</router-link>
                                <router-link class="list-group-item" to="/mine_info">我的信息</router-link>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="container">
                            
                                 <table class="table table-hover" style="width: 1000px">
                                            <thead>
                                                <tr>
                                                    <th>日期</th>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>到达站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>单价</th>
                                                   
                                                </th>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                   
                                                    <td>{{ date }}</td>
                                                    <td>{{ train_id }}</td>
                                                    <td>{{ startstation }}</td>
                                                    <td>{{ endstation }}</td>
                                                    <td>{{ departuretime }}</td>
                                                    <td>{{ arrivaltime }}</td>
                                                    <td>{{ pay }}</td>
                                                    
                                                 </tr>
                                            </tbody>
                                        </table>
                                    <select v-model="seat_style" class="selectpicker show-tick" title="类型" data-live-search="true" data-size="20">
                                                <option>商务座</option>
                                                <option>一等座</option>
                                                <option>二等座</option>
                                                <option>软卧</option>
                                                <option>硬卧</option>
                                                <option>软座</option>
                                                <option>硬座</option>
                                    </select>
                                   
                              
                               
                            </div>
                            <div class="container">
                                <h1>
                                        预定
                                    </h1>
                                    <form @submit.prevent="submit" style="width: 500px">
                                        <div class="form-group">
                                            <label>身份证号</label>
                                            <input v-model="passenger_id_num" type="text" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <button type="submit" class="btn btn-primary btn-block">确认</button>
                                        </div>
                                    </form>
                            
                            </div>
                        </div>
                    </div>
                </div>
                
            `,


            data() {
                return {
                    date: null,
                    train_id: null,
                    startstation: null,
                    endstation: null,
                    departuretime: null,
                    arrivaltime: null,
                    pay: null,
                    index_select:null,
                    seat_style:"硬座",
                    order_data_select: null,
                    style:"hardseat",
                    passenger_id_num:null,

                }
            },
            created(){
                this.order_data_select = this.$route.params.search_data
                this.index_select = this.$route.params.index
                this.train_id = this.order_data_select[this.index_select]['train_id']
                this.date = this.$route.params.date
                this.startstation = this.$route.params.startstation
                this.endstation =this.$route.params.endstation
                this.departuretime = this.order_data_select[this.index_select]['departuretime']
                this.arrivaltime = this.order_data_select[this.index_select]['arrivaltime']
                this.pay = this.order_data_select[this.index_select]['hardseat']['pay']
            },
            methods:{
                submit(){
                    var self = this
                    if(this.seat_style=="硬座"){
                       this.style="hardseat";
                    }

                     $.ajax({
                        url:'/api/v1/order',
                        type:'Post',
                        data:{
                            date:this.date,
                            train_id:this.train_id,
                            startstation:this.startstation,
                            endstation:this.endstation,
                            departuretime:this.departuretime,
                            arrivaltime:this.arrivaltime,
                            pay:this.pay,
                            data:"[{\"carriage\":"+this.order_data_select[this.index_select][this.style]['queue'][0]['carriage_id']+",\"seat\":"+this.order_data_select[this.index_select][this.style]['queue'][0]['seat']+",\"passenger_id_num\":"+this.passenger_id_num+"},]",

                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.$router.push({name: 'preplot_manage',});
                            }else {
                                alert(data.message)
                            }

                        }
                    })



                }
            },

        },

    },
    {
        path: '/transfer_ticket',
        name: 'transfer_ticket',
        component: {
            template: `
                <div class="container">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="list-group side-bar">
                                <router-link class="list-group-item" to="/">首页</router-link>
                                <router-link class="list-group-item active" to="/search_left_ticket">余票查询</router-link>
                                <router-link class="list-group-item" to="/preplot_manage">订单管理</router-link>
                                <router-link class="list-group-item" to="/mine_info">我的信息</router-link>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="container">
                            
                                 <table class="table table-hover" style="width: 1000px">
                                            <thead>
                                                <tr>
                                                    <th>日期</th>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>到达站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>单价</th>
                                                   
                                                </th>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                   
                                                    <td>{{ date }}</td>
                                                    <td>{{ train_id }}</td>
                                                    <td>{{ startstation }}</td>
                                                    <td>{{ endstation }}</td>
                                                    <td>{{ departuretime }}</td>
                                                    <td>{{ arrivaltime }}</td>
                                                    <td>{{ pay }}</td>
                                                    
                                                 </tr>
                                            </tbody>
                                        </table>
                                    <select v-model="seat_style" class="selectpicker show-tick" title="类型" data-live-search="true" data-size="20">
                                                <option>商务座</option>
                                                <option>一等座</option>
                                                <option>二等座</option>
                                                <option>软卧</option>
                                                <option>硬卧</option>
                                                <option>软座</option>
                                                <option>硬座</option>
                                    </select>
                                   
                              
                               
                            </div>
                            <div class="container">
                                <h1>
                                        预定
                                    </h1>
                                    <form @submit.prevent="submit" style="width: 500px">
                                        <div class="form-group">
                                            <label>身份证号</label>
                                            <input v-model="passenger_id_num" type="text" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <button type="submit" class="btn btn-primary btn-block">确认</button>
                                        </div>
                                    </form>
                            
                            </div>
                        </div>
                    </div>
                </div>
                
            `,


            data() {
                return {
                    date: null,
                    train_id: null,
                    startstation: null,
                    endstation: null,
                    departuretime: null,
                    arrivaltime: null,
                    pay: null,
                    index_select:null,
                    seat_style:"硬座",
                    order_data_select: null,
                    style:"hardseat",
                    passenger_id_num:null,

                }
            },
            created(){
                this.order_data_select = this.$route.params.search_data
                this.index_select = this.$route.params.index
                this.train_id = this.order_data_select[this.index_select]['train_id']
                this.date = this.$route.params.date
                this.startstation = this.$route.params.startstation
                this.endstation =this.$route.params.endstation
                this.departuretime = this.order_data_select[this.index_select]['departuretime']
                this.arrivaltime = this.order_data_select[this.index_select]['arrivaltime']
                this.pay = this.order_data_select[this.index_select]['hardseat']['pay']
            },
            methods:{
                submit(){
                    var self = this
                    if(this.seat_style=="硬座"){
                       this.style="hardseat";
                    }

                     $.ajax({
                        url:'/api/v1/order',
                        type:'Post',
                        data:{
                            date:this.date,
                            train_id:this.train_id,
                            startstation:this.startstation,
                            endstation:this.endstation,
                            departuretime:this.departuretime,
                            arrivaltime:this.arrivaltime,
                            pay:this.pay,
                            data:"[{\"carriage\":"+this.order_data_select[this.index_select][this.style]['queue'][0]['carriage_id']+",\"seat\":"+this.order_data_select[this.index_select][this.style]['queue'][0]['seat']+",\"passenger_id_num\":"+this.passenger_id_num+"},]",

                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.$router.push({name: 'home',params: {user_id:this.user_id}});
                                self.$emit('get_user',self.user_id)
                            }else {
                                alert(data.message)
                            }

                        }
                    })



                }
            },

        },

    },
    {

        path:'/',
        name:'home',
        component:{
            template:`
                <div class="container">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="list-group side-bar">
                                <router-link class="list-group-item active" to="/">首页</router-link>
                                <router-link class="list-group-item" to="/search_left_ticket">余票查询</router-link>
                                <router-link class="list-group-item" to="/preplot_manage">订单管理</router-link>
                                <router-link class="list-group-item" to="/mine_info">我的信息</router-link>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div class="container">
                               
                            </div>
                        </div>
                    </div>
                </div>
                
            `,
        },
    },
    {
        path:'/login',
        name:'login',
        component:{
            template : ` 
                            <div class="container login" >
                                <div class="form-container">
                                    <h1>
                                        登录
                                        <small>没有账号？<router-link to="/register">注册</router-link> </small>
                                    </h1>
                                    <form @submit.prevent="submit">
                                        <div class="form-group">
                                            <label>用户名</label>
                                            <input v-model="user_id" type="text" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <label>密码</label>
                                            <input v-model="passwd" type="password" class="form-control">    
                                        </div>
                                        <div class="form-group">
                                            <button type="submit" class="btn btn-primary btn-block">登录</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                    `,
            data:function(){
                return{
                    user_id:'',
                    passwd:'',
                    re_data:'',
                }
            },
            methods:{
                submit(){
                    var self = this
                    $.ajax({
                        url:'/api/v1/login',
                        type:'Post',
                        data:{
                            user_id:this.user_id,
                            passwd:this.passwd,
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.$emit('get_user',self.user_id);
                                self.$router.push({name: 'home',params: {user_id:self.user_id}});
                            }else {
                                alert(data.message)
                            }

                        }
                    })
                }
            }
        }
    },

    {
        path:'/register',
        component:{
            template:`
                            <div class="container login">
                                <div class="form-container">
                                    <h1>
                                        注册
                                    </h1>
                                    <form @submit.prevent="submit">
                                        <div class="form-group">
                                            <label>用户名</label>
                                            <input v-model="user_id" type="text" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <label>密码</label>
                                            <input v-model="passwd" type="password" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <label>姓名</label>
                                            <input v-model="user_name" type="text" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <label>身份证号</label>
                                            <input v-model="id_num" type="test" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <label>邮箱</label>
                                            <input v-model="email" type="email" class="form-control">
                                        </div>
                                        <div class="form-group">
                                            <label>电话</label>
                                            <input v-model="phone" type="text" class="form-control">
                                        </div>
                                        <p>忘记密码？</p>
                                        <div class="form-group">
                                            <button type="submit" class="btn btn-primary btn-block">登录</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
             `,
            data(){
                return{
                    user_id:'',
                    passwd:'',
                    user_name:'',
                    id_num:'',
                    email:'',
                    phone:'',
                }
            },
            methods:{
                submit(){
                    var self = this
                    $.ajax({
                        url:'/api/v1/register',
                        type:'Post',
                        data:{
                            user_id:this.user_id,
                            passwd:this.passwd,
                            user_name:this.user_name,
                            id_num:this.id_num,
                            email:this.email,
                            phone:this.phone,
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.$router.push({name: 'home',params: {user_id:this.user_id}});
                                self.$emit('get_user',self.user_id)
                            }else {
                                alert(data.message)
                            }

                        }
                    })

                }
            }
        },
    },

    {
      path:'/search_left_ticket',
      component:{
          template:`
                <div class="container">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="list-group side-bar">
                                <router-link class="list-group-item" to="/">首页</router-link>
                                <router-link class="list-group-item active" to="/search_left_ticket">余票查询</router-link>
                                <router-link class="list-group-item" to="/preplot_manage">订单管理</router-link>
                                <router-link class="list-group-item" to="/mine_info">我的信息</router-link>
                            </div>
                        </div>
                        <div class="col-md-8">
                              <div class="row clearfix">
                                    <div class = "date-station">
                                          <select v-model="year" class="selectpicker show-tick" title="年份" data-live-search="true" data-size="20">
                                                <option>2018</option>
                                                <option>2017</option>
                                                <option>2016</option>
                                                <option>2015</option>
                                                <option>2013</option>
                                                <option>2012</option>
                                                <option>2011</option>
                                          </select>
                                          <label>年</label>
                                          <select v-model="month" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                               <option>1</option>
                                               <option>2</option>
                                               <option>3</option>
                                               <option>4</option>
                                               <option>5</option>
                                               <option>6</option>
                                               <option>7</option>
                                               <option>8</option>
                                               <option>9</option>
                                               <option>10</option>
                                               <option>11</option>
                                               <option>12</option>
                                          </select>
                                          <label>月</label>
                                          <select v-model="day" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                                <option>1</option>
                                                <option>2</option>
                                                <option>3</option>
                                                <option>4</option>
                                                <option>5</option>
                                                <option>6</option>
                                                <option>7</option>
                                                <option>8</option>
                                                <option>9</option>
                                                <option>10</option>
                                                <option>11</option>
                                                <option>12</option>
                                                <option>13</option>
                                                <option>14</option>
                                                <option>15</option>
                                                <option>16</option>
                                                <option>17</option>
                                                <option>18</option>
                                                <option>19</option>
                                                <option>20</option>
                                                <option>21</option>
                                                <option>22</option>
                                                <option>23</option>
                                                <option>24</option>
                                                <option>25</option>
                                                <option>26</option>
                                                <option>27</option>
                                                <option>28</option>
                                                <option>29</option>
                                                <option>30</option>
                                                <option>31</option>
                                          </select>
                                          <label>日</label>
                                          <label>始发站</label>
                                           <select v-model="startstation" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                               <option>北京站</option>
                                               <option>上海站</option>
                                               <option>威海站</option>
                                               <option>深圳站</option>
                                               <option>广州站</option>
                                               <option>烟台站</option>
                                               <option>济南站</option>
                                               <option>青岛站</option>
                                             
                                          </select>
                                           <label>终点站</label>
                                           <select v-model="endstation" class="selectpicker show-tick" title="月分" data-live-search="true" data-size="20">
                                               <option>北京站</option>
                                               <option>上海站</option>
                                               <option>威海站</option>
                                               <option>深圳站</option>
                                               <option>广州站</option>
                                               <option>烟台站</option>
                                               <option>济南站</option>
                                               <option>青岛站</option>
                                          </select>
                                          <label style="margin-left: 100px">出行方式</label>
                                          <select v-model="out_style" class="selectpicker show-tick" title="方式" data-live-search="true" data-size="20">
                                               <option>直达</option>
                                               <option>中转</option>
                                               
                                          </select>
                                       
                                          <button v-if="out_style=='直达'" style="margin-left: 1000px;background-color: #1b9dec;width: 100px" @click="search" class="btn btn-block">查询</button>
                                          <button v-else style="margin-left: 1000px;background-color: #1b9dec;width: 100px" @click="transfer_search" class="btn btn-block">查询</button>

                              </div>     
                              <div class="container">
                              
                                  <div v-if="out_style=='直达'">
                                        <table class="table table-hover" style="width: 1000px">
                                            <thead>
                                                <tr>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>到达站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>商务座</th>
                                                    <th>一等座</th>
                                                    <th>二等座</th>
                                                    <th>软卧</th>
                                                    <th>硬卧</th>
                                                    <th>软座</th>
                                                    <th>硬座</th>
                                                    <th>无座</th>
                                                    <th>操作</th>
                                                </th>
                                            </thead>
                                            <tbody>
                                                <tr v-for="(item,index) in search_data">
                                                    <td>{{ item['train_id'] }}</td>
                                                    <td>{{ startstation }}</td>
                                                    <td>{{ endstation }}</td>
                                                    <td>{{ item['departuretime'] }}</td>
                                                    <td>{{ item['arrivaltime'] }}</td>
                                                    <td>{{ item['businessclass']['num']}}</td>
                                                    <td>{{ item['firstclass']['num'] }}</td>
                                                    <td>{{ item['economyclass']['num'] }}</td>
                                                    <td>{{ item['softsleeper']['num'] }}</td>
                                                    <td>{{ item['hardsleeper']['num'] }}</td>
                                                    <td>{{ item['softseat']['num'] }}</td>
                                                    <td>{{ item['hardseat']['num'] }}</td>
                                                    <td>0</td>
                                                    <td><button @click="order(index)">预定</button></td>
                                                 </tr>
                                            </tbody>
                                        </table>
                                  </div>
                                  
                                  <div v-else>
                                        <table class="table table-hover" style="width: 1000px">
                                            <thead>
                                                <tr>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>到达站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>商务座</th>
                                                    <th>一等座</th>
                                                    <th>二等座</th>
                                                    <th>软卧</th>
                                                    <th>硬卧</th>
                                                    <th>软座</th>
                                                    <th>硬座</th>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>到达站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>商务座</th>
                                                    <th>一等座</th>
                                                    <th>二等座</th>
                                                    <th>软卧</th>
                                                    <th>硬卧</th>
                                                    <th>软座</th>
                                                    <th>硬座</th>
                                                    <th>操作</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                    <tr v-for="(item,index) in search_data">
                                                        <td>{{ item['train_id_first'] }}</td>
                                                        <td>{{ startstation }}</td>
                                                        <td>{{ item['transferstation_id'] }}</td>
                                                        <td>{{ item['departuretime_first'] }}</td>
                                                        <td>{{ item['arrivaltime_first'] }}</td>
                                                        <td>{{ item['ticket_info'][0]['businessclass']['num']}}</td>
                                                        <td>{{ item['ticket_info'][0]['firstclass']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][0]['economyclass']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][0]['softsleeper']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][0]['hardsleeper']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][0]['softseat']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][0]['hardseat']['num'] }}</td>
                                                        <td>{{ item['train_id_second'] }}</td>
                                                        <td>{{ item['transferstation_id'] }}</td>
                                                        <td>{{ endstation }}</td>
                                                        <td>{{ item['departuretime_second'] }}</td>
                                                        <td>{{ item['arrivaltime_second'] }}</td>
                                                        <td>{{ item['ticket_info'][1]['businessclass']['num']}}</td>
                                                        <td>{{ item['ticket_info'][1]['firstclass']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][1]['economyclass']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][1]['softsleeper']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][1]['hardsleeper']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][1]['softseat']['num'] }}</td>
                                                        <td>{{ item['ticket_info'][1]['hardseat']['num'] }}</td>
                                                        <td><button @click="transfer(index)">预定</button></td>

                                                     </tr>
                                            </tbody>
                                        </table>
                                  </div>


                              </div>
                        </div>
                    </div>
                </div>
            `,
           data(){
                return{

                    year: 2018,
                    month: 5,
                    day: 1,
                    startstation: "深圳站",
                    endstation: "北京站",
                    search_data: null,
                    date: null,
                    out_style: "直达",
                }
            },
           methods:{
              order(index){
                //     this.order_data_select = this.$route.params.search_data
                // this.index_select = this.$route.params.index
                // this.date = this.$route.params.date
                // this.startstation = this.$route.params.startstation
                // this.endstation =this.$route.params.endstation
                // this.departuretime = this.order_data_select[this.index_select]['departuretime']
                // this.arrvialtime = this.order_data_select[this.index_select]['arrvialtime']
                // this.pay = this.order_data_select[this.index_select]['hardseat']['pay']

                  this.$router.push({name:'order_ticket',
                  params:{
                      search_data:this.search_data,
                      startstation:this.startstation,
                      endstation:this.endstation,
                      index:index,
                      date:this.year+'-'+this.month+'-'+this.day
                  }});
                  console.log(index)

              },

               tranfer(index){

                  this.$router.push({name:'transfer_ticket',params:{
                      // train_id_first:search_data[index]['train_id_first'],
                      // train_id_second:search_data[index]['train_id_second'],
                      // startstation:this.startstation,
                      // transferstation:search_data[index]['transferstation_id'],
                      // endstation:this.endstation,
                      // departuretime_first:search_data[index]['departuretime_first'],
                      // arrivaltime_first:search_data[index]['arrivaltime_first'],
                      // departuretime_second:search_data[index]['departuretime_second'],
                      // arrivaltime_second:search_data[index]['arrivaltime_second'],

                      order_data:this.search_data,

                      }});
                  console.log(index)

              },

              search(){
                 console.log('查询')
                 var self = this
                    $.ajax({
                        url:'/api/v1/searchdirect/',
                        type:'Post',
                        data:{
                          date:this.year+'-'+this.month+'-'+this.day,
                          startstation:this.startstation,
                          endstation:this.endstation,
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.search_data = data.data;
                                console.log(self.search_data.valueOf('train_id'))
                            }else {
                                alert(data.message)
                            }

                        }
                    })
                },
                transfer_search(){
                 console.log('查询')
                 var self = this
                    $.ajax({
                        url:'/api/v1/searchtransfer/',
                        type:'Post',
                        data:{
                          date:this.year+'-'+this.month+'-'+this.day,
                          startstation:this.startstation,
                          endstation:this.endstation,
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.search_data = data.data;
                            }else {
                                alert(data.message)
                            }

                        }
                    })
              },

           }
      },
    },

    {
        path:'/preplot_manage',
        component:{
            template:`
                <div class="container">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="list-group side-bar">
                                <router-link class="list-group-item" to="/">首页</router-link>
                                <router-link class="list-group-item" to="/search_left_ticket">余票查询</router-link>
                                <router-link class="list-group-item active" to="/preplot_manage">订单管理</router-link>
                                <router-link class="list-group-item" to="/mine_info">我的信息</router-link>
                            </div>
                        </div>
                        <div class="col-md-8">
                             <div class="container">
                                  <div>
                                        <table class="table table-hover" style="width: 1000px">
                                            <thead>
                                                <tr>
                                                    <th>订单号</th>
                                                    <th>日期</th>
                                                    <th>票号</th>
                                                    <th>车次</th>
                                                    <th>出发站</th>
                                                    <th>终点站</th>
                                                    <th>出发时间</th>
                                                    <th>到达时间</th>
                                                    <th>乘客</th>
                                                    <th>金额</th>
                                                    <th>有效</th>
                                                    <th>退款</th>
                                                    <th>支付</th>
                                                    <th>结账</th>
                                                    <th>操作</th>
                                                    <th>改签</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                
                                                <tr v-for="(item,index) in preplot_data">
                                                    <td>{{ item['preplot_id'] }}</td>
                                                    <td>{{ item['date'] }}</td>
                                                    <td>{{ item['ticket'][0]['ticket_id'] }}</td>
                                                    <td>{{ item['ticket'][0]['train_id']}}</td>
                                                    <td>{{ item['ticket'][0]['startstation'] }}</td>
                                                    <td>{{ item['ticket'][0]['endstation'] }}</td>
                                                    <td>{{ item['ticket'][0]['departuretime'] }}</td>
                                                    <td>{{ item['ticket'][0]['arrivaltime'] }}</td>
                                                    <td>{{ item['ticket'][0]['passenger'] }}</td>
                                                    <td>{{ item['ticket'][0]['pay'] }}</td>
                                                    <td>{{ item['ticket'][0]['is_valid'] }}</td>
                                                    <td>{{ item['ticket'][0]['is_refund'] }}</td>
                                                    <td>{{ item['is_paid'] }}</td>
                                                    <td><button @click="pay(index)">支付</button></td>
                                                    <td><button @click="refund(index)">退款</button></td>
                                                    <td><button @click="change(index)">改签</button></td>
                                                 </tr>
                                            </tbody>
                                        </table>
                                  </div>
                        </div>
                    </div>
                </div>
            `,
            data(){
                return{
                    preplot_data:null,
                }
            },
            methods:{
                change(index){

                    this.$router.push({name:'change',
                  params:{
                      preplot_id:this.preplot_data[index]['preplot_id'],
                      ticket_id:this.preplot_data[index]['ticket'][0]['ticket_id'],
                      startstation:this.preplot_data[index]['ticket'][0]['startstation'],
                      endstation:this.preplot_data[index]['ticket'][0]['endstation'],
                      passenger:this.preplot_data[index]['ticket'][0]['passenger']
                  }});



                }
                ,
                pay(index){

                    var self = this
                    $.ajax({
                        url:'/api/v1/pay/',
                        type:'Post',
                        data:{
                          preplot_id:this.preplot_data[index]['preplot_id'],
                          pay:this.preplot_data[index]['total_pay']
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                alert(data.message)
                                self.$router.push({name: 'preplot_manage',});
                            }else {
                                alert(data.message)
                            }

                        }
                    })


                },
                refund(index){
                    console.log('执行');
                    var self = this
                    $.ajax({
                        url:'/api/v1/refund/',
                        type:'Post',
                        data:{
                          preplot_id:this.preplot_data[index]['preplot_id'],
                          ticket_id:this.preplot_data[index]['ticket'][0]['ticket_id'],
                          pay:this.preplot_data[index]['total_pay']
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                alert(data.message)
                                self.$router.push({name: 'preplot_manage',});
                            }else {
                                alert(data.message)
                            }

                        }
                    })

                },
            },
            created(){
                console.log('订单')
                 var self = this
                    $.ajax({
                        url:'/api/v1/preplot/',
                        type:'Get',
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.preplot_data = data.data;
                            }else {
                                alert(data.message)
                            }

                        }
                    })
            }
        },
    },

    {
        path:'/mine_info',
        component:{
            template:`
                <div class="container">
                    <div class="row">
                        <div class="col-md-2">
                            <div class="list-group side-bar">
                                <router-link class="list-group-item" to="/">首页</router-link>
                                <router-link class="list-group-item" to="/search_left_ticket">余票查询</router-link>
                                <router-link class="list-group-item" to="/preplot_manage">订单管理</router-link>
                                <router-link class="list-group-item active" to="/mine_info">我的信息</router-link>
                            </div>
                        </div>
                        <div class="col-md-8">
                            <div>
                                <ul>
                                    <li>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">用户名</label>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">{{ user_id }}</label>
                                    </li>
                                    <li>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">姓名</label>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">{{ user_name }}</label>
                                    </li>
                                    <li>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">身份证号</label>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">{{ id_num }}</label>
                                    </li>
                                    <li>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">邮箱</label>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">{{ email }}</label>
                                    </li>
                                    <li>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">电话</label>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">{{ phone }}</label>
                                    </li>
                                      <li>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">money</label>
                                    <label style="margin-left: 50px;margin-right: 50px;margin-bottom: 50px;color: cornflowerblue">{{ money }}</label>
                                    </li>
                                </ul>
                            </div>
                            <div>
                                <button @click="clicked">充值</button>
                            </div>
                            <div v-if="recharge_flag==true" class="form-container">
                            
                                <form @submit.prevent="recharge_submit" style="width: 500px">
                                    <div class="form-group">
                                            <label>金额</label>
                                            <input v-model="cash" type="number" class="form-control">
                                    </div>
                                    <div class="form-group">
                                            <button type="submit" class="btn btn-primary btn-block">提交</button>
                                    </div>
                                </form>
                                        
                            </div>
                        </div>
                    </div>
                </div>
            `,
            data() {
                return {
                    cash:0,
                    recharge_flag: false,
                    user_id: null,
                    user_name: null,
                    id_num: null,
                    email: null,
                    phone: null,
                    money: 0,
                }
            },
            created(){
                console.log('sdaf')
                 var self = this
                    $.ajax({
                        url:'/api/v1/user/',
                        type:'Get',
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.phone = data.data.phone;
                                self.user_id = data.data.user_id;
                                self.user_name = data.data.user_name;
                                self.money = data.data.money;
                                self.id_num = data.data.id_num;
                                self.email = data.data.email;
                                self.$emit('get_user',self.user_id)
                            }else {
                                alert(data.message)
                            }

                        }
                    })
            }
            ,
            methods:{

                clicked(){
                    console.log('调用');
                    console.log(this.recharge_flag)
                    if(this.recharge_flag){
                        this.recharge_flag=false;
                    }else {
                        this.recharge_flag = true ;

                    }

                },
                recharge_submit(){

                    console.log('充值成功')
                    var self = this
                    $.ajax({
                        url:'/api/v1/recharge/',
                        type:'Post',
                        data:{
                            money:this.cash,
                        },
                        dataType:'json',
                        success:function (data) {
                            if(data.status == 200){
                                console.log(data);
                                self.money=data.data.money
                            }else {
                                alert(data.message)
                            }

                        }
                    })
                }
            }
        },
    },
];


var router = new VueRouter({
    routes:routes
});

var app = new Vue({
    el:'#app',
    router:router,
    data(){
        return{
            flag:false,
            page:0,
            user_id:null,
            passwd:null,
            status:null,
            message:null,
            data:null,
        }
    },
    methods:{
        clicked_logout(){
          this.$router.push({name:'/',});
          location.reload();
        },
        get_user_id(val){
            console.log(val);
            self.user_id = val;
            console.log(self.user_id);
            console.log(self.user_id);
            this.flag = true;

        }
    }

});