from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from bitcoin_data_app.models import Block_Table, Transaction_Table, Output_Table, Input_Table
from django.shortcuts import render_to_response
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import os
import qrcode
import re




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
    display_object = Block_Table.objects.all().order_by('-block_height')[:5]

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

    display_object = Block_Table.objects.all().order_by('-block_height')
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
        c = 0
        if not search_term:
            return render(request,'website_api/wrong_search.html')
            print("block not present")
        else:
            print("whooo")
        transaction_search_term = Transaction_Table.objects.filter(block_height = search_term[0].block_height)
        for i in transaction_search_term:
            transaction_list.append(i.transaction_hash)
            output_address_search_term = Output_Table.objects.filter(transaction_hash_id=i.transaction_hash)
            input_address_search_term = Input_Table.objects.filter(transaction_hash_id=i.transaction_hash)
            flag.append(c)
            c += 1
            output_address_list = []
            input_address_list = []
            if not input_address_search_term:
                print("NOT")
            if output_address_search_term:

                for add in output_address_search_term:
                    output_address_list.append(add.address)
            if input_address_search_term:
                for add in input_address_search_term:
                    input_address_list.append(add.input_address)
            print(output_address_list)
            record_output_address = {'transaction_hash':i.transaction_hash,
                                      'output_address':output_address_list,
                                      'input_address':input_address_list,
                                      'flag':c}
            final_list.append(record_output_address)



        return render(request,'website_api/search_block_hash.html',{'block_hash':search_term[0].block_hash,
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
                                                                    'c':c,})








"""
View to extract the transaction hash from the database and the corresponding addresses involved in it.
It is called when the main search function redirects the control over here.
"""

def search_transaction_hash(request):
    if 'q' in request.GET:
        message = request.GET['q']
        #message = request
        output_address_list = []
        input_address_list = []
        search_term = Transaction_Table.objects.filter(transaction_hash=message)
        print(message)
        if not search_term:
            return render(request,'website_api/wrong_search.html')
            print("hash not present")
        else:
            print("present")
        output_search_term = Output_Table.objects.filter(transaction_hash_id=message)
        input_search_term = Input_Table.objects.filter(transaction_hash_id=message)
        for add in output_search_term:
            output_address_list.append(add)
        #input_address_list = ['qwertyuiop','asdfghjkl','zxcvbnm','7415852963']
        #output_address_list.append('lazwsxedcrfv')
        print("here it is = ")
        print(search_term[0].transaction_hash_size)
        return render(request,'website_api/search_transaction_hash.html',{'transaction_hash':search_term[0].transaction_hash,
                                                                            'block_size':search_term[0].block_size,
                                                                            'Number_of_inputs':search_term[0].V_in,
                                                                            'Number_of_outputs':search_term[0].V_out,
                                                                            'locktime':search_term[0].locktime,
                                                                            'version':search_term[0].version,
                                                                            'block_height':search_term[0].block_height,
                                                                            'coinbase':search_term[0].is_CoinBase,
                                                                            'output_addresses':output_address_list,
                                                                            'input_addresses':input_address_list,
                                                                            'transaction_hash_size':search_term[0].transaction_hash_size,
                                                                            'output_script':output_search_term[0].output_script_value,
                                                                            })





"""
View to search for addresses whether it is an input address or an output address.
It is called when redirected from main search function.
Creates Qr code for each address.
"""
def search_address(request):
     if 'q' in request.GET:
         message = request.GET['q']
         flag = 0
         transaction_list = []
         output_search_term = Output_Table.objects.filter(address=message)
         if not output_search_term:

             input_search_term = Input_Table.objects.filter(input_address=message)
             if not input_search_term:
                 return render(request,'website_api/wrong_search.html')
             else:
                 flag = 1

             search_term = input_search_term
         else:

             search_term = output_search_term
         for i in search_term:
             record_transaction = {'transaction_hash':i.transaction_hash}
             transaction_list.append(record_transaction)

         if flag == 0 or flag == 1:
             qr = qrcode.QRCode(
             version = 1,
             error_correction = qrcode.constants.ERROR_CORRECT_H,
             box_size = 10,
             border = 4,
             )
             if not transaction_list:
                 print("List is empty")
             else:
                 print("not empty")
             qr.add_data(message)
             qr.make(fit=True)
             img = qr.make_image()
             img.save("/home/praful/bitcoin-sql-migrator/website_api/static/qr_codes/{0}.png".format(message),delimiter=",")

             print(flag)
             url = 'http://localhost:8000/static/qr_codes/'+message+'.png'

             if flag == 1:
                 print(transaction_list)
                 return render(request, 'website_api/search_input_address.html',{'Address':message,
                                                                                 'transaction_hash':search_term[0].transaction_hash,
                                                                                 'transaction_index':search_term[0].transaction_index,
                                                                                 'input_script':search_term[0].input_script,
                                                                                 'input_sequence_number':search_term[0].input_sequence_number,
                                                                                 'input_size':search_term[0].input_size,
                                                                                 'image':url,
                                                                                 'transaction_hash_list':transaction_list,
                                                                                 })
             else:
                 return render(request, 'website_api/search_address.html',{'Address':message,
                                                                           'transaction_hash':search_term[0].transaction_hash,
                                                                           'output_no':search_term[0].output_no,
                                                                           'output_type':search_term[0].output_type,
                                                                           'output_value':search_term[0].output_value,
                                                                           'size':search_term[0].size,
                                                                           'image':url,
                                                                           'transaction_hash_list':transaction_list,
                                                                           })


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
