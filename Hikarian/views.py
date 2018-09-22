from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from common.auth.userSystem import userSystem,makepassword,checkpassword,md5
from django.http import JsonResponse
from django.db.models import F,Q
from Hikarian.common import affair
from datetime import datetime
import redis

# Create your tests here.
import hashlib
import time
from Hikarian import models

# Create your views here.
re = redis.StrictRedis(host='127.0.0.1',port='6379',db=0)


@never_cache
def hasLoggedIn(request):
    '''
    判断用户是否在线的一个函数
    目前划不清楚用途
    :param request:
    :return:
    '''
    pass

def login(request):
    '''
    登陆函数
    :param request: POST
        {
        ’user_id':
        'passwd':
    }
    :return:
                {
        'status':
        'message':
    }

    '''
    # 判断request.method
    if request.method == 'GET':
        # 重定向到 登陆界面
        return redirect('/api/v1/login/')

    elif request.method == 'POST':

        # 获取用户 账户 和 密码
        user_id = request.POST.get('user_id')
        passwd = request.POST.get('passwd')
        print(user_id)
        print(passwd)
        # 获取user对象
        user = userSystem(request)
        # user登陆 认证
        # 判定新用户登陆 顶替旧的用户
        if user.getUsername() != user_id:
            user.delCache()
            # 清理 session
            request.session.flush()

        error = user.authentication(user_id=user_id, passwd=passwd)
        # error为空 则登陆成功
        # error不为空 则登陆不成功
        if not error:
            return JsonResponse({
                'status': 200,
                'message': 'OK',
                'data': {
                }

            })
        else:
            return JsonResponse({
                'status': 202,
                'message': error,
                'data': {
                }
            })


def logout(request):
    '''
        账号 登出
        :param request:
        :return:
                {
        'status':
        'message':
       }

        '''
    # 清理缓存
    user = userSystem(request)
    user.delCache()
    # 清理 session
    request.session.flush()

    return JsonResponse({
        'status': 200,
        'message': 'OK',
    })

def register(request):
    '''
    用户注册
    :param request:POST
        {
        'user_id':
        'passwd':
        'user_name':
        'id_num':
        'email':
        'phone'
    }
    :return:
        {
        'status':
        'message':
    }

    '''
    # 错误信息列表
    error = ''

    # 后台获取并判断用户名和密码 是否为空
    user_id = request.POST.get('user_id')
    passwd = request.POST.get('passwd')

    # 正则判断 账号密码等正则信息
    if user_id is None or passwd is None:
        error = 'The user_id & passwd cannot be empty'
        # 获取并判断 用户名是否存在
    else:
        if not models.userInfo.objects.filter(Q(user_id=user_id) & Q(is_delete=False)).exists():
            passwd = makepassword(user_id,passwd)
            user_name = request.POST.get('user_name')
            id_num = request.POST.get('id_num')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            print('zhixingle')
            # 调用 model类的 新建对象方法 存储用户对象
            models.userInfo.userInfoObject(user_id,passwd,user_name,id_num,email,phone)
            # 返回 json
            print('---------------------')
            return JsonResponse({
                'status': 200,
                'message': 'OK',
            })
        else:
                error = 'Username already exists'

    return JsonResponse({
        'status': 202,
        'message': error,
    })


def user_splitter(request,GET=None,POST=None):
    '''
    获取用户信息 分流器
    根据 request.method 分配方法
    GET:view.userGET
    POST:view.userPOST
    :param request: GET \\ POST
        {

    }
    :return:

    '''
    # 错误信息列表
    error = ''
    if request.method == 'GET' and GET is not None:
        return GET(request)
    elif request.method == 'POST' and POST is not None:
        return POST(request)
    else:
        error = 'request.method is WRONG'

@never_cache
def userGET(request):
    '''
    显示用户信息
    :param request:
    :return:
    '''
    # 错误信息列表
    error = ''
    assert request.method == 'GET'
    # 获取用户对象
    user_id = request.GET.get('user_id')
    if user_id:
        user = models.userInfo.objects.get_or_none(user_id=user_id)
    else:
        user = models.userInfo.objects.get_or_none(user_id=userSystem(request).getUsername())

    if user is not None:

        return JsonResponse({

            'status': 200,
            'message': 'SUCCESS',
            'data': {
                'user_id': user.user_id,
                'user_name': user.user_name,
                'id_num': user.id_num,
                'email': user.email,
                'phone':user.phone,
                'money':user.money,

            }
        })
    else:
        error = 'user is not exist'
        return JsonResponse({
            'status': 202,
            'message': error
        })


@never_cache
def userPOST(request):
    '''
    修改用户信息
    :param request: POST
    :return:

    '''
    # 错误信息列表
    error = ''
    assert request.method == 'POST'

    user = models.userInfo.objects.get_or_none(user_id=userSystem(request).getUsername())

    if user:
        user.user_name = request.POST.get('user_name', user.user_name)
        user.phone = request.POST.get('phone', user.phone)
        user.email = request.POST.get('email', user.email)
        user.id_num = request.POST.get('id_num', user.id_num)
    else:
        error = 'user is not exist.'
        return JsonResponse(
            {
                'status': 202,
                'message': error,
            }
        )

    # 保存 修改
    user.save()

    return JsonResponse({
        'status': 200,
        'message': 'SUCCESS'
    })


def recharge(request):
    '''

    :param request: POST
        {
        'money':xxx
    }
    :return:
    '''

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        cash = request.POST.get('money')
        user = models.userInfo.objects.get_or_none(user_id=userSystem(request).getUsername())
        user.money += int(cash)
        user.save()
        return JsonResponse({
            'status': 200,
            'message': 'SUCCESS',
            'data': {
                'money':user.money,
            }
        })


def searchdirect(request):
    '''

    :param request:
    :return:
               {
                'status':200,
                'message':'OK',
                'data':
                    [
                        {
                            'train_id':everytrain.train_id,
                            'departuretime':xxxxx,
                            'arrivaltime':xxxxx,
                            'businessclass': {
                                'num': ticket_left[0],
                                'pay':xxxx,
                                'queue': ticket_queue[0]

                            },
                            'firstclass':{
                                'num': ticket_left[1],
                                'pay':xxxx,
                                'queue': ticket_queue[1]
                            },
                            'economyclass':{
                                'num': ticket_left[2],
                                'pay':xxxx,
                                'queue': ticket_queue[2]
                            },
                            'softsleeper':{
                                'num': ticket_left[3],
                                'pay':xxxx,
                                'queue': ticket_queue[3]
                            },
                            'hardsleeper':{
                                'num': ticket_left[4],
                                'pay':xxxx,
                                'queue': ticket_queue[4]
                            },
                            'softseat':{
                                'num': ticket_left[5],
                                'pay':xxxx,
                                'queue': ticket_queue[5]

                            },
                            'hardseat':{
                                'num': ticket_left[6],
                                'pay':xxxx,
                                'queue': ticket_queue[6]
                            }
                        },

                        ........

                    ]
            }
    '''

    error = ''

    if request.method == 'GET':
        return redirect('/api/v1/order')
    elif request.method == 'POST':

        startstation = request.POST.get('startstation')
        endstation = request.POST.get('endstation')
        date = request.POST.get('date')

        print(startstation, endstation, date)

        # 后台验证 确保收到的一定不是空值
        if startstation and endstation and date:

            train_ticket_left = []
            # 直达方式 余票
            train_possiable = affair.searchTrain_Direct(startstation, endstation)
            for everytrain in train_possiable:

                # 初始化 一个车票剩余 数组
                # 商务座 一等座 二等座 软卧 硬卧 软座 硬座 无座
                ticket_left = [0, 0, 0, 0, 0, 0, 0, 0]
                ticket_queue = [[], [], [], [], [], [], [], []]
                ticket_pay = [0, 0, 0, 0, 0, 0, 0, 0]

                # 获取当前车次的 车厢 和 经停信息 用数组表示
                carriageArray = affair.searchTrainCarriage(everytrain.train_id.train_id)
                stationArray = affair.searchTrainStation(everytrain.train_id.train_id)
                # 获取始发站 终点站的站点位置
                start_site, end_site, distance_relative = affair.get_location(startstation,endstation,stationArray)
                #计算站点距离，以计算车票价格


                # 计算每一个车厢的余票
                '''
                车厢0
                    车站1 车站2 车站3
                座位1
                座位2
                座位3

                '''
                site_station_matrix = []
                carriage_type_list = [0 for _ in range(len(carriageArray))]
                for everycarriage in carriageArray:
                    # 初始化 座次-车站 矩阵
                    # 初始化 车厢类型对应表
                    # 初始化 出票队列
                    index = int(everycarriage.carriage_id.type)
                    carriage_type_list[carriageArray.index(everycarriage)] = int(everycarriage.carriage_id.type)
                    site_station_matrix.append([[0 for _ in range(len(stationArray))]for _ in range(everycarriage.carriage_id.seat_num)])
                    # 计算价格
                    if ticket_pay[index] == 0:
                        ticket_pay[index] = ticket_pay[index] + distance_relative*everycarriage.carriage_id.unit_price

                # 获取 当前车次 当天 车票预定信息
                ticketArray = affair.searchTrainTicketSaled(everytrain.train_id.train_id, date)
                for everyticket in ticketArray:
                    start, end = affair.get_location(everyticket[startstation], everyticket[endstation], stationArray)

                    site_station_matrix[everyticket['carriagenum']][everyticket['sitenum']][start] = 1
                    site_station_matrix[everyticket['carriagenum']][everyticket['sitenum']][end] = 1


                # 获取 当前车次 当天 余票信息
                # 每个车厢
                for each_carriage in site_station_matrix:
                    # 每个座位
                    seat = 0
                    for each_seat in each_carriage:

                        if affair.is_available(start_site, end_site, each_seat):
                            type = carriage_type_list[site_station_matrix.index(each_carriage)]
                            ticket_left[type] += 1
                            if len(ticket_queue[type]) < 11:
                                ticket_queue[type].append(
                                    {
                                        'carriage_id': carriageArray[site_station_matrix.index(each_carriage)].carriage_id.carriage_id,
                                        'seat': seat
                                    }
                                )
                        seat += 1


                train_ticket_left.append(
                    {
                        'train_id': everytrain.train_id.train_id,
                        'departuretime': everytrain.train_id.departuretime,
                        'arrivaltime': everytrain.train_id.arrivaltime,

                        'businessclass': {
                            'num': ticket_left[0],
                            'pay': ticket_pay[0],
                            'queue': ticket_queue[0]

                        },
                        'firstclass': {
                            'num': ticket_left[1],
                            'pay': ticket_pay[1],
                            'queue': ticket_queue[1]
                        },
                        'economyclass': {
                            'num': ticket_left[2],
                            'pay': ticket_pay[2],
                            'queue': ticket_queue[2]
                        },
                        'softsleeper': {
                            'num': ticket_left[3],
                            'pay': ticket_pay[3],
                            'queue': ticket_queue[3]
                        },
                        'hardsleeper': {
                            'num': ticket_left[4],
                            'pay': ticket_pay[4],
                            'queue': ticket_queue[4]
                        },
                        'softseat': {
                            'num': ticket_left[5],
                            'pay': ticket_pay[5],
                            'queue': ticket_queue[5]

                        },
                        'hardseat': {
                            'num': ticket_left[6],
                            'pay': ticket_pay[6],
                            'queue': ticket_queue[6]
                        },
                    }
                )

            print(train_ticket_left)
            return JsonResponse(
                {
                    'status': 200,
                    'message': 'OK',
                    'data': train_ticket_left,
                }
            )

        else:
            error = 'Please check your commit message : startstation & endstation & date'

            return JsonResponse(
                {
                    'status': 202,
                    'message': error,
                }
            )

def searchtransfer(request):
    '''

    :param request:
    :return: {
                'status':200,
                'message':OK,
                'data':[
                         {
                            'train_id_first':xxxxx,
                            'departuretime_first':xxxxx,
                            'transferstation_id':xxxxx,
                            'arrivaltime_first':xxxxx,
                            'departuretime_second':xxxxx,
                            'train_id_second':xxxxx,
                            'arrivaltime_second':xxxxx,
                            'ticket_info':[
                                {
                                    'businessclass': {
                                        'num': ticket_left[0],
                                        'pay':xxxx,
                                        'queue': ticket_queue[0]

                                    },
                                    'firstclass':{
                                        'num': ticket_left[1],
                                        'pay':xxxx,
                                        'queue': ticket_queue[1]
                                    },
                                    'economyclass':{
                                        'num': ticket_left[2],
                                        'pay':xxxx,
                                        'queue': ticket_queue[2]
                                    },
                                    'softsleeper':{
                                        'num': ticket_left[3],
                                        'pay':xxxx,
                                        'queue': ticket_queue[3]
                                    },
                                    'hardsleeper':{
                                        'num': ticket_left[4],
                                        'pay':xxxx,
                                        'queue': ticket_queue[4]
                                    },
                                    'softseat':{
                                        'num': ticket_left[5],
                                        'pay':xxxx,
                                        'queue': ticket_queue[5]

                                    },
                                    'hardseat':{
                                        'num': ticket_left[6],
                                        'pay':xxxx,
                                        'queue': ticket_queue[6]
                                    }
                                }
                                ,
                                {
                                    'businessclass': {
                                        'num': ticket_left[0],
                                        'pay':xxxx,
                                        'queue': ticket_queue[0]

                                    },
                                    'firstclass':{
                                        'num': ticket_left[1],
                                        'pay':xxxx,
                                        'queue': ticket_queue[1]
                                    },
                                    'economyclass':{
                                        'num': ticket_left[2],
                                        'pay':xxxx,
                                        'queue': ticket_queue[2]
                                    },
                                    'softsleeper':{
                                        'num': ticket_left[3],
                                        'pay':xxxx,
                                        'queue': ticket_queue[3]
                                    },
                                    'hardsleeper':{
                                        'num': ticket_left[4],
                                        'pay':xxxx,
                                        'queue': ticket_queue[4]
                                    },
                                    'softseat':{
                                        'num': ticket_left[5],
                                        'pay':xxxx,
                                        'queue': ticket_queue[5]

                                    },
                                    'hardseat':{
                                        'num': ticket_left[6],
                                        'pay':xxxx,
                                        'queue': ticket_queue[6]
                                    }
                                },
                         },

                            ........

                        ]


                    }

    '''
    error = ''
    if request.method == 'GET':
        redirect('/')
    elif request.method == 'POST':

        startstation = request.POST.get('startstation')
        endstation = request.POST.get('endstation')

        date = request.POST.get('date')

        if startstation and endstation and date:

            # 中转方式 中转一次
            result = []

            # 获取经过起点的车辆
            # 获取经过终点的车辆
            trainstartArray = affair.searchTrain_Pass(startstation)
            trainendArray = affair.searchTrain_Pass(endstation)
            # 寻找 转乘 车辆
            for everytrain in trainstartArray:
                print(everytrain.train_id)
                startstationArray = affair.searchTrainStation(everytrain.train_id)
                # 对 当前车次的每一个车站 进行匹配
                for transfer_station_to_select in startstationArray:

                    select_now_loc, startloc, distance_relative_first = affair.get_location(transfer_station_to_select.startstation_id, startstation, startstationArray)
                    if select_now_loc > startloc:

                        for transfertrain in trainendArray:

                            endstationArray = affair.searchTrainStation(transfertrain.train_id)

                            for station in endstationArray:
                                transferloc, endloc, distance_relative_second = affair.get_location(station.startstation_id, endstation, endstationArray)
                                if transferloc < endloc \
                                        and transfer_station_to_select.startstation_id == station.startstation_id \
                                        and transfer_station_to_select.departuretime < station.departuretime:

                                        transfer_ticket_first = affair.get_ticket_left_between_station(everytrain.train_id.train_id,startstation,station.startstation_id, date)
                                        transfer_ticket_second = affair.get_ticket_left_between_station(transfertrain.train_id.train_id,station.startstation_id,endstation, date)

                                        result.append(
                                            {

                                                'train_id_first': everytrain.train_id.train_id,
                                                'departuretime_first': everytrain.train_id.departuretime,
                                                'arrivaltime_first': everytrain.train_id.arrivaltime,
                                                'train_id_second': transfertrain.train_id.train_id,
                                                'departuretime_second': transfertrain.train_id.departuretime,
                                                'arrivaltime_second': transfertrain.train_id.arrivaltime,
                                                'transferstation_id': station.startstation_id,
                                                'ticket_info': [
                                                        transfer_ticket_first,
                                                        transfer_ticket_second,
                                                    ]
                                            }
                                        )

            return JsonResponse(
                {
                    'status': 200,
                    'message': 'OK',
                    'data': result,
                }
            )


        else:

            error = 'Please check your commit message : startstation & endstation & date'
            return JsonResponse(
                {
                    'status': 202,
                    'message': error,
                }
            )


def order(request):
    '''

    如果时间更改的话 就需要加个字段，来计算时间

    ticket_id
    train_id
    startstation
    endstation
    carriage_id
    site
    pay
    departuretime
    arrivaltime
    is_valid

    preplot_id
    user_id
    date = mod
    is_paid

    :param request: POST
    {
        'date':2018-5-16,
        'train_id':G3
        'startstation':2
        'endstation':8
        'departuretime':05:06
        'arrivaltime':17:56
        'pay':5000
        'data':[
               {
                    'carriage_id':21,
                   'seat':0,
                 'passenger_id_num':130521199803077773,
                },
            ]
    }
    :return:
    '''

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        # 获取票的详细信息
        train_id = request.POST.get('train_id')
        startstation = models.stationInfo.objects.get_or_none(station_id=request.POST.get('startstation'))
        endstation = models.stationInfo.objects.get_or_none(station_id=request.POST.get('endstation'))
        pay = request.POST.get('pay')
        date = request.POST.get('date')
        departuretime = date + request.POST.get('departuretime')
        arrivaltime = date + request.POST.get('arrivaltime')

        data = request.POST.get('data')
        # 形成订单
        owner = models.userInfo.objects.get_or_none(user_id=userSystem(request).getUsername())
        preplot_id = md5(time.strftime('%M:%S'))
        preplot = models.preplot.preplotObject(preplot_id, owner, date)


        for each_person in eval(data):

            carriage_id = each_person.get('carriage_id')
            seat = each_person.get('seat')
            passenger_id_num = each_person.get('passenger_id_num')

            #形成票
            train = models.trainInfo.objects.get_or_none(train_id=train_id)
            print(train_id)
            print(train)
            carriage = models.carriageInfo.objects.get_or_none(carriage_id=carriage_id)
            # carriage_num = models.trainCarriage.objects.filter(Q(train_id=train) & Q(carriage_id=carriage))[0].carriage_num
            ticket_id = md5(time.strftime('%M:%S'))
            passenger = models.userInfo.objects.get_or_none(id_num=passenger_id_num)

            ticket = models.ticketInfo.ticketInfoObject(ticket_id, train, carriage, seat, pay, startstation, endstation, datetime.strptime(departuretime, '%Y-%m-%d%H:%M'), datetime.strptime(arrivaltime, '%Y-%m-%d%H:%M'))
            #形成绑定信息
            models.ticketPreplot.ticketPreplotObject(preplot, ticket, passenger)

        return JsonResponse({
            'status': 200,
            'message': 'SUCCESS',
        })

def refund(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        preplot_id = request.POST.get('preplot_id')


def pay(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'GET':
        pass
    elif request.method == 'POST':

        preplot_id = request.POST.get('preplot_id')
        preplot = models.preplot.objects.get_or_none(preplot_id=preplot_id)
        ticket = models.ticketInfo.objects.get_or_none(ticket_id=preplot.ticket_id)
        if ticket.is_vaild:
            money = ticket.money
            user = models.userInfo.objects.get_or_none(user_id=userSystem(request).getUserObject())
            user.money -= money
            user.save()
        return JsonResponse({
            'status': 200,
            'message': 'OK',
        })


def change(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass

def prelot(request):

    if request.method == 'GET':
        user = models.userInfo.objects.get_or_none(userSystem(request).getUserObject())
