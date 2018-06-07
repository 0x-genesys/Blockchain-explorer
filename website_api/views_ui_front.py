from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from bitcoin_data_app.models import Block_Table, Transaction_Table, Output_Table, Input_Table

from django.urls import reverse_lazy
import qrcode
from django.http import HttpResponse, JsonResponse
#import JsonResponse
import os

def base_view(request):



    #display_object = Block_Table.objects.raw('select * from populate_block_table order by timestamp desc limit 5')
    return render(request,'website_api/base.html')

def recent_data(request):
    display_object = Block_Table.objects.all().order_by('timestamp')[:5]
    block_hash_list = []
    block_header_list = []
    block_no_of_transactions_list = []
    block_size_list = []
    block_height_list = []
    timestamp_list = []

    output = []
    #print("its here")
    if not display_object:
        print("nothing")
    else:

        #print(display_object[0].block_hash)
        for i in range(0,5):
            block_hash_list.append(display_object[i].block_hash)
            block_header_list.append(display_object[i].block_header)
            block_no_of_transactions_list.append(display_object[i].block_no_of_transactions)
            block_size_list.append(display_object[i].block_size)
            block_height_list.append(display_object[i].block_height)
            timestamp_list.append(display_object[i].timestamp)
            record = {'block_hash_list':display_object[i].block_hash,
                                                        'block_header_list':display_object[i].block_header,
                                                        'block_no_of_transactions_list':display_object[i].block_no_of_transactions,
                                                        'block_size_list':display_object[i].block_size,
                                                        'block_height_list':display_object[i].block_height,
                                                        'timestamp_list':display_object[i].timestamp,
                                                        }
            output.append(record)

        record = {}

        print(record)
            #print(list[i])
        return render(request,'website_api/recent_data.html',{'output':output,
                                                                'range':range(5)})

def recent_hundred_data(request):
    display_object = Block_Table.objects.all().order_by('timestamp')[:100]
    block_hash_list = []
    block_header_list = []
    block_no_of_transactions_list = []
    block_size_list = []
    block_height_list = []
    timestamp_list = []

    output = []

    for i in range(0,100):
        block_hash_list.append(display_object[i].block_hash)
        block_header_list.append(display_object[i].block_header)
        block_no_of_transactions_list.append(display_object[i].block_no_of_transactions)
        block_size_list.append(display_object[i].block_size)
        block_height_list.append(display_object[i].block_height)
        timestamp_list.append(display_object[i].timestamp)
        record = {'block_hash_list':display_object[i].block_hash,
                                                    'block_header_list':display_object[i].block_header,
                                                    'block_no_of_transactions_list':display_object[i].block_no_of_transactions,
                                                    'block_size_list':display_object[i].block_size,
                                                    'block_height_list':display_object[i].block_height,
                                                    'timestamp_list':display_object[i].timestamp,
                                                    }
        output.append(record)

    record = {}

    print(record)
        #print(list[i])
    return render(request,'website_api/recent_data.html',{'output':output,
                                                            'range':range(5)})



def search_block_hash(request):
    if 'q' in request.GET:
        message = request.GET['q']
        #print(message)
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
            # final_list.append(i.transaction_hash)
            # for add in input_address_search_term:
            #     final_list.append(add.address)
            # for add in output_address_search_term:
            #     final_list.append(add.input_address)
            if not input_address_search_term:
                print("NOT")
            for add in output_address_search_term:


                output_address_list.append(add.address)
            for add in input_address_search_term:
                input_address_list.append(add.input_address)
            print(output_address_list)
            record_output_address = {'transaction_hash':i.transaction_hash,
                                      'output_address':output_address_list,
                                      'input_address':input_address_list,
                                      'flag':c}
            final_list.append(record_output_address)
            # output_address_list.append('0')
            # input_address_list.append('0')
        #print(final)
        # for x in input_address_list:
        #     a, b = x.split('(')
        #     final, temp = b.split(',')
        #     input_address_list_final.append(final)
        #
        #print(transaction_list)
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
                                                                'c':c,
                                                                })
                                                                # 'transactions':transaction_list,
                                                                # 'output_addresses':output_address_list,
                                                                # 'input_addresses':input_address_list,
                                                                # 'c':c,


def search_transaction_hash(request):
    if 'q' in request.GET:
        message = request.GET['q']
        search_term = Transaction_Table.objects.filter(transaction_hash=message)
        print(message)
        if not search_term:
            return render(request,'website_api/wrong_search.html')
            print("hash not present")
        else:
            print("present")

    return render(request, 'website_api/search_transaction_hash.html',{'transaction_hash':search_term[0].transaction_hash,
                                                                        'block_size':search_term[0].block_size,
                                                                        'Number_of_inputs':search_term[0].V_in,
                                                                        'Number_of_outputs':search_term[0].V_out,
                                                                        'locktime':search_term[0].locktime,
                                                                        'version':search_term[0].version,
                                                                        'block_height':search_term[0].block_height,
                                                                        })


def search_address(request):
    if 'q' in request.GET:
        message = request.GET['q']
        flag = 0

        output_search_term = Output_Table.objects.filter(address=message)
        if not output_search_term:

            input_search_term = Input_Table.objects.filter(input_address=message)
            if not input_search_term:
                return render(request,'website_api/wrong_search.html')
            else:
                flag = 1

            #print("no output")
            search_term = input_search_term
        else:
            #print("no input")
            #flag = 2
            search_term = output_search_term
        if flag == 0 or flag == 1:
            qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = 10,
            border = 4,
            )
            qr.add_data(message)
            qr.make(fit=True)
            img = qr.make_image()
            img.save("/home/praful/bitcoin-sql-migrator/website_api/static/qr_codes/{0}.png".format(message),delimiter=",")
            #response = HttpResponse(content_type="image/png")
            #url.save(response,"PNG")
            #print(search_term)
            print(flag)
            url = 'http://localhost:8000/static/'+message+'.png'
            if flag == 1:
                return render(request, 'website_api/search_input_address.html',{'Address':message,
                                                                                'transaction_hash':search_term[0].transaction_hash,
                                                                                'transaction_index':search_term[0].transaction_index,
                                                                                'input_script':search_term[0].input_script,
                                                                                'input_sequence_number':search_term[0].input_sequence_number,
                                                                                'input_size':search_term[0].input_size,
                                                                                'image':url,
                                                                                })
            else:
                return render(request, 'website_api/search_address.html',{'Address':message,
                                                                          'transaction_hash':search_term[0].transaction_hash,
                                                                          'output_no':search_term[0].output_no,
                                                                          'output_type':search_term[0].output_type,
                                                                          'output_value':search_term[0].output_value,
                                                                          'size':search_term[0].size,
                                                                          'image':url,
                                                                          })



def wrong_query(request):
    return render(request,'website_api/wrong_search.html')
