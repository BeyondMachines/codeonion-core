# Generated by Django 3.2.5 on 2021-07-23 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0003_alter_scanned_repo_repo_last_checked_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repo_dependency_pair',
            name='date_scanned',
            field=models.DateField(auto_now_add=True, verbose_name='Date Scanned'),
        ),
    ]