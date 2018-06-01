# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Block_Table(models.Model):
    block_hash = models.CharField(max_length=200)
    block_header = models.CharField(max_length=200)
    block_no_of_transactions = models.IntegerField()
    block_size = models.IntegerField()
    block_height = models.IntegerField( blank=True, null=True)

#############################  Block header contents ####################
    block_header_version = models.CharField(max_length=10)
    previous_block_hash = models.CharField(primary_key=True,max_length=200, null=False)
    merkle_root = models.CharField(max_length=100)
    timestamp = models.DateTimeField(null=False)
    bits = models.CharField(max_length=50)
    nonce = models.CharField(max_length=50)
    difficulty = models.IntegerField()


    def __str__(self):
        return str(self.block_height)
    def __unicode__(self):
        return str(block_height)
    #def __str__(self):
    #    return str(self.previous_block_hash)
    #def __unicode__(self):
    #    return str(self.block_height)

class Transaction_Table(models.Model):
    transaction_hash = models.CharField(primary_key=True,max_length=200, null=False)
    block_height = models.ForeignKey('Block_Table', null=True, blank=True, on_delete=models.CASCADE)
    block_size = models.IntegerField(null=True)
    is_CoinBase = models.BooleanField(default=True)
    V_in = models.IntegerField(default=0)
    V_out = models.IntegerField(default=0)
    locktime = models.IntegerField( null=False)
    version = models.CharField(max_length=10)
    #raw_hex = models.SlugField(max_length=255)


    def __str__(self):
        return str(self.transaction_hash)

    def __unicode__(self):
        return str(self.transaction_hash)
#models.ForeignKey('Comment', blank=True, null=True)

class Input_Table(models.Model):
    #transaction_hash_in = models.CharField(max_length=500,null=False, primary_key=True)
    transaction_hash = models.ForeignKey('Transaction_Table', blank=True, null=True, on_delete=models.CASCADE)
    transaction_index = models.CharField(max_length=20,null=False)
    input_script = models.TextField(max_length=400, null=False)
    input_sequence_number = models.CharField(max_length=20, null=False)
    input_size = models.IntegerField(null=False)
    #input_hex = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.input_script

class Output_Table(models.Model):
    transaction_hash = models.ForeignKey('Transaction_Table', on_delete=models.CASCADE)
    output_no = models.IntegerField(null=False)
    output_type = models.CharField(max_length=20, null=False)
    output_value = models.CharField(max_length=100,null=False)
    size = models.IntegerField(null=False)
    script = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=400, null=False)

    def __str__(self):
        return self.address


# Create your models here.
