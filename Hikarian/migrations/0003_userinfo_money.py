# Generated by Django 2.0.7 on 2018-09-22 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hikarian', '0002_auto_20180918_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='money',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
