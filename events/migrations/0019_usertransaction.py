# Generated by Django 3.2.8 on 2021-11-03 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_delete_usertransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=300)),
                ('transaction_username', models.CharField(max_length=300)),
                ('transaction_event_fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_event_name', models.CharField(max_length=300)),
                ('transaction_created_at', models.DateTimeField(auto_now_add=True)),
                ('transaction_updated_At', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
