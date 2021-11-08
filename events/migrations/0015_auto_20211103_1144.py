# Generated by Django 3.2.8 on 2021-11-03 06:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20211102_1724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertransaction',
            old_name='created_at',
            new_name='transaction_created_at',
        ),
        migrations.RenameField(
            model_name='usertransaction',
            old_name='event_fees',
            new_name='transaction_event_fees',
        ),
        migrations.RenameField(
            model_name='usertransaction',
            old_name='status',
            new_name='transaction_event_name',
        ),
        migrations.RenameField(
            model_name='userwallet',
            old_name='username',
            new_name='wallet_username',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='event_name',
        ),
        migrations.RemoveField(
            model_name='usertransaction',
            name='username',
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='transaction_type',
            field=models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default=datetime.datetime(2021, 11, 3, 6, 14, 25, 613601, tzinfo=utc), max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertransaction',
            name='transaction_updated_At',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
