from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from common.auth.userSystem import userSystem,makepassword,checkpassword,md5
from django.http import JsonResponse
from django.db.models import F,Q
from Hikarian.common import affair
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
    :param request:
    :return:
    '''
    # 判断request.method
    if request.method == 'GET':
        # 重定向到 登陆界面
        return redirect('/api/v1/login/')

    elif request.method == 'POST':

        # 获取用户 账户 和 密码
        user_id = request.POST.get('user_id')
        passwd = request.POST.get('passwd')
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
    '''
    # 清理缓存
    pass

def register(request):

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
        if not models.userInfo.objects.filter(Q(user_id=user_id) & Q(is_Delete=False)).exists():
            passwd = makepassword(user_id,passwd)
            user_name = request.POST.get('user_name')
            id_num = request.POST.get('id_num')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            # 调用 model类的 新建对象方法 存储用户对象
            models.userInfo.userInfoObject(user_id,passwd,user_name,id_num,email,phone)
            # 返回 json
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
    :param request:
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


def searchdirect(request):
    '''

    :param request:
    :return:

    '''

    error = ''

    if request.method == 'GET':
        return redirect('/api/v1/order')
    elif request.method == 'POST':

        startstation = request.POST.get('startstation')
        endstation = request.POST.get('endstation')

        date = request.POST.get('date')
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

                # 获取当前车次的 车厢 和 经停信息 用数组表示
                carriageArray = affair.searchTrainCarriage(everytrain.train_id)
                stationArray = affair.searchTrainStation(everytrain.train_id)
                # 获取始发站 终点站的站点位置
                start_site,end_site = affair.get_location(startstation,endstation,stationArray)
                # 计算每一个车厢的余票

                #初始化 座次-车站 矩阵
                #初始化 车厢类型对应表
                #初始化 出票队列
                '''
                车厢0
                    车站1 车站2 车站3
                座位1
                座位2
                座位3
                
                '''
                site_station_matrix = []
                carriage_type_list = []
                for everycarriage in carriageArray:
                    carriage_type_list[carriageArray.index(everycarriage)] = int(everycarriage.type)
                    site_station_matrix.append([[[0]for _ in range(len(stationArray))]for _ in range(everycarriage.site_num)])

                # 获取 当前车次 当天 车票预定信息
                ticketArray = affair.searchTrainTicketSaled(everytrain.train_id, date)
                for everyticket in ticketArray:
                    start,end = affair.get_location(everyticket[startstation],everyticket[endstation],stationArray)

                    site_station_matrix[everyticket['sitenum']][everyticket['carriagenum']][start] = 1
                    site_station_matrix[everyticket['sitenum']][everyticket['carriagenum']][end] = 1

                # 获取 当前车次 当天 余票信息
                for each_carriage in site_station_matrix:
                    for each_site in each_carriage:
                        if affair.is_available(start_site,end_site,each_site):
                            type = carriage_type_list[site_station_matrix.index(each_carriage)]
                            ticket_left[type] += 1
                            if len(ticket_queue[type]) < 11:
                                ticket_queue[type].append(
                                    {
                                        'carriage_id': carriageArray[site_station_matrix.index(each_carriage)].carriage_id,
                                        'site': each_carriage.index(each_site)
                                    }
                                )



                train_ticket_left.append(
                    {
                        'train_id':everytrain.train_id,
                        'businessclass': {
                            'num': ticket_left[0],
                            'queue': ticket_queue[0]

                        },
                        'firstclass':{
                            'num': ticket_left[1],
                            'queue': ticket_queue[1]
                        },
                        'economyclass':{
                            'num': ticket_left[2],
                            'queue': ticket_queue[2]
                        },
                        'softsleeper':{
                            'num': ticket_left[3],
                            'queue': ticket_queue[3]
                        },
                        'hardsleeper':{
                            'num': ticket_left[4],
                            'queue': ticket_queue[4]
                        },
                        'softseat':{
                            'num': ticket_left[5],
                            'queue': ticket_queue[5]

                        },
                        'hardseat':{
                            'num': ticket_left[6],
                            'queue': ticket_queue[6]
                        },
                    }
                )

            return JsonResponse(
                {
                    'status':200,
                    'message':'OK',
                    'data':train_ticket_left,
                }
            )

        else:
            error = 'Please check your commit message : startstation & endstation & date'

            return JsonResponse(
                {
                    'status':202,
                    'message':error,
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
        redirect('/api/v1/login')
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

            for everytrain in trainstartArray:

                startstationArray = affair.searchTrainStation(everytrain.train_id)

                for transger_station_to_select in startstationArray:
                    select_now_loc, startloc = affair.get_location(transger_station_to_select.station_id, startstation, startstationArray)
                    if select_now_loc > startloc:

                        for transfertrain in trainendArray:

                            endstationArray = affair.searchTrainStation(transfertrain.train_id)

                            for station in endstationArray:
                                transferloc,endloc = affair.get_location(station.station_id,endstation,endstationArray)
                                if transferloc < endloc \
                                        and transger_station_to_select.station_id == station.station_id:

                                        transfer_ticket_first = affair.get_ticket_left_between_station(everytrain.train_id,startstation,station.station_id,date)
                                        transfer_ticket_second = affair.get_ticket_left_between_station(transfertrain.train_id,station.station_id,endstation,date)

                                        result.append(
                                            {
                                                'train_id_first':everytrain.train_id,
                                                'train_id_second':transfertrain.train_id,
                                                'transferstation_id':station.station_id,
                                                'ticket_info':[
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

    :param request:
    :return:
    '''

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        # 获取票的详细信息
        train_id = request.POST.get('train_id')
        startstation = request.POST.get('startstation')
        endstation = request.POST.get('endstation')
        carriage_id = request.POST.get('carriage_id')
        site = request.POST.get('site')
        pay = request.POST.get('pay')
        departuretime = request.POST.get('departuretime')
        arrivaltime = request.POST.get('arrivaltime')
        date = request.POST.get('date')
        passenger_id = request.POST.get('passenger')

        #形成票
        train = models.trainInfo.objects.get_or_none(train_id=train_id)
        carriage = models.carriageInfo.objects.get_or_none(carriage_id=carriage_id)
        ticket_id = md5(time.strftime('%M:%S'))
        ticket = models.ticketInfo.ticketInfoObject(ticket_id,train,carriage,site,pay,departuretime,arrivaltime)

        #形成订单
        passenger = models.userInfo.objects.get_or_none(id_num=passenger_id)
        preplot_id = md5(time.strftime('%M:%S'))
        preplot = models.preplot.preplotObject(preplot_id,passenger,date)

        #形成绑定信息
        models.ticketPreplot.ticketPreplotObject(preplot,ticket,passenger)



def refund(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        preplot_id = request.POST.get('preplot_id')


def pay(request):
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
            'status':200,
            'message':'OK',
        })


def change(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass

def prelot(request):

    if request.method == 'GET':
        user = models.userInfo.objects.get_or_none(userSystem(request).getUserObject())
