# coding=utf-8

from Hikarian import models


def searchTrain_Distance(train_id, startstation, endstation,):
    '''
    获取某车次经停某车站和某车站之间的距离
    :param train_id:
    :param startstation:
    :param endstation:
    :return:
    '''
    sql = 'select id,distance from hikarian_traintostation ' \
            'where  train_id_id = %s ' \
            'and (startstation_id = %s or startstation_id = %s)' % [train_id,startstation,endstation]

    result = models.trainToStation.objects.raw(sql)

    distance = result[1].distance - result[0].distance

    return distance

def searchTrain_Pass(station):
    '''
    获取 经过 某个车站 的所有车次
    :param station:
    :return:
    '''
    sql = 'select id,train_id_id from hikarian_traintostation ' \
          'where startstation_id = %s' % station

    return list(models.trainToStation.objects.raw(sql))

def searchTrain_Direct(startstation,endstation):
    '''
    获取直达方式下
    待定选择的车次
    :param startstation:
    :param endstation:
    :return:
    '''
    sql = 'select id,train_id_id from hikarian_traintostation ' \
          'where startstation_id = %s ' \
          'and train_id_id in ( select train_id_id from hikarian_traintostation ' \
                            'where startstation_id = %s)' % (startstation,endstation)

    return list(models.trainToStation.objects.raw(sql))

def searchTrainStation(train_id):
    '''
    获取当前车次的经停信息
    :param train_id:
    :return:
    '''
    sql = 'select id,startstation_id from hikarian_traintostation ' \
          'where train_id_id = \'%s\' order by distance' % train_id
    return list(models.trainToStation.objects.raw(sql))

def searchTrainCarriage(train_id):
    '''
    获取当前车次的车厢数
    :param train_id:
    :return:
    '''
    sql = 'select id,carriage_id_id from hikarian_traincarriage ' \
          'where train_id_id = \'%s\' order by carriage_num' % train_id
    return list(models.trainCarriage.objects.raw(sql))

def searchTrainTicketSaled(train_id,go_date):
    '''
    获取当前车辆已售出的票-》座位，以及 出发终点站
    :param train_id: 列车车次
    :param sale_date: 售票日期
    :return:[
                {
                'startstation':
                'endstation':
                'carriagenum':
                'sitenum':
                },
                ...
            ]
    '''
    print(go_date)
    sql = 'select ticket_id from hikarian_ticketinfo ' \
          'where train_id_id = \'%s\'' % train_id

    ticket_array = models.ticketInfo.objects.raw(sql)
    result = []
    for ticket in ticket_array:
        a= ticket.carriage_id
        b =ticket.site

        result.append(
            {
                'startstation': ticket.startstation,
                'endstation': ticket.endstation,
                'carriagenum': int(a.carriage_id),
                'sitenum': int(b)

            }
        )
    print(result)
    return []

def get_position(station,stationArray):

    for location in range(len(stationArray)):

        if stationArray[location].station_id == station:

            return location

    return None

def get_location(startstation,endstation,stationArray):
    start = 0
    end = 0
    distance_start = 0
    distance_end = 0
    for location in stationArray:

        if location.startstation_id == startstation:
            start = stationArray.index(location)
            distance_start = location.distance
        elif location.startstation_id == endstation:
            end = stationArray.index(location)
            distance_end = location.distance
    return start, end, distance_end - distance_start

def is_available(start, end, site_station_Array):
    flag = True
    for loc in range(start, end+1):
        if site_station_Array[loc] == 1:
            flag = False
            break
    return flag

def get_ticket_left_between_station(train_id, startstation, endstation, date):
    '''

    :param startstation:
    :param endstation:
    :param date:
    :return:
                        {
                            'businessclass': {
                                'num': ticket_left[0],
                                'pay':xxx,
                                'queue': ticket_queue[0]

                            },
                            'firstclass':{
                                'num': ticket_left[1],
                                'pay':xxx,
                                'queue': ticket_queue[1]
                            },
                            'economyclass':{
                                'num': ticket_left[2],
                                'pay':xxx,
                                'queue': ticket_queue[2]
                            },
                            'softsleeper':{
                                'num': ticket_left[3],
                                'pay':xxx,
                                'queue': ticket_queue[3]
                            },
                            'hardsleeper':{
                                'num': ticket_left[4],
                                'pay':xxx,
                                'queue': ticket_queue[4]
                            },
                            'softseat':{
                                'num': ticket_left[5],
                                'pay':xxx,
                                'queue': ticket_queue[5]

                            },
                            'hardseat':{
                                'num': ticket_left[6],
                                'pay':xxx,
                                'queue': ticket_queue[6]
                            },
                        }

    '''
    train_ticket_left = {}

    # 初始化 一个车票剩余 数组
    # 商务座 一等座 二等座 软卧 硬卧 软座 硬座 无座
    ticket_left = [0, 0, 0, 0, 0, 0, 0, 0]
    ticket_queue = [[], [], [], [], [], [], [], []]
    ticket_pay = [0, 0, 0, 0, 0, 0, 0, 0]

    # 获取当前车次的 车厢 和 经停信息 用数组表示
    carriageArray = searchTrainCarriage(train_id)
    stationArray = searchTrainStation(train_id)
    # 获取始发站 终点站的站点位置
    start_site, end_site, distance_relative = get_location(startstation, endstation, stationArray)
    # 计算站点距离，以计算车票价格

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
        site_station_matrix.append(
            [[0 for _ in range(len(stationArray))] for _ in range(everycarriage.carriage_id.seat_num)])
        # 计算价格
        if ticket_pay[index] == 0:
            ticket_pay[index] = ticket_pay[index] + distance_relative * everycarriage.carriage_id.unit_price

    # 获取 当前车次 当天 车票预定信息
    ticketArray = searchTrainTicketSaled(train_id, date)
    for everyticket in ticketArray:
        start, end, d = get_location(everyticket[startstation], everyticket[endstation], stationArray)

        site_station_matrix[everyticket['carriagenum']][everyticket['sitenum']][start] = 1
        site_station_matrix[everyticket['carriagenum']][everyticket['sitenum']][end] = 1

    # 获取 当前车次 当天 余票信息
    # 每个车厢
    for each_carriage in site_station_matrix:
        # 每个座位
        seat = 0
        for each_seat in each_carriage:

            if is_available(start_site, end_site, each_seat):
                type = carriage_type_list[site_station_matrix.index(each_carriage)]
                ticket_left[type] += 1
                if len(ticket_queue[type]) < 11:
                    ticket_queue[type].append(
                        {
                            'carriage_id': carriageArray[
                                site_station_matrix.index(each_carriage)].carriage_id.carriage_id,
                            'seat': seat
                        }
                    )
            seat += 1

    train_ticket_left['businessclass'] = {
                'num': ticket_left[0],
                'pay':ticket_pay[0],
                'queue': ticket_queue[0]

            }
    train_ticket_left['firstclass'] = {
        'num': ticket_left[1],
        'pay': ticket_pay[1],
        'queue': ticket_queue[1]

    }
    train_ticket_left['economyclass'] = {
        'num': ticket_left[2],
        'pay': ticket_pay[2],
        'queue': ticket_queue[2]

    }
    train_ticket_left['softsleeper'] = {
        'num': ticket_left[3],
        'pay': ticket_pay[3],
        'queue': ticket_queue[3]

    }
    train_ticket_left['hardsleeper'] = {
        'num': ticket_left[4],
        'pay': ticket_pay[4],
        'queue': ticket_queue[4]

    }
    train_ticket_left['softseat'] = {
        'num': ticket_left[5],
        'pay': ticket_pay[5],
        'queue': ticket_queue[5]

    }
    train_ticket_left['hardseat'] = {
        'num': ticket_left[6],
        'pay': ticket_pay[6],
        'queue': ticket_queue[6]

    }

    return train_ticket_left

def get_preplot(user):
    '''
    获取用户的订单信息
    :param user:
    :return:
    [


    ]
    '''

    preplot = list(models.preplot.objects.filter(user_id=user))

    preplot_list = []
    for each_preplot in preplot:
        total_pay = 0

        preplot_dic = {}

        preplot_dic['preplot_id'] = each_preplot.preplot_id
        preplot_dic['is_paid'] = each_preplot.is_paid
        preplot_dic['date'] = each_preplot.date
        ticket_list = []
        ticket_query_set = list(models.ticketPreplot.objects.filter(preplot_id=each_preplot.preplot_id))

        for each_ticket in ticket_query_set:

            ticket_id = each_ticket.ticket_id
            train_id = ticket_id.train_id
            startstation = ticket_id.startstation
            endstation = ticket_id.endstation
            departuretime = ticket_id.departuretime
            arrivaltime = ticket_id.arrivaltime
            pay = ticket_id.pay
            is_valid = ticket_id.is_valid
            passenger = each_ticket.passenger_id
            is_refund = each_ticket.is_refund

            total_pay = total_pay + pay

            ticket_list.append({
                'ticket_id': ticket_id.ticket_id,
                'train_id': train_id.train_id,
                'startstation': startstation.station_name,
                'endstation': endstation.station_name,
                'departuretime': departuretime,
                'arrivaltime': arrivaltime,
                'passenger': passenger,
                'is_valid': is_valid,
                'is_refund': is_refund,
                'pay': pay
            })

        preplot_dic['ticket'] = ticket_list
        preplot_dic['total_pay'] = total_pay
        preplot_list.append(preplot_dic)
    print(preplot_list)
    return preplot_list







