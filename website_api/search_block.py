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
from website_api.views_ui_front import get_all_input_data, extract_time_tuple
from PIL import Image


"""
View to search for block hash from the database along with the included transactions of the block and their
corresponding addresses. This function is called when the main search function redirects the control to this function.
"""
def search_block_hash(request):
    try:
        limit = 15
        if 'q' in request.GET:
            print(str("begin"))
            block_hash = request.GET['q']

            #PAGINATION

            page = 0

            if 'page' in request.GET:
                page = int(request.GET['page'])

            print(str(page))

            offset = limit * page

            len_tx_for_block = Transaction_Table.objects.filter(block_hash_id = block_hash).count()
            print(len_tx_for_block)

            previous = "/btc/search/?q=" + block_hash + "&page="+str(page-1)
            next_ = "/btc/search/?q=" + block_hash + "&page="+str(page+1)

            if (offset+limit) >= len_tx_for_block:
                next_ = None

            if offset == 0:
                previous = None

            print(offset)
            print(limit)

            #LOGIC

            search_term = Block_Table.objects.filter(block_hash=block_hash) #for merkel, prvious block etc.
            transaction_list = []

            input_address_list_final = []
            flag = []
            final_list = []

            if not search_term:
                return render(request,'website_api/wrong_search.html')

            transaction_db = Transaction_Table.objects.filter(block_hash_id = search_term[0].block_hash)[offset:limit+offset]

            print(transaction_db)

            txs = []

            for transaction in transaction_db:
                txs.append(transaction.transaction_hash)

            #QUERY + LOOP
            print(txs)
            # outputs_db = get_values_all_query('bitcoin_data_app_output_table', txs, 'transaction_hash_id', None, None, None)
            # inputs_db = get_values_all_query('bitcoin_data_app_input_table', txs, 'transaction_hash_id', None, None, None)
            # inputs_db = get_all_input_data_for_tuple(inputs_db)

            outputs_db = Output_Table.objects.filter(transaction_hash_id__in=txs)
            inputs_db = Input_Table.objects.filter(transaction_hash_id__in=txs)
            inputs_db = get_all_input_data(inputs_db)

            for transaction in transaction_db:
                transaction_hash = transaction.transaction_hash
                transaction_list.append(transaction_hash)

                output_address_list = []
                input_address_list = []
                output_db_balance = []

                #query inputs from outputs
                if inputs_db and len(inputs_db) > 0:
                    for input_ in inputs_db:
                        if input_.input_address and input_.transaction_hash_id == transaction_hash:
                            input_address_list.append(input_.input_address)

                if outputs_db and len(outputs_db) > 0:
                    for output in outputs_db:
                        if output.transaction_hash_id == transaction_hash:
                            output_address_list.append(output.address)
                            output_db_balance.append(output)

                balance = calculate_amount_received(output_db_balance)  
                print(balance)

                record_output_address = {
                                          'transaction_hash':transaction_hash,
                                          'output_address':output_address_list,
                                          'input_address':input_address_list,
                                          'balance': balance
                                        }

                final_list.append(record_output_address)
                
            #VIEW
            return render(request,'website_api/search_block_hash.html', {
                                                                        'block_hash':search_term[0].block_hash,
                                                                        'previous_block_hash':search_term[0].previous_block_hash,
                                                                        'merkle_root':search_term[0].merkle_root,
                                                                        'block_no_of_transactions':search_term[0].block_no_of_transactions,
                                                                        'block_size':search_term[0].block_size,
                                                                        'block_height':search_term[0].block_height,
                                                                        'timestamp':search_term[0].timestamp,
                                                                        'difficulty':search_term[0].difficulty,
                                                                        'bits':search_term[0].bits,
                                                                        'nonce':search_term[0].nonce,
                                                                        'final_list':final_list,
                                                                        'next_page': next_,
                                                                        'previous_page': previous
                                                                        })
    except Exception as e:
        print(e)
        return render(request,'website_api/wrong_search.html')