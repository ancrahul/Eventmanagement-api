# Generated by Django 3.2.8 on 2021-11-03 06:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20211103_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertransaction',
            name='transaction_username',
            field=models.CharField(default=datetime.datetime(2021, 11, 3, 6, 27, 3, 817248, tzinfo=utc), max_length=300),
            preserve_default=False,
        ),
    ]