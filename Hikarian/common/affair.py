# coding=utf-8

from Hikarian import models


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


def searchTrainTicketSaled(train_id,sale_date):
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
          'where tarin_id_id = %s and '
