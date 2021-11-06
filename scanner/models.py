from django.db import models
from datetime import date
from slugify import slugify
import random
import string
from django.db.models.signals import post_save
import uuid


# Create your models here.

class Dependency(models.Model):  # this is a generic challenge model where all challenges are picked up from.
    dependency_name = models.CharField(max_length=70, blank=True, null=True, unique=True)
    dependency_language = models.CharField(max_length=70, blank=True, null=True)  # the language under which we found the repo
    dependency_url = models.URLField(max_length=300, blank=True, null=True, unique=True)  # the location where we find more info for this dependency (PyPi for Python)
    dependency_license = models.CharField(max_length=70, blank=True, null=True)
    dependency_license_last_checked_date = models.DateField(blank=True, null=False, default=date.today)

    def __str__(self):
        return self.dependency_name

    class Meta:
        unique_together = ('dependency_name', 'dependency_language')



class Scanned_Repo(models.Model):  # this is a generic challenge model where all challenges are picked up from.
    repo_id = models.UUIDField(default=uuid.uuid4, unique=False)  # unique ID which I use to control the organization creation/editing if someone changes the name of the program
    repo_store = models.CharField(max_length=70, blank=True, null=True)  # the repository store of the repo (github, gitlab etc...)
    repo_name = models.CharField(max_length=70, blank=True, null=True, unique=True)
    repo_primary_language = models.CharField(max_length=70, blank=True, null=True)
    repo_url = models.URLField(max_length=300, blank=True, null=True, unique=True) 
    repo_is_private = models.BooleanField(default=False)
    repo_license = models.CharField(max_length=70, blank=True, null=True)
    repo_last_checked_date = models.DateField(blank=True, null=True)
    repo_scan_error = models.BooleanField(default=False)
    repo_scan_error_message = models.CharField(max_length=70, blank=True, null=True, default = "")

    def __str__(self):
        return self.repo_name

    class Meta:
        unique_together = ('repo_name', 'repo_store')


class Repo_Dependency_Pair(models.Model):
    repo = models.ForeignKey(Scanned_Repo, related_name='repo', null=False, blank=False, on_delete=models.CASCADE)
    dependency = models.ForeignKey(Dependency, related_name='dependency', null=False, blank=False, on_delete=models.CASCADE)
    date_scanned = models.DateField(verbose_name="Date Scanned", auto_now_add=True)

    def __str__(self):
        return self.repo.repo_name