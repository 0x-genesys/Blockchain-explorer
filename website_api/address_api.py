from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from bitcoin_data_app.models import Block_Table, Transaction_Table, Output_Table, Input_Table
from django.shortcuts import render_to_response
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from app.settings import BLOCK_DATA_DIR, BASE_DIR, STATICFILES_DIRS
import os
import qrcode
import time
import calendar
import re
from django.db import connection
import io
import math
from .calaculate_amount import calculate_amount_tx, calculate_amount_address, calculate_amount_received, calculate_amount_received_tuple
import urllib, base64
from io import BytesIO
from PIL import Image
from website_api.views_ui_front import get_all_input_data_for_tuple, extract_time_tuple, search_address


"""
View to search for addresses whether it is an input address or an output address.
It is called when redirected from main search function.
Creates Qr code for each address.
"""
def search_address_new(request):
    if 'q' in request.GET:
        try:
            address = request.GET['q']
            n_count = get_output_count(address) #todo how to add input here
            print(">>>>>n_count "+str(n_count))

            if n_count < 20:
                #for light pages
                print(">>>>OLD FLOW")
                return search_address(request)

            print(">>>>NEW FLOW")
            page = 0
            if 'page' in request.GET:
                page = int(request.GET['page'])

            previous = "/btc/mainSearch/?q="+address+"&page="+str(page-1)
            next_ = "/btc/mainSearch/?q="+address+"&page="+str(page+1)
            bucket = 5
            offset = bucket*page

            print(">>>>>start ")
            n_outputs = get_outputs_list(address, offset, bucket)
            print(">>>>>outputs "+str(n_outputs))

            n_inputs = get_inputs_list(address, offset, bucket)
            print(">>>>>inputs "+str(n_inputs))

            if (offset+bucket) >= n_count:
                next_ = None

            if offset == 0:
                previous = None

            input_transaction_hashes = []
            output_transaction_hashes = []
            tx_addresses = {}

            #total balance in the account
            # balance = calculate_amount_address(n_inputs, n_outputs)
            balance = '???'

            #total received in the account
            # total_received = calculate_amount_received(n_outputs)
            total_received = '???'

            #just output because inputs will have same set of tx as outputs
            transactions = {tx['transaction_hash'] for tx in n_outputs}

            print("transactions "+str(transactions))

            transaction_entries = []

            for tx in transactions:
                print(tx)
                tx_final_entry = {}
                tx_final_entry['tx_entry'] = {}
                tx_final_entry['tx_entry']['transaction_hash'] = tx
                tx_final_entry['addresses'] = {}
                tx_final_entry['addresses']['input'] = []
                tx_final_entry['addresses']['output'] = []

                _outputs = []
                _inputs = []

                #build inputs with previous output reference
                for _input in n_inputs:
                    if _input['transaction_hash'] == tx:
                        _inputs.append(_input)

                #query input data from previous output reference
                _inputs = get_all_input_data_for_tuple(_inputs)



                #find out relevant inputs from all the data
                for _input in _inputs:
                    if 'input_address' in _input:
                        tx_final_entry['addresses']['input'].append(_input['input_address'])

                #find out relevant outputs from all the data
                for _output in n_outputs:
                    if _output['transaction_hash'] == tx:
                        tx_final_entry['addresses']['output'].append(_output['address'])
                        _outputs.append(_output)
                        tx_final_entry['tx_entry']['timestamp'] = _output['timestamp']

                net_value = calculate_amount_received_tuple(_outputs)
                tx_final_entry['value'] = net_value
                transaction_entries.append(tx_final_entry)

            transaction_entries.sort(key=extract_time_tuple, reverse=False)
        except Exception as e:
            print(e)
            return render(request,'website_api/wrong_search.html')

        return render(request, 'website_api/search_address.html', {
                                                                'Address':address,
                                                                'transaction_list':transaction_entries,
                                                                'balance': balance,
                                                                'total_received': total_received,
                                                                'tx_count': n_count,
                                                                'next_page': next_,
                                                                'previous_page': previous
                                                               })


def get_outputs_list(address, offset, limit):
    query = "select t3.output_value, t3.address, tx.transaction_hash, tx.timestamp "
    query = query + "  from ("
    query = query + "  select t2.address, t1.transaction_hash, t1.timestamp"
    query = query + "  from bitcoin_data_app_transaction_table t1 "
    query = query + "  inner join bitcoin_data_app_output_table t2"
    query = query + "  on t2.transaction_hash_id = t1.transaction_hash "
    query = query + "  where t2.address = '" + str(address) + "' "
    query = query + "  offset " + str(offset) + " limit " + str(limit)
    query = query + " ) tx inner JOIN bitcoin_data_app_output_table t3 on t3.transaction_hash_id=tx.transaction_hash;"
    return execute_query(query)


def get_inputs_list(address, offset, limit):
    query = "select t3.previous_transaction_hash, t3.transaction_index, tx.transaction_hash"
    query = query + "  from ("
    query = query + "  select t2.address, t1.transaction_hash, t1.timestamp"
    query = query + "  from bitcoin_data_app_transaction_table t1 "
    query = query + "  inner join bitcoin_data_app_output_table t2"
    query = query + "  on t2.transaction_hash_id = t1.transaction_hash "
    query = query + "  where t2.address = '" + str(address) + "' "
    query = query + "  offset " + str(offset) + " limit " + str(limit)
    query = query + " ) tx inner JOIN bitcoin_data_app_input_table t3 on t3.transaction_hash_id=tx.transaction_hash;"
    return execute_query(query)

def get_output_count(address):
    return Output_Table.objects.filter(address=address).count()

def execute_query(query):
    cursor = connection.cursor()
    cursor.execute(query)

    field_names = [item[0] for item in cursor.description]
    rawData = cursor.fetchall()

    #convert list tuple data to dictionary meaningful data
    result = []
    for row in rawData:
        objDict = {}
        for index, value in enumerate(row):
            objDict[field_names[index]] = value
        result.append(objDict)
    cursor.close()

    return result
