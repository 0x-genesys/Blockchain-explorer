# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class input_table(models.Model):
    transaction_hash = models.CharField(max_length=500,null=False)
    transaction_index = models.CharField(max_length=20,null=False)
    input_script = models.CharField(max_length=200, null=False)
    input_sequence_number = models.CharField(max_length=20, null=False)
    input_size = models.CharField(max_length=200, null=False)
    input_hex = models.CharField(max_length=500, null=False)
# Create your models here.
