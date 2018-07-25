from blockchain_parser.blockchain import Blockchain
import os
import gc
import csv
import json
import threading
from bitcoin_data_app.models import Transaction_Table, Input_Table_Temp, Output_Table, Block_Table
from django.http import JsonResponse
from django.db import connection
import math
import time
from app.settings import BLOCK_DATA_DIR


#start > stop (reverse)
def get_blocks(start, stop):
    thread1 = Mythread(start, stop)
    thread1.start()
    # net = stop - start

    # bucket = 100000
    # limit = math.ceil(net / bucket)

    # print("Limit value is "+ str(limit))

    # for i in range(limit):
    #     local_start = start + (i*bucket)
    #     local_stop = local_start + bucket
    #     local_start = str(local_start)
    #     local_stop = str(local_stop)
    #     thread1 = Mythread(local_start, local_stop)
    #     thread1.start()


class Mythread(threading.Thread):

    def __init__(self, start_local, stop_local):
        threading.Thread.__init__(self)
        self.start_local = start_local
        self.stop_local = stop_local

    def run(self):
        blockchain = Blockchain(BLOCK_DATA_DIR)
        print("BLOCKS accessed")
        print("start "+self.start_local)
        print("stop "+self.stop_local)

        for block in blockchain.get_ordered_blocks(BLOCK_DATA_DIR + '/index', int(self.start_local), int(self.stop_local), 'index-cache.pickle'):
            self.get_tx_table(block)
            print("\n\n\nFor block "+ str(block.height))
            time.sleep(0.1)


    def get_tx_table(self, block):
        for tx in block.transactions:
            time.sleep(.001)
            self.get_input_table(tx)


    def get_input_table(self, tx):
            inputs_to_insert = []
            # previous_transactions = []
            for _input in tx.inputs:
               try:
                    previous_transaction_hash = None
                    print("\n _input.transaction_hash " + str(_input.transaction_hash))
                    print("for transaction_hash_id " + str(tx.hash))
                    if(str(_input.transaction_hash) != '0000000000000000000000000000000000000000000000000000000000000000'):
                        previous_transaction_hash  = str(_input.transaction_hash)
                        # previous_transactions.append(previous_transaction_hash)

                    print("previous_transaction_hash "+str(previous_transaction_hash))

                    record_data = {
                                'transaction_hash_id': tx.hash,
                                'previous_transaction_hash':  previous_transaction_hash,
                                'transaction_index': str(_input.transaction_index),
                                'input_sequence_number': _input.sequence_number,
                                'input_size': _input.size,
                                'input_address':None,
                                'input_value': None,
                                'input_script_type': None,
                                'input_script_value': _input.script.value,
                                'input_script_operations': _input.script.operations
                             }
                    print("writing previous_transaction_hash " + str(record_data['previous_transaction_hash']))
                    inputs_to_insert.append(record_data)
               except Exception as e:
                  print("error >>>>>>>>>>>>>. "+str(e) )
                  continue

            # if len(previous_transactions) > 0:
            #     outputs = Output_Table.objects.only('address', 'output_value','output_type', 'output_no', 'transaction_hash_id').filter(transaction_hash_id__in=previous_transactions)
            #     for output in outputs:
            #         for _input in inputs_to_insert:
            #             # print(_input['previous_transaction_hash'] + "  " + output.transaction_hash_id )
            #             # print(_input['transaction_index'] + "  " + output.output_no)
            #             if _input['previous_transaction_hash'] == output.transaction_hash_id and output.output_no == _input['transaction_index']:
            #                 # print("inserting inputs")
            #                 # print("\n_input >>> " + str(_input))
            #                 # print("\noutput >>> " + str(output))
            #                 _input['input_address'] = output.address
            #                 _input['input_value'] = output.output_value
            #                 _input['input_script_type'] = output.output_type
            Input_Table_Temp.objects.bulk_create([
                    Input_Table_Temp(**record) for record in inputs_to_insert
                ])

def run(*args):
    get_blocks(args[0], args[1])
