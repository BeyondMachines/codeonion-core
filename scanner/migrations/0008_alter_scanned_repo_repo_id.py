# Generated by Django 3.2.5 on 2021-08-04 13:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0007_auto_20210803_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scanned_repo',
            name='repo_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
