# Generated by Django 3.2.5 on 2021-07-18 13:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repo_Dependency_Pair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_scanned', models.DateTimeField(auto_now_add=True, verbose_name='Date Scanned')),
            ],
        ),
        migrations.CreateModel(
            name='Scanned_Repo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo_store', models.CharField(blank=True, max_length=70, null=True)),
                ('repo_name', models.CharField(blank=True, max_length=70, null=True, unique=True)),
                ('repo_primary_language', models.CharField(blank=True, max_length=70, null=True)),
                ('repo_url', models.URLField(blank=True, max_length=300, null=True, unique=True)),
                ('repo_is_private', models.BooleanField(default=False)),
                ('repo_license', models.CharField(blank=True, max_length=70, null=True)),
                ('repo_last_checked_date', models.DateField(blank=True, default=datetime.date.today)),
            ],
            options={
                'unique_together': {('repo_name', 'repo_store')},
            },
        ),
        migrations.DeleteModel(
            name='Repo',
        ),
        migrations.RenameField(
            model_name='dependency',
            old_name='license_last_checked_date',
            new_name='dependency_license_last_checked_date',
        ),
        migrations.AddField(
            model_name='dependency',
            name='dependency_url',
            field=models.URLField(blank=True, max_length=300, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='dependency',
            name='dependency_language',
            field=models.CharField(blank=True, max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='repo_dependency_pair',
            name='dependency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependency', to='scanner.dependency'),
        ),
        migrations.AddField(
            model_name='repo_dependency_pair',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repo', to='scanner.scanned_repo'),
        ),
    ]
