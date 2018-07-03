# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.indexes import GinIndex
#import djngo.contrib.postgres.search as pg_search

class Block_Table(models.Model):
    # block_hash = models.CharField(primary_key=True, db_index=True, max_length=200)
    block_hash = models.CharField(db_index=False, max_length=200)
    block_header = models.CharField(db_index=False, max_length=200)
    block_no_of_transactions = models.IntegerField(db_index=False,)
    block_size = models.IntegerField(db_index=False)
    block_height = models.IntegerField(db_index=False,blank=True, null=False)

#############################  Block header contents ####################
    block_header_version = models.CharField(db_index=False,max_length=10)
    previous_block_hash = models.CharField(db_index=False,max_length=200, null=False)
    merkle_root = models.CharField(db_index=False,max_length=100)
    timestamp = models.DateTimeField(db_index=False,null=False)
    bits = models.CharField(db_index=False,max_length=50)
    nonce = models.CharField(db_index=False,max_length=50)
    difficulty = models.TextField(db_index=False)

    def __str__(self):
        return str(self.block_height)
    def __unicode__(self):
        return str(self.block_height)

class Transaction_Table(models.Model):
    # transaction_hash = models.CharField(primary_key=True, db_index=True, max_length=200, null=False)
    # block_height = models.ForeignKey('Block_Table', to_field="block_height", db_index=True, null=True, blank=True, on_delete=models.CASCADE)
    block_hash_id = models.CharField(db_index=False, max_length=200)
    transaction_hash = models.CharField(db_index=False,max_length=200, null=False)
    timestamp =  models.DateTimeField(db_index=False,null=False)
    block_size = models.IntegerField(db_index=False,null=True)
    is_CoinBase = models.BooleanField(db_index=False,default=True)
    V_in = models.TextField(db_index=False,default=0)
    V_out = models.TextField(db_index=False,default=0)
    locktime = models.IntegerField( db_index=False,null=False)
    version = models.CharField(db_index=False,max_length=10)
    transaction_hash_size = models.TextField(db_index=False,default=0)

    def __str__(self):
        return str(self.transaction_hash)

    def __unicode__(self):
        return str(self.transaction_hash)

class Input_Table(models.Model):
    # transaction_hash = models.ForeignKey('Transaction_Table', db_index=True, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    transaction_hash_id = models.CharField(max_length=200, null=False)
    previous_transaction_hash = models.CharField(db_index=True, max_length=200, null=True)
    transaction_index = models.TextField(max_length=20,null=False)
    input_sequence_number = models.CharField(max_length=20, null=False)
    input_size = models.TextField(null=False)
    input_address = models.CharField(db_index=True, max_length=400, null=True)
    input_value = models.CharField(max_length=100, null=True)
    input_script_type = models.TextField(max_length=400, null=True)
    input_script_value = models.TextField(max_length=400, null=True)
    input_script_operations = models.TextField(max_length=400, null=True)

    def __str__(self):
        return self.input_address

class Output_Table(models.Model):
    # transaction_hash = models.ForeignKey('Transaction_Table', db_index=True, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    transaction_hash_id = models.CharField(db_index=False, max_length=200, null=False)
    output_no = models.TextField(db_index=False,null=False)
    output_type = models.CharField(db_index=False,max_length=20, null=False)
    output_value = models.CharField(db_index=False,max_length=100,null=False)
    size = models.TextField(db_index=False,null=False)
    address = models.CharField(db_index=False,max_length=400, null=False)
    #output_script_type = models.TextField(max_length=400, null=True)
    output_script_value = models.TextField(db_index=False,max_length=400, null=True)
    output_script_operations = models.TextField(db_index=False,max_length=400, null=True)

    def __str__(self):
        return self.address


# Create your models here.
