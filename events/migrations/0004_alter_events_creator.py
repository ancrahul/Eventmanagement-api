# Generated by Django 3.2.8 on 2021-10-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_events_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='creator',
            field=models.CharField(max_length=200),
        ),
    ]
