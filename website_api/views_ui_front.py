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
import io
from .calaculate_amount import calculate_amount_tx, calculate_amount_address, calculate_amount_received
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
    paginator = Paginator(display_object,100)

    page = request.GET.get('page')
    dobs = paginator.get_page(page)
    return render(request,'website_api/recent_hundred_data.html',{'output':dobs,
                                                            'range':range(5)})





"""
This View is important in a way that it decides what is searched and with the help of
Regex in Python/Django. It gives the user to search from a single search bar like transaction hash, block hash, etc.
"""

def main_search_bar(request):
    if 'q' in request.GET:
        message = request.GET['q']
        pattern_block_hash = re.compile("^[0]{8}[a-zA-Z0-9]{56}$")
        pattern_transaction_hash = re.compile("^[a-zA-Z0-9]{64}$")
        pattern_address = re.compile("^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$")
        pattern_height = re.compile("^[+]?\d+$")
        if pattern_block_hash.match(message):
            print("block")
            return redirect('/ui/search/?q='+message)
        elif pattern_transaction_hash.match(message):
            print("transaction")
            return redirect('/ui/searchTransaction/?q='+message)
        elif pattern_address.match(message):
            print(message)
            print("TRUE")
            #return redirect(search_address,message)
            return redirect('/ui/searchAddress/?q='+message)

        elif pattern_height.match(message):
            return redirect('/ui/searchBlockHeight/?q='+message)
        else:
            return render(request,'website_api/wrong_search.html')







"""
View to search for block hash from the database along with the included transactions of the block and their
corresponding addresses. This function is called when the main search function redirects the control to this function.
"""
def search_block_hash(request):
    if 'q' in request.GET:
        message = request.GET['q']
        #message = request
        search_term = Block_Table.objects.filter(block_hash=message)
        transaction_list = []

        input_address_list_final = []
        flag = []
        final_list = []

        if not search_term:
            return render(request,'website_api/wrong_search.html')

        transaction_db = Transaction_Table.objects.filter(block_hash_id = search_term[0].block_hash)
        print(len(transaction_db))
        for transaction in transaction_db:
            transaction_list.append(transaction.transaction_hash)
            outputs_db = Output_Table.objects.filter(transaction_hash_id=transaction.transaction_hash)
            inputs_db = Input_Table.objects.filter(transaction_hash_id=transaction.transaction_hash)

            output_address_list = []
            input_address_list = []

            if inputs_db and len(inputs_db) > 0:
                for input_ in inputs_db:
                    if input_.input_address:
                        input_address_list.append(input_.input_address)

            if outputs_db and len(outputs_db) > 0:
                for output in outputs_db:
                        output_address_list.append(output.address)
                
            balance = calculate_amount_received(outputs_db)    

            record_output_address = {
                                      'transaction_hash':transaction.transaction_hash,
                                      'output_address':output_address_list,
                                      'input_address':input_address_list,
                                      'balance': balance
                                      }

            final_list.append(record_output_address)
            

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
                                                                    'final_list':final_list
                                                                    })






"""
View to extract the transaction hash from the database and the corresponding addresses involved in it.
It is called when the main search function redirects the control over here.
"""

def search_transaction_hash(request):
    if 'q' in request.GET:
        message = request.GET['q']
        #message = request
        output_address_list = []
        output_address_price = []
        input_address_list = []
        output_scripts = []
        input_scripts = []
        search_term = Transaction_Table.objects.filter(transaction_hash=message).order_by('-timestamp')
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
        message = request.GET['q']

        n_outputs = Output_Table.objects.filter(address=message)
        n_inputs = Input_Table.objects.filter(input_address=message)

        input_transaction_hashes = []
        output_transaction_hashes = []
        tx_addresses = {}

        for input_entry in n_inputs:
            tx_hash = input_entry.transaction_hash_id
            print(input_entry.input_value)
            input_transaction_hashes.append(tx_hash)

        for output_entry in n_outputs:
            tx_hash = output_entry.transaction_hash_id
            output_transaction_hashes.append(tx_hash)

        balance = calculate_amount_address(n_inputs, n_outputs)
        total_received = calculate_amount_received(n_outputs)



        #get unique hashes
        transaction_hashes = list(set(input_transaction_hashes + output_transaction_hashes))

        transaction_entries = []

        for transaction_hash in transaction_hashes:
            tx_entries = Transaction_Table.objects.filter(transaction_hash=transaction_hash)
            tx_inputs_db = Input_Table.objects.filter(transaction_hash_id=transaction_hash)
            tx_outputs_db = Output_Table.objects.filter(transaction_hash_id=transaction_hash)
            tx_inputs = []
            tx_outputs = []

            #construct the inputs
            for _input in tx_inputs_db:
                if _input.input_address is not None:
                    tx_inputs.append(_input.input_address)

            for _output in tx_outputs_db:
                tx_outputs.append(_output.address)

            net_value = calculate_amount_received(tx_outputs_db)

            tx_entry = tx_entries[0]
            tx_final_entry = {}
            tx_final_entry['tx_entry'] = tx_entry
            tx_final_entry['addresses'] = {}
            tx_final_entry['value'] = net_value
            tx_final_entry['addresses'] = {}
            tx_final_entry['addresses']['input'] = tx_inputs
            tx_final_entry['addresses']['output'] = tx_outputs

            transaction_entries.append(tx_final_entry)

        transaction_entries.sort(key=extract_time, reverse=True)
        return render(request, 'website_api/search_address.html', {
                                                                'Address':message,
                                                                'transaction_list':transaction_entries,
                                                                'balance': balance,
                                                                'total_received': total_received,
                                                                'tx_count': len(transaction_hashes)
                                                               })

def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        mysql_time_struct = time.strptime(str(json['tx_entry'].timestamp), "%Y-%m-%d %H:%M:%S")
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
            return redirect('/ui/search/?q='+block_search_term[0].block_hash)





"""
This View is invoked whenever someone searches for a wrong hash or if the data is not present in the database
"""

def wrong_query(request):
    return render(request,'website_api/wrong_search.html')
