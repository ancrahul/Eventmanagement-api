# Generated by Django 3.2.8 on 2021-10-28 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_eventsjoined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='creator',
            field=models.CharField(max_length=200),
        ),
    ]