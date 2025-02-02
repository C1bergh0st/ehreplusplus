# Generated by Django 2.2.7 on 2019-12-17 11:40

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0014_auto_20191127_0950'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ehre', models.IntegerField(default='0')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='counter.UserValues')),
            ],
        ),
    ]
