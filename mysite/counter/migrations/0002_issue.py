# Generated by Django 2.2.6 on 2019-10-28 22:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('counter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Issue', help_text='Der Titel für diesen Antrag', max_length=256)),
                ('reason', models.TextField(help_text='Der Grund für diesen Antrag')),
                ('honor_change', models.BooleanField(default='True')),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('duration', models.DurationField(default=datetime.timedelta(days=7))),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='created_issues', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issue_targeted_by', to=settings.AUTH_USER_MODEL)),
                ('voted_no', models.ManyToManyField(related_name='voted_no', to=settings.AUTH_USER_MODEL)),
                ('voted_yes', models.ManyToManyField(related_name='voted_yes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
