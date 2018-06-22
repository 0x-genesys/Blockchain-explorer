# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from bitcoin_data_app.models import Block_Table, Transaction_Table, Input_Table, Output_Table
from django.core import serializers



def get_transaction_details(request):
    if request.method == 'GET':
        query = request.GET.get('transaction_hash','')
        #print(query)
        transaction_object = Transaction_Table.objects.filter(transaction_hash=query)
        input_object = Input_Table.objects.filter(transaction_hash=query)
        output_object = Output_Table.objects.filter(transaction_hash=query)


        if not transaction_object:
            print("nothing returned")
        else:
            transaction_object_serialized = serializers.serialize('json',[transaction_object[0],])

            return JsonResponse({"transaction_hash": query,
                                "block_height":transaction_object[0].block_height_id,
                                  "block_size":transaction_object[0].block_size,
                                  "is_CoinBase":transaction_object[0].is_CoinBase,
                                  "number of inputs":transaction_object[0].V_in,
                                  "number of outputs":transaction_object[0].V_out,
                                  "locktime":transaction_object[0].locktime,
                                  "version":transaction_object[0].version,
                                  "transaction_index":input_object[0].transaction_index,
                                  "input_script":input_object[0].input_script,
                                  "input_sequence_number":input_object[0].input_sequence_number,
                                  "input_size":input_object[0].input_size,
                                  "output_no":output_object[0].output_no,
                                  "output_type":output_object[0].output_type,
                                  "output_value":output_object[0].output_value,
                                  "size":output_object[0].size,
                                  "output_script":output_object[0].script,
                                  "address":output_object[0].address, }, status=200)



def get_block_details(request):
    if request.method == 'GET':
        query = request.GET.get('block_hash', '')

        block_object = Block_Table.objects.filter(block_hash=query)

        if not block_object:
            print("Data does not exist or wrong input")
        else:
            return JsonResponse({'block_hash': block_object[0].block_hash,
                                 'block_header':block_object[0].block_header,
                                 'block_no_of_transactions':block_object[0].block_no_of_transactions,
                                 'block_size':block_object[0].block_size,
                                 'block_height':block_object[0].block_height,
                                 'block_header_version':block_object[0].block_header_version,
                                 'previous_block_hash':block_object[0].previous_block_hash,
                                 'merkle_root':block_object[0].merkle_root,
                                 'timestamp':block_object[0].timestamp,
                                 'bits':block_object[0].bits,
                                 'nonce':block_object[0].nonce,
                                 'difficulty':block_object[0].difficulty       }, status=200)
