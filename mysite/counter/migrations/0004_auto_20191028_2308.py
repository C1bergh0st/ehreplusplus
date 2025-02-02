# Generated by Django 2.2.6 on 2019-10-28 23:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0003_auto_20191028_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='voted_no',
            field=models.ManyToManyField(blank=True, related_name='voted_no', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='voted_yes',
            field=models.ManyToManyField(blank=True, related_name='voted_yes', to=settings.AUTH_USER_MODEL),
        ),
    ]
