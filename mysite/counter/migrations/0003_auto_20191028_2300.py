# Generated by Django 2.2.6 on 2019-10-28 23:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0002_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='creation_date',
            field=models.DateTimeField(auto_now=True, help_text='Erstellt am'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(days=7), help_text='Dauer'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='honor_change',
            field=models.BooleanField(default='True', help_text='Ehre geben'),
        ),
    ]
