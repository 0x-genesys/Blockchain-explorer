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
View to extract the transaction hash from the database and the corresponding addresses involved in it.
It is called when the main search function redirects the control over here.
"""
#1NadpqHPHHFVDP15fB7e46mk5GJjs2NP8D
def search_transaction_hash(request):
    if 'q' in request.GET:
        tx_search = request.GET['q']
        #message = request
        output_address_list = []
        output_address_price = []
        input_address_list = []
        output_scripts = []
        input_scripts = []
        search_term = Transaction_Table.objects.filter(transaction_hash=tx_search).order_by('-timestamp')
        if len(search_term) == 0:
            return render(request,'website_api/wrong_search.html')
        block = Block_Table.objects.filter(block_hash=search_term[0].block_hash_id)
        #print(message)
        if not search_term:
            return render(request,'website_api/wrong_search.html')
        else:
            output_db = Output_Table.objects.filter(transaction_hash_id=search_term[0].transaction_hash)
            input_db = Input_Table.objects.filter(transaction_hash_id=search_term[0].transaction_hash)

            for output in output_db:
                if output.address:
                    output_address_list.append(output.address)
                if output.output_script_value:
                    output_scripts.append(output.output_script_value)

            input_db =  get_all_input_data(input_db)

            for input_ in input_db:
                if input_.input_address:
                    input_address_list.append(input_.input_address)
                if input_.input_script_value:
                    input_scripts.append(input_.input_script_value)
                if input_.input_value:
                    print(str(int(input_.input_value)/100000000))
                    output_address_price.append(str(int(input_.input_value)/100000000))

            balance = calculate_amount_received(output_db)

            return render(request,'website_api/search_transaction_hash.html', {
                                                                                'transaction_hash':search_term[0].transaction_hash,
                                                                                'block_size':search_term[0].block_size,
                                                                                'Number_of_inputs':search_term[0].V_in,
                                                                                'Number_of_outputs':search_term[0].V_out,
                                                                                'locktime':search_term[0].locktime,
                                                                                'version':search_term[0].version,
                                                                                'block_height':block[0].block_height,
                                                                                'coinbase':search_term[0].is_CoinBase,
                                                                                'output_addresses':output_address_list,
                                                                                'output_address_price': output_address_price,
                                                                                'input_addresses':input_address_list,
                                                                                'transaction_hash_size':search_term[0].transaction_hash_size,
                                                                                'output_script':output_scripts,
                                                                                'input_scripts':input_scripts,
                                                                                'timestamp': search_term[0].timestamp,
                                                                                'balance': balance,
                                                                            })
