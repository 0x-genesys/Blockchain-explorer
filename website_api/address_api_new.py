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


def search_address(request):
    if 'q' in request.GET:
        try:
            address = request.GET['q']

            page = 0

            if 'page' in request.GET:
                page = int(request.GET['page'])

            print(">>>>>start ")
            n_outputs = Output_Table.objects.filter(address=address)
            print(">>>>>outputs "+str(n_outputs))

            # n_inputs = Input_Table.objects.filter(input_address=address)
            # n_inputs = get_all_input_data(n_inputs)
            # print(">>>>>inputs "+str(n_inputs))

            input_transaction_hashes = []
            output_transaction_hashes = []
            tx_addresses = {}

            # for input_entry in n_inputs:
            #     tx_hash = input_entry.transaction_hash_id
            #     input_transaction_hashes.append(tx_hash)
            # print(">>>>>got n_inputs "+str(input_transaction_hashes))

            for output_entry in n_outputs:
                tx_hash = output_entry.transaction_hash_id
                output_transaction_hashes.append(tx_hash)
            # print(">>>>>got n_outputs "+str(output_transaction_hashes))

            #total balance in the account
            # balance = calculate_amount_address([], n_outputs)

            #total received in the account
            total_received = calculate_amount_received(n_outputs)

            #get unique hashes
            transaction_hashes = list(set(output_transaction_hashes))

            transaction_entries = []
            # length_tx = len(transaction_hashes)
            bucket = 10

            offset = page*bucket

            previous = "/btc/mainSearch/?q="+address+"&page="+str(page-1)
            next_ = "/btc/mainSearch/?q="+address+"&page="+str(page+1)

            if (offset+bucket) >= len(transaction_hashes):
                next_ = None

            if offset == 0:
                previous = None

            txs = []
            
            #Take out paginated txs sorted on timestamp
            tx_entries = Transaction_Table.objects.filter(transaction_hash__in=transaction_hashes).order_by('-timestamp')[offset:bucket+offset]
            for tx_entry in tx_entries:
                txs.append(tx_entry.transaction_hash)

            #BEGIN PAGINATED  QUERIES
                
            #PRE QUERY ALL DATA (WE SAVE I/O databse in iteration , this makes it very fast)
            temp_tx_inputs = Input_Table.objects.filter(transaction_hash_id__in=txs)
            temp_tx_inputs = get_all_input_data(temp_tx_inputs)
            temp_tx_outputs = Output_Table.objects.filter(transaction_hash_id__in=txs)

            for tx_entry in tx_entries:
                print(tx_entry)
                tx_inputs = []
                tx_outputs = []
                amount_transacted = 0
                transaction_hash = tx_entry.transaction_hash
                # print("tx_entry "+str(tx_entry))

                tx_final_entry = {}
                tx_final_entry['tx_entry'] = tx_entry
                tx_final_entry['addresses'] = {}

                #ADDRESS information:
                # for tx_input in n_inputs:
                #     if tx_input.transaction_hash_id == transaction_hash:
                #         if tx_input.input_address is not None:
                #             tx_inputs.append(tx_input.input_address)
                #             amount_transacted = amount_transacted - int(tx_input.input_value)

                for tx_output in n_outputs:
                    if tx_output.transaction_hash_id == transaction_hash:
                        if tx_output.address is not None:
                            tx_outputs.append(tx_output.address)
                            amount_transacted = amount_transacted + int(tx_output.output_value)

                #Other address information:
                if len(tx_inputs) == 0:
                    #address was in output of this tx, hence it is a credit tx
                    print("credit")
                    for tx_input_temp in temp_tx_inputs:
                        if tx_input_temp.transaction_hash_id == transaction_hash:
                            print(tx_input_temp.input_address)
                            if tx_input_temp.input_address is not None:
                                tx_inputs.append(tx_input_temp.input_address)
                                # if tx_input_temp.input_address != address:
                                #     #increase balance because someone else has given input
                                #     amount_transacted = amount_transacted + int(tx_input_temp.input_value)
                

                if len(tx_outputs) <= 1:
                    #equal to one because of balance amount being tranferred to same address
                    #address was in input of this tx, hence it is a debit tx
                    print("debit")
                    for tx_output_temp in temp_tx_outputs:
                        if tx_output_temp.transaction_hash_id == transaction_hash:
                            if tx_output_temp.address is not None:
                                tx_outputs.append(tx_output_temp.address)
                                # if tx_output_temp.address != address:
                                #     #decrease balance because you gave someone else money in output
                                #     amount_transacted = amount_transacted - int(tx_output_temp.output_value)


                net_value = amount_transacted / 100000000 #satoshi to btc

                tx_final_entry['value'] = net_value
                tx_final_entry['addresses']['input'] = tx_inputs
                tx_final_entry['addresses']['output'] = tx_outputs

                transaction_entries.append(tx_final_entry)

            # transaction_entries.sort(key=extract_time_tuple, reverse=True)
        except Exception as e:
            print(e)
            return render(request,'website_api/wrong_search.html')

        return render(request, 'website_api/search_address.html', {
                                                                'Address':address,
                                                                'transaction_list':transaction_entries,
                                                                # 'balance': balance,
                                                                'total_received': total_received,
                                                                'tx_count': len(transaction_hashes),
                                                                'next_page': next_,
                                                                'previous_page': previous
                                                               })