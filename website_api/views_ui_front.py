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



"""
View to set the header and the footer through all the pages in the site
"""
def base_view(request):
    return render(request,'website_api/base.html')



"""
View to showcase the wallet developed for crypto currencies.
"""
def wallet(request):
    return render(request,'website_api/wallet.html')




"""
View to call the introduction page of the Blockwala BTC Explorer
Showing latest 5 blocks and enables the user to search for any kind of hash, Address,
Height etc
"""
def index(request):
    display_object = Block_Table.objects.all().order_by('-timestamp')[:5]

    if not display_object:
        print("nothing")
    else:
        return render(request,'website_api/index.html',{'output':display_object,
                                                                'range':range(5)})




# def recent_data(request):
#     display_object = Block_Table.objects.all().order_by('-block_height')[:5]
#
#     return render(request,'website_api/recent_data.html',{'output':display_object,
#                                                                 'range':range(5)})



"""
View to call all the block entries along with their details and show them in
a set of 100/page. Query is made more repsponsive by indexing.
"""
def recent_hundred_data(request):
    display_object = Block_Table.objects.all().order_by('-timestamp')
    paginator = Paginator(display_object, 100)

    page = request.GET.get('page')
    dobs = paginator.get_page(page)
    return render(request,'website_api/recent_hundred_data.html',{'output':dobs, 'range':range(5)})





"""
This View is important in a way that it decides what is searched and with the help of
Regex in Python/Django. It gives the user to search from a single search bar like transaction hash, block hash, etc.
"""

def main_search_bar(request):
    print(request)
    if 'q' in request.GET:
        message = request.GET['q']
        if 'page' in request.GET:
            page = request.GET['page']
        else:
            page = 0
        pattern_block_hash = re.compile("^[0]{8}[a-zA-Z0-9]{56}$")
        pattern_transaction_hash = re.compile("^[a-zA-Z0-9]{64}$")
        pattern_address = re.compile("^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$")
        pattern_height = re.compile("^[+]?\d+$")
        if pattern_block_hash.match(message):
            print("block")
            return redirect('/btc/search/?q='+message+ "&page="+str(page))
        elif pattern_transaction_hash.match(message):
            print("transaction")
            return redirect('/btc/searchTransaction/?q='+message)
        elif pattern_address.match(message):
            print(message)
            print("TRUE")
            # return redirect(search_address, message)
            return redirect('/btc/searchAddress/?q=' + message +"&page="+str(page))

        elif pattern_height.match(message):
            return redirect('/btc/searchBlockHeight/?q=' + message + "&page="+str(page))
        else:
            return render(request,'website_api/wrong_search.html')





def extract_time_tuple(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        mysql_time_struct = time.strptime(str(json['tx_entry']['timestamp']), "%Y-%m-%d %H:%M:%S")
        mysql_time_epoch = calendar.timegm(mysql_time_struct)
        return int(mysql_time_epoch)
    except KeyError:
        return 0


"""
View to search for block Height and it redirects the height function to search block hash function
by giving the corresponding hash.
"""

def search_block_height(request):
    if 'q' in request.GET:
        message = request.GET['q']
        print("anything")
        print(message)
        block_search_term = Block_Table.objects.filter(block_height=message)
        if not block_search_term:
            return render(request,'website_api/wrong_search.html')
        else:
            return redirect('/btc/search/?q='+block_search_term[0].block_hash)


def get_all_input_data(inputs_db):
    tx_hashes = []
    for input_ in inputs_db:
        tx_hashes.append(input_.previous_transaction_hash)
    # print(">>>>>>> "+str(tx_hashes))
    if len(tx_hashes) > 0:
        length_tx = len(tx_hashes)
        bucket = 20
        limit_tx = math.ceil(length_tx/bucket)
        # print("length_tx "+str(length_tx))
        # print("limit_tx "+str(limit_tx))
        for i in range(limit_tx):
            start = i*bucket
            end = (i+1)*bucket
            # print("i  "+str(i))
            # print("start "+str(start))

            if end > (length_tx):
                 end = length_tx

            # print("end  "+str(end))
            sliceObj = slice(start, end)
            txs = tx_hashes[sliceObj]

            # outputs = Output_Table.objects.only('address', 'output_value','output_type', 'output_no', 'transaction_hash_id').filter(transaction_hash_id__in=txs)

            outputs = get_values_all_query('bitcoin_data_app_output_table', txs, 'transaction_hash_id', None, None, None)

            for output in outputs:
                for _input in inputs_db:
                    # print(_input.previous_transaction_hash + "  " + output.transaction_hash_id )
                    # print(_input.transaction_index + "  " + output.output_no)
                    if _input.previous_transaction_hash == output['transaction_hash_id'] and output['output_no'] == _input.transaction_index:
                        _input.input_address = output['address']
                        _input.input_value = output['output_value']
                        _input.input_script_type = output['output_type']

    return inputs_db

def get_all_input_data_for_tuple(inputs):
    tx_hashes = []
    for input_ in inputs:
        tx_hashes.append(input_['previous_transaction_hash'])
    # print(">>>>>>> "+str(tx_hashes))
    if len(tx_hashes) > 0:
        length_tx = len(tx_hashes)
        bucket = 20
        limit_tx = math.ceil(length_tx/bucket)
        # print("length_tx "+str(length_tx))
        # print("limit_tx "+str(limit_tx))
        for i in range(limit_tx):
            start = i*bucket
            end = (i+1)*bucket
            # print("i  "+str(i))
            # print("start "+str(start))

            if end > (length_tx):
                 end = length_tx

            # print("end  "+str(end))
            sliceObj = slice(start, end)
            txs = tx_hashes[sliceObj]

            # outputs = Output_Table.objects.only('address', 'output_value','output_type', 'output_no', 'transaction_hash_id').filter(transaction_hash_id__in=txs)
            outputs = get_values_all_query('bitcoin_data_app_output_table', txs, 'transaction_hash_id', None, None, None)

            for output in outputs:
                for _input in inputs:
                    # print(_input.previous_transaction_hash + "  " + output.transaction_hash_id )
                    # print(_input.transaction_index + "  " + output.output_no)
                    if _input['previous_transaction_hash'] == output['transaction_hash_id'] and output['output_no'] == _input['transaction_index']:
                        _input['input_address'] = output['address']
                        _input['input_value'] = output['output_value']
                        _input['input_script_type'] = output['output_type']

    return inputs


def get_values_all_query(table, data_list, column_to_search, order_by, limit, offset):
    # tx_entries = Transaction_Table.objects.filter(transaction_hash__in=txs)
    query_tx = 'select * from '+ table + ' INNER JOIN  ( VALUES '
    # tx_entries = Transaction_Table.objects.all()
    for i, data_entry in enumerate(data_list):
        query_tx = query_tx + "('"+str(data_entry)+"')"
        if i < len(data_list) - 1:
            query_tx = query_tx + ","
    query_tx = query_tx + ") vals(v) ON ( " + column_to_search + " = v)"

    if order_by is not None:
        query_tx = query_tx + " order by " + order_by

    if offset is not None:
        query_tx = query_tx +" offset " + offset

    if limit is not None:
        query_tx = query_tx +" limit " + limit

    # print(query_tx)

    cursor = connection.cursor()
    cursor.execute(query_tx)

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


"""
This View is invoked whenever someone searches for a wrong hash or if the data is not present in the database
"""

def wrong_query(request):
    return render(request,'website_api/wrong_search.html')
