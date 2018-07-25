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
            #return redirect(search_address,message)
            return redirect('/btc/searchAddress/?q=' + message +"&page="+str(page))

        elif pattern_height.match(message):
            return redirect('/btc/searchBlockHeight/?q=' + message + "&page="+str(page))
        else:
            return render(request,'website_api/wrong_search.html')







"""
View to search for block hash from the database along with the included transactions of the block and their
corresponding addresses. This function is called when the main search function redirects the control to this function.
"""
def search_block_hash(request):
    try:
        if 'q' in request.GET:
            print(str("begin"))
            block_hash = request.GET['q']

            #PAGINATION

            page = 0

            if 'page' in request.GET:
                page = int(request.GET['page'])

            print(str(page))

            limit = 5
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

            for transaction in transaction_db:
                transaction_hash = transaction.transaction_hash
                # transaction_list.append(transaction_hash)
                # outputs_db = Output_Table.objects.filter(transaction_hash_id=transaction.transaction_hash)
                # inputs_db = Input_Table.objects.filter(transaction_hash_id=transaction.transaction_hash)

                output_address_list = []
                input_address_list = []
                output_db_balance = []

                #query inputs from outputs

                # if inputs_db and len(inputs_db) > 0:
                #     for input_ in inputs_db:
                #         if input_['input_address'] and input_['transaction_hash_id'] == transaction_hash:
                #             input_address_list.append(input_['input_address'])

                # if outputs_db and len(outputs_db) > 0:
                #     for output in outputs_db:
                #         if output['transaction_hash_id'] == transaction_hash:
                #             output_address_list.append(output['address'])
                #             output_db_balance.append(output)
                    
                # balance = calculate_amount_received_tuple(output_db_balance)  
                # print(balance)

                record_output_address = {
                                          'transaction_hash':transaction_hash,
                                          # 'output_address':output_address_list,
                                          # 'input_address':input_address_list,
                                          # 'balance': balance
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






"""
View to search for addresses whether it is an input address or an output address.
It is called when redirected from main search function.
Creates Qr code for each address.
"""
def search_address(request):
    if 'q' in request.GET:
        try:
            address = request.GET['q']

            page = 0

            if 'page' in request.GET:
                page = int(request.GET['page'])

            # print(">>>>>start ")
            n_outputs = Output_Table.objects.filter(address=address).order_by('id')
            # print(">>>>>outputs "+str(n_outputs))

            n_inputs = Input_Table.objects.filter(input_address=address).order_by('id')
            n_inputs = get_all_input_data(n_inputs)
            # print(">>>>>inputs "+str(n_inputs))

            input_transaction_hashes = []
            output_transaction_hashes = []
            tx_addresses = {}

            for input_entry in n_inputs:
                tx_hash = input_entry.transaction_hash_id
                input_transaction_hashes.append(tx_hash)
            # print(">>>>>got n_inputs "+str(input_transaction_hashes))

            for output_entry in n_outputs:
                tx_hash = output_entry.transaction_hash_id
                output_transaction_hashes.append(tx_hash)
            # print(">>>>>got n_outputs "+str(output_transaction_hashes))

            #total balance in the account
            balance = calculate_amount_address(n_inputs, n_outputs)

            #total received in the account
            total_received = calculate_amount_received(n_outputs)

            #get unique hashes
            transaction_hashes = list(set(input_transaction_hashes + output_transaction_hashes))

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
            
            tx_entries = get_values_all_query('bitcoin_data_app_transaction_table', transaction_hashes, 'transaction_hash', 'timestamp DESC', str(bucket), str(offset))
            # print("tx_entries "+str(tx_entries))

            txs = []
            for tx_entry in tx_entries:
                txs.append(tx_entry['transaction_hash'])

            tx_inputs_db = get_values_all_query('bitcoin_data_app_input_table', txs, 'transaction_hash_id', None, None, None)
            # print("tx_inputs_db "+ str(tx_inputs_db))
            # tx_inputs_db = Input_Table.objects.filter(transaction_hash_id__in=txs)
            tx_inputs_db = get_all_input_data_for_tuple(tx_inputs_db)
            tx_outputs_db = get_values_all_query('bitcoin_data_app_output_table', txs, 'transaction_hash_id', None, None, None)
            # tx_outputs_db = Output_Table.objects.filter(transaction_hash_id__in=txs)
            
            # print("tx_inputs_db  "+str(tx_inputs_db))
            # print("tx_outputs_db  "+str(tx_outputs_db))

            for tx_entry in tx_entries:
                tx_inputs = []
                tx_outputs = []
                # print("tx_entry "+str(tx_entry))

                tx_final_entry = {}
                tx_final_entry['tx_entry'] = tx_entry
                tx_final_entry['addresses'] = {}

                for tx_input in tx_inputs_db:
                    if tx_input['transaction_hash_id'] == tx_entry['transaction_hash']:
                        if tx_input['input_address'] is not None:
                            tx_inputs.append(tx_input['input_address'])

                for tx_output in tx_outputs_db:
                    if tx_output['transaction_hash_id'] == tx_entry['transaction_hash']:
                        tx_outputs.append(tx_output['address'])

                net_value = calculate_amount_received_tuple(tx_outputs_db)

                tx_final_entry['value'] = net_value
                tx_final_entry['addresses']['input'] = tx_inputs
                tx_final_entry['addresses']['output'] = tx_outputs

                transaction_entries.append(tx_final_entry)

            transaction_entries.sort(key=extract_time_tuple, reverse=True)
        except Exception as e:
            print(e)
            return render(request,'website_api/wrong_search.html')

        return render(request, 'website_api/search_address.html', {
                                                                'Address':address,
                                                                'transaction_list':transaction_entries,
                                                                'balance': balance,
                                                                'total_received': total_received,
                                                                'tx_count': len(transaction_hashes),
                                                                'next_page': next_,
                                                                'previous_page': previous
                                                               })

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
        bucket = 100
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
        bucket = 100
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
