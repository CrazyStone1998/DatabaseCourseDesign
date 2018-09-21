# coding=utf-8

from Hikarian import models


def searchTrain_Pass(station):
    '''
    获取 经过 某个车站 的所有车次
    :param station:
    :return:
    '''
    sql = 'select train_id_id from hikarian_traintostation ' \
          'where startstation_id = %s'

    return models.trainInfo.objects.raw(sql)

def searchTrain_Direct(startstation,endstation):
    '''
    获取直达方式下
    待定选择的车次
    :param startstation:
    :param endstation:
    :return:
    '''
    sql = 'select train_id_id from hikarian_traintostation ' \
          'where startstation_id = %s and ' \
          'train_id_id in ( select train_id_id ' \
                            'from hikarian_traintostation ' \
                            'where startstation_id = %s)' % [startstation,endstation]

    return models.trainInfo.objects.raw(sql)

def searchTrainStation(train_id):
    '''
    获取当前车次的经停信息
    :param train_id:
    :return:
    '''
    sql = 'select startstation_id from hikarian_traintostation ' \
          'where train_id_id = %s order by departuretime' % train_id

    return models.stationInfo.objects.raw(sql)

def searchTrainCarriage(train_id):
    '''
    获取当前车次的车厢数
    :param train_id:
    :return:
    '''
    sql = 'select carriage_id_id from hikarian_traincarriage ' \
          'where train_id_id = %s order by carriage_num' % train_id

    return models.carriageInfo.objects.raw(sql)


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

    sql = 'select ticket_id from hikarian_ticketinfo ' \
          'where tarin_id_id = %s and convert(departuretime,date) = %s ' \
          'and train_id_id = %s' % [go_date, train_id]

    ticket_array = models.ticketInfo.objects.raw(sql)
    result = []
    for ticket in ticket_array:
        result.append(
            {
                'startstation': ticket.startstation,
                'endstation': ticket.endstation,
                'carrriagenum': ticket.carriagenum,
                'sitenum': ticket.site
            }
        )
    return result

def get_position(station,stationArray):

    for location in range(len(stationArray)):

        if stationArray[location].station_id == station:

            return location

    return None


def get_location(startstation,endstation,stationArray):
    start = 0
    end = 0
    for location in range(len(stationArray)):

        if stationArray[location].station_id == startstation:
            start = location
        elif stationArray[location].station_id == endstation:
            end = location
    return start,end

def is_available(start,end,site_station_Array):
    flag = True

    for loc in range(start,end+1):
        if site_station_Array[loc] == 1:
            flag = False
    return flag

def get_ticket_left_between_station(train_id,startstation,endstation,date):
    '''

    :param startstation:
    :param endstation:
    :param date:
    :return:
                        {
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

    '''
    train_ticket_left = {}

    # 初始化 一个车票剩余 数组
    # 商务座 一等座 二等座 软卧 硬卧 软座 硬座 无座
    ticket_left = [0, 0, 0, 0, 0, 0, 0, 0]
    ticket_queue = [[], [], [], [], [], [], [], []]

    # 获取当前车次的 车厢 和 经停信息 用数组表示
    carriageArray = searchTrainCarriage(train_id)
    stationArray = searchTrainStation(train_id)
    # 获取始发站 终点站的站点位置
    start_site, end_site = get_location(startstation, endstation, stationArray)
    # 计算每一个车厢的余票

    # 初始化 座次-车站 矩阵
    # 初始化 车厢类型对应表
    # 初始化 出票队列
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
        site_station_matrix.append([[[0] for _ in range(len(stationArray))] for _ in range(everycarriage.site_num)])

    # 获取 当前车次 当天 车票预定信息
    ticketArray = searchTrainTicketSaled(train_id, date)
    for everyticket in ticketArray:
        start, end = get_location(everyticket[startstation], everyticket[endstation], stationArray)

        site_station_matrix[everyticket['sitenum']][everyticket['carriagenum']][start] = 1
        site_station_matrix[everyticket['sitenum']][everyticket['carriagenum']][end] = 1

    # 获取 当前车次 当天 余票信息
    for each_carriage in site_station_matrix:
        for each_site in each_carriage:
            if is_available(start_site, end_site, each_site):
                type = carriage_type_list[site_station_matrix.index(each_carriage)]
                ticket_left[type] += 1
                if len(ticket_queue[type]) < 11:
                    ticket_queue[type].append(
                        {
                            'carriage_id': carriageArray[site_station_matrix.index(each_carriage)].carriage_id,
                            'site': each_carriage.index(each_site)
                        }
                    )

    train_ticket_left['businessclass'] = {
                'num': ticket_left[0],
                'queue': ticket_queue[0]

            }
    train_ticket_left['firstclass'] = {
        'num': ticket_left[1],
        'queue': ticket_queue[1]

    }
    train_ticket_left['economyclass'] = {
        'num': ticket_left[2],
        'queue': ticket_queue[2]

    }
    train_ticket_left['softsleeper'] = {
        'num': ticket_left[3],
        'queue': ticket_queue[3]

    }
    train_ticket_left['hardsleeper'] = {
        'num': ticket_left[4],
        'queue': ticket_queue[4]

    }
    train_ticket_left['softseat'] = {
        'num': ticket_left[5],
        'queue': ticket_queue[5]

    }
    train_ticket_left['hardseat'] = {
        'num': ticket_left[6],
        'queue': ticket_queue[6]

    }

    return train_ticket_left