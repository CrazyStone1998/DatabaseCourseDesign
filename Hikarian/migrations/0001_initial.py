# Generated by Django 2.0.7 on 2018-09-15 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='carriageInfo',
            fields=[
                ('carriage_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=5)),
                ('seat_num', models.IntegerField()),
                ('unit_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='preplot',
            fields=[
                ('preplot_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('date', models.CharField(max_length=20)),
                ('is_paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='stationInfo',
            fields=[
                ('station_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('station_name', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=10)),
                ('province', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ticketInfo',
            fields=[
                ('ticket_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('site', models.CharField(max_length=10)),
                ('pay', models.FloatField()),
                ('departuretime', models.DateTimeField()),
                ('arrivaltime', models.DateTimeField()),
                ('is_valid', models.BooleanField(default=True)),
                ('carriage_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.carriageInfo')),
                ('endstation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endsite', to='Hikarian.stationInfo')),
                ('issuingstation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.stationInfo')),
                ('startstation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='startsite', to='Hikarian.stationInfo')),
            ],
        ),
        migrations.CreateModel(
            name='ticketPreplot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preplot_id', models.CharField(max_length=10)),
                ('ticket_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ticketRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund', models.FloatField()),
                ('is_success', models.BooleanField(default=False)),
                ('preplot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.preplot')),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.ticketInfo')),
            ],
        ),
        migrations.CreateModel(
            name='trainCarriage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carriage_num', models.IntegerField()),
                ('carriage_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.carriageInfo')),
            ],
        ),
        migrations.CreateModel(
            name='trainInfo',
            fields=[
                ('train_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('train_type', models.CharField(max_length=2)),
                ('departuretime', models.TimeField()),
                ('arrivaltime', models.TimeField()),
                ('carriagenum', models.IntegerField()),
                ('stationnum', models.IntegerField()),
                ('mail', models.FloatField()),
                ('endstation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.stationInfo')),
                ('startstation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start', to='Hikarian.stationInfo')),
            ],
        ),
        migrations.CreateModel(
            name='trainToStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departuretime', models.TimeField(max_length=20)),
                ('duration', models.IntegerField(default=0)),
                ('distance', models.FloatField()),
                ('startstation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.stationInfo')),
                ('train_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.trainInfo')),
            ],
        ),
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('passwd', models.CharField(max_length=40)),
                ('user_name', models.CharField(max_length=15)),
                ('id_num', models.CharField(max_length=18)),
                ('email', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=11)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='traincarriage',
            name='train_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.trainInfo'),
        ),
        migrations.AddField(
            model_name='ticketpreplot',
            name='passenger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.userInfo'),
        ),
        migrations.AddField(
            model_name='ticketinfo',
            name='train_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.trainInfo'),
        ),
        migrations.AddField(
            model_name='preplot',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hikarian.userInfo'),
        ),
    ]
