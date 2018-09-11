from django.db import models

# Create your models here.


class userInfo(models.Model):

    user_id = models.CharField(max_length=20, unique=True, primary_key=True)
    passwd = models.CharField(max_length=40)
    user_name = models.CharField(max_length=15)
    id_num = models.CharField(max_length=18)
    email = models.CharField(max_length=40)
    phone = models.CharField(max_length=11)
    is_delete = models.BooleanField(default=False)



class stationInfo(models.Model):
    station_id = models.CharField(max_length=10, unique=True, primary_key=True)
    station_name = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    province = models.CharField(max_length=10)



class trainInfo(models.Model):

    train_id = models.CharField(max_length=10, unique=True, primary_key=True)
    train_type = models.CharField(max_length=2)
    startstation = models.ForeignKey(stationInfo, to_field='station_id',related_name='start', on_delete=models.CASCADE)
    endstation = models.ForeignKey(stationInfo, to_field='station_id', on_delete=models.CASCADE)
    departuretime = models.CharField(max_length=20)
    arrivaltime = models.CharField(max_length=20)
    carriagenum = models.IntegerField()
    mail = models.FloatField()



class carriageInfo(models.Model):

    carriage_id = models.CharField(max_length=10, unique=True, primary_key=True)
    type = models.CharField(max_length=5)
    seat_num = models.IntegerField()
    unit_price = models.FloatField()
    ticketOutQueue = models.CharField(max_length=1000)
    ticketInQueue = models.CharField(max_length=1000)



class ticketInfo(models.Model):

    ticket_id = models.CharField(max_length=10, unique=True, primary_key=True)
    tarin_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    carriage_id = models.ForeignKey(carriageInfo, to_field='carriage_id', on_delete=models.CASCADE)
    site = models.CharField(max_length=10)
    pay = models.FloatField()
    departuretime = models.CharField(max_length=20)
    arriveltime = models.CharField(max_length=20)
    issuingstation = models.ForeignKey(stationInfo, to_field='station_id', on_delete=models.CASCADE)



class trainToStation(models.Model):

    train_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    startstation = models.ForeignKey(stationInfo, to_field='station_id', related_name='startstation', on_delete=models.CASCADE)
    endstation = models.ForeignKey(stationInfo, to_field='station_id', on_delete=models.CASCADE)
    departuretime = models.CharField(max_length=20)
    arrivaltime = models.CharField(max_length=20)
    distance = models.FloatField()



class trainCarriage(models.Model):

    train_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    carriage_id = models.ForeignKey(carriageInfo, to_field='carriage_id', on_delete=models.CASCADE)
    carriage_num = models.IntegerField()



class ticketPreplot(models.Model):

    preplot_id = models.CharField(max_length=10, unique=True, primary_key=True)
    ticket_id = models.ForeignKey(ticketInfo, to_field='ticket_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey(userInfo, to_field='user_id', on_delete=models.CASCADE)
    date = models.CharField(max_length=20)
    is_paid = models.BooleanField(default=False)

class ticketRefund(models.Model):

    preplot_id = models.ForeignKey(ticketPreplot, to_field='preplot_id', on_delete=models.CASCADE)
    refund  = models.FloatField()
    is_success = models.BooleanField(default=False)

class trainSiteStatistics(models.Model):

    train_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    site_matrix = models.CharField(max_length=1000)
    site_num = models.IntegerField()

class trainSiteAssignment(models.Model):

    train_id = models.ForeignKey(trainInfo, to_field='train_id', on_delete=models.CASCADE)
    sale_date = models.DateTimeField()
    site_assign_matrix = models.CharField(max_length=1000)





    