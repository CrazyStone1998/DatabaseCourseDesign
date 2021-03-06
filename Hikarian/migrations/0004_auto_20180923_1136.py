# Generated by Django 2.0.7 on 2018-09-23 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hikarian', '0003_userinfo_money'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketpreplot',
            options={'verbose_name': '订单绑定信息', 'verbose_name_plural': '订单绑定信息'},
        ),
        migrations.AlterModelOptions(
            name='traincarriage',
            options={'verbose_name': '车厢组成', 'verbose_name_plural': '车厢组成'},
        ),
        migrations.AlterModelOptions(
            name='traintostation',
            options={'verbose_name': '经停信息', 'verbose_name_plural': '经停信息'},
        ),
        migrations.AddField(
            model_name='ticketpreplot',
            name='is_refund',
            field=models.BooleanField(default=False),
        ),
    ]
