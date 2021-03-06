# Generated by Django 3.2.5 on 2021-07-18 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_title', models.CharField(blank=True, max_length=70, null=True, unique=True)),
                ('message_text', models.CharField(blank=True, max_length=250, null=True)),
                ('message_created_date', models.DateField(blank=True, default=datetime.date.today)),
            ],
        ),
    ]
