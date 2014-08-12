# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import datetime
import time


class Phone(models.Model):
    user = models.ForeignKey(User, blank=True ,null=True)
    time = models.CharField(max_length=255, blank=True , null=True)
    brand = models.CharField(max_length=255, blank=True , null=True)
    pattern = models.CharField(max_length=255, blank=True , null=True)
    sn = models.CharField(max_length=255, blank=True , null=True)
    price_in = models.CharField(max_length=255, blank=True , null=True)
    price_out = models.CharField(max_length=255, blank=True , null=True)
    number = models.CharField(max_length=255, blank=True , null=True)
    time_out = models.CharField(max_length=255, blank=True , null=True)
    settled = models.BooleanField(default=False)
    remark = models.CharField(max_length=255, blank=True , null=True)

