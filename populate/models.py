# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class main_table(models.Model):
    transaction_hash_main = models.CharField(max_length=200, null=False)
    block_height = models.IntegerField(max_length=10, null=True)
    size = models.IntegerField(null=True)
    is_coinbase = models.BooleanField(default=True)
    v_in = models.IntegerField(max_length=10, default=0)
    v_out = models.IntegerField(max_length=10,default=0)
    locktime = models.IntegerField(max_length=10, null=False)
    version = models.CharField(max_length=10)
    #raw_hex = models.CharField(max_length=200)



    def __unicode__(self):
        return str(self.transaction_hash_main)


class block_and_blockHeader(models.Model):
    transaction_hash = models.ForeignKey(get_main_table, on_delete=models.CASCADE)
    previous_block_hash = models.CharField(max_length=200, null=False)
    merkle_root = models.CharField(max_length=100)
    timestamp = models.DateTimeField(null=False)
    block_header_version = models.CharField(max_length=100)
    bits = models.IntegerField(max_length=30)
    nonce = models.IntegerField(max_length=30)
    difficulty = models.IntegerField(max_length=20)


class output_table(models.Model):
    transaction_hash_out = models.ForeignKey(main_table, on_delete=models.CASCADE)
    output_no = models.IntegerField(max_length=100, null=False)
    output_type = models.CharField(max_length=20, null=False)
    output_value = models.IntegerField(max_length=200, null=False)
    size = models.IntegerField(max_length=200, null=False)
    script = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=400, null=False)

class input_table(models.Model):
    #transaction_hash_in = models.CharField(max_length=500,null=False, primary_key=True)
    transaction_hash_in = models.ForeignKey(main_table, on_delete=models.CASCADE)
    transaction_index = models.CharField(max_length=20,null=False)
    input_script = models.CharField(max_length=200, null=False)
    input_sequence_number = models.CharField(max_length=20, null=False)
    input_size = models.IntegerField(max_length=200, null=False)
    input_hex = models.CharField(max_length=500, null=False)
# Create your models here.
