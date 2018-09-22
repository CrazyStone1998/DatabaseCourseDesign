from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection,transaction
# Create your models here.

cursor = connection.cursor()

'''
select 

'''

class hikarianManager(models.Manager):
    def get_or_none(self,**kwargs):
        '''
        定义 get_or_none
        该方法 当get对象不存在时返回none
        :param kwargs:
        :return:
        '''
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class userInfo(models.Model):


    user_id = models.CharField(max_length=20, unique=True, primary_key=True)
    passwd = models.CharField(max_length=40)
    user_name = models.CharField(max_length=15)
    id_num = models.CharField(max_length=18)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=11)
    money = models.IntegerField()
    is_delete = models.BooleanField(default=False)

    objects = hikarianManager()

    @classmethod
    def userInfoObject(cls, user_id, passwd, user_name, id_num, email=None, phone=None,money = 0):

        new = userInfo()

        new.user_id = user_id
        new.passwd = passwd
        new.user_name = user_name
        new.id_num = id_num
        new.email = email
        new.phone = phone
        new.money = money

        new.save()

        return new

class stationInfo(models.Model):

    station_id = models.CharField(max_length=10, unique=True, primary_key=True)
    station_name = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    province = models.CharField(max_length=10)

    objects = hikarianManager()

    @classmethod
    def stationInfoObject(cls,station_id,station_name,city,province):

        new = stationInfo()
        new.station_id = station_id
        new.station_name = station_name
        new.city = city
        new.province = province

        new.save()
        return new

    def __str__(self):
        return self.station_name

class trainInfo(models.Model):

    train_id = models.CharField(max_length=10, unique=True, primary_key=True)
    train_type = models.CharField(max_length=2)
    startstation = models.ForeignKey(stationInfo, to_field='station_id',related_name='start', on_delete=models.CASCADE)
    endstation = models.ForeignKey(stationInfo, to_field='station_id', on_delete=models.CASCADE)
    departuretime = models.TimeField()
    arrivaltime = models.TimeField()
    carriagenum = models.IntegerField()
    stationnum = models.IntegerField()
    mail = models.FloatField()

    objects = hikarianManager()

    @classmethod
    def trainInfoObject(cls,train_id,train_type,startstation,endstation,departuretime,arrivaltime,carriagenum,stationnum,mail):

        new = trainInfo()
        new.train_id = train_id
        new.train_type = train_type
        new.startstation = startstation
        new.endstation = endstation
        new.departuretime = departuretime
        new.arrivaltime = arrivaltime
        new.carriagenum = carriagenum
        new.stationnum = stationnum
        new.mail = mail

        new.save()
        return new
    def __str__(self):

        return self.train_id

class carriageInfo(models.Model):

    carriage_id = models.CharField(max_length=10, unique=True, primary_key=True)
    type = models.CharField(max_length=5)
    seat_num = models.IntegerField()
    unit_price = models.FloatField()

    objects = hikarianManager()

    @classmethod
    def carriageInfoObject(cls,carriage_id,type,seat_num,unit_price,):

        new = carriageInfo()

        new.carriage_id = carriage_id
        new.type = type
        new.seat_num = seat_num
        new.unit_price = unit_price

        new.save()
        return new

    def __str__(self):

        return self.carriage_id

class ticketInfo(models.Model):

    ticket_id = models.CharField(max_length=10, unique=True, primary_key=True)
    train_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    startstation = models.ForeignKey(stationInfo, to_field='station_id', related_name='startsite', on_delete=models.CASCADE)
    endstation = models.ForeignKey(stationInfo, to_field='station_id',related_name='endsite', on_delete=models.CASCADE)
    carriage_id = models.ForeignKey(carriageInfo, to_field='carriage_id', on_delete=models.CASCADE)
    site = models.CharField(max_length=10)
    pay = models.FloatField()
    departuretime = models.DateTimeField()
    arrivaltime = models.DateTimeField()
    is_valid = models.BooleanField(default=True)

    objects = hikarianManager()

    @classmethod
    def ticketInfoObject(cls, ticket_id, train_id, carriage_id, site, pay, startstation, endstation, departuretime, arrivaltime):

        new = ticketInfo()

        new.ticket_id = ticket_id
        new.train_id = train_id
        new.startstation = startstation
        new.endstation = endstation
        new.carriage_id = carriage_id
        new.site = site
        new.pay = pay
        new.departuretime = departuretime
        new.arrivaltime = arrivaltime

        new.save()

        return new

class trainToStation(models.Model):

    train_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    startstation = models.ForeignKey(stationInfo, to_field='station_id', on_delete=models.CASCADE)
    departuretime = models.TimeField(max_length=20)
    duration = models.IntegerField(default=0)
    distance = models.FloatField()

    objects = hikarianManager()

    class Meta:
        verbose_name = '经停信息'
        verbose_name_plural = '经停信息'

    @classmethod
    def trainToStation(cls,train_id,startstation,departuretime,duration,distance):

        new = trainToStation()
        new.train_id = train_id
        new.startstation = startstation
        new.departuretime = departuretime
        new.duration = duration
        new.distance = distance

        new.save()
        return new

class trainCarriage(models.Model):

    train_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    carriage_id = models.ForeignKey(carriageInfo, to_field='carriage_id', on_delete=models.CASCADE)
    carriage_num = models.IntegerField()

    objects = hikarianManager()

    class Meta:
        verbose_name = '车厢组成'
        verbose_name_plural = '车厢组成'

    @classmethod
    def trainCarriage(cls,train_id,carriage_id,carriage_num):
        new = trainCarriage()
        new.train_id = train_id
        new.carriage_id = carriage_id
        new.carriage_num = carriage_num

        new.save()
        return new

class preplot(models.Model):

    preplot_id = models.CharField(max_length=10, unique=True, primary_key=True)
    user_id = models.ForeignKey(userInfo, to_field='user_id', on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    is_paid = models.BooleanField(default=False)

    objects = hikarianManager()

    @classmethod
    def preplotObject(cls, preplot_id, user_id, date):

        new = preplot()

        new.preplot_id = preplot_id
        new.user_id = user_id
        new.date = date

        new.save()

        return new

class ticketPreplot(models.Model):

    preplot_id = models.ForeignKey(preplot,to_field='preplot_id',on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(ticketInfo,to_field='ticket_id',on_delete=models.CASCADE)
    passenger = models.ForeignKey(userInfo,to_field='user_id',on_delete=models.CASCADE)

    objects = hikarianManager()

    class Meta:

        verbose_name = '订单绑定信息'
        verbose_name_plural = '订单绑定信息'

    @classmethod
    def ticketPreplotObject(cls,preplot_id,ticket_id,passenger):

        new = ticketPreplot()
        new.preplot_id = preplot_id
        new.ticket_id = ticket_id
        new.passenger = passenger

        new.save()
        return new


class ticketRefund(models.Model):

    preplot_id = models.ForeignKey(preplot, to_field='preplot_id', on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(ticketInfo, to_field='ticket_id', on_delete=models.CASCADE)
    refund = models.FloatField()
    is_success = models.BooleanField(default=False)

    objects = hikarianManager()

    @classmethod
    def ticketRefundObject(cls,preplot_id,refund,is_success):

        new = ticketRefund()

        new.preplot_id = preplot_id
        new.refund = refund
        new.is_success = is_success

        new.save()

        return new



    