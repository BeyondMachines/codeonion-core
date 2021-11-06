from django.db import models
from datetime import date, datetime
from slugify import slugify
import random
import string
from django.db.models.signals import post_save


# Create your models here.

class Message(models.Model):  # this is a generic challenge model where all challenges are picked up from.
    message_title = models.CharField(max_length=70, blank=True, null=True, unique=True)
    message_text = models.CharField(max_length=250, blank=True, null=True)
    message_created_date = models.DateField(blank=True, null=False, default=date.today)

    def __str__(self):
        return self.message_title
