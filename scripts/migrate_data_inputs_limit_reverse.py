from blockchain_parser.blockchain import Blockchain
import os
import gc
import csv
import json
import threading
from bitcoin_data_app.models import Transaction_Table, Input_Table, Output_Table, Block_Table
from django.http import JsonResponse
from django.db import connection
import math
import time
from app.settings import BLOCK_DATA_DIR


#start > stop (reverse)
def get_blocks(start, stop):
    start = int(start)
    stop = int(stop)
    net = stop - start

    bucket = 100000
    limit = math.ceil(net / bucket)

    print("Limit value is "+ str(limit))

    for i in range(limit):
        local_start = start + (i*bucket)
        local_stop = local_start + bucket
        local_start = str(local_start)
        local_stop = str(local_stop)
        thread1 = Mythread(local_start, local_stop)
        thread1.start()


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
            print("For block "+ str(block.height))
            time.sleep(0.1)


    def get_tx_table(self, block):
        for tx in block.transactions:
            time.sleep(.001)
            self.get_input_table(tx)


    def get_input_table(self, tx):
            inputs_to_insert = []
            for _input in tx.inputs:
                try:
                    previous_transaction_hash = ''

                    if(_input.transaction_hash != '0000000000000000000000000000000000000000000000000000000000000000'):
                        previous_transaction_hash  = _input.transaction_hash


                    print("previous_transaction_hash "+str(previous_transaction_hash))

                    record = {
                                'transaction_hash_id': tx.hash,
                                'previous_transaction_hash':  previous_transaction_hash,
                                'transaction_index': _input.transaction_index,
                                'input_sequence_number': _input.sequence_number,
                                'input_size': _input.size,
                                'input_address':None,
                                'input_value': None,
                                'input_script_type': None,
                                'input_script_value': _input.script.value,
                                'input_script_operations': _input.script.operations
                             }
                    if previous_transaction_hash != '':
                      #We take out address from previous transaction hash and output no.
                      outputs = Output_Table.objects.only('address', 'output_value').filter(transaction_hash_id=str(previous_transaction_hash), output_no=str(_input.transaction_index))

                      for output in outputs[0]:
                          # print("output['address'] " + str(output))
                          record['input_address'] = output.address
                          record['input_value'] = output.output_value
                          record['input_script_type'] = output.output_type
                      inputs_to_insert.append(record)
                except:
                    continue

            Input_Table.objects.bulk_create([
                    Input_Table(**record) for record in inputs_to_insert
                ])

def run(*args):
    get_blocks(args[0], args[1])
