from blockchain_parser.blockchain import Blockchain
import os
import gc
import csv
import json
import threading
import time
from bitcoin_data_app.models import Transaction_Table, Input_Table, Output_Table, Block_Table
from django.http import JsonResponse
from django.db import connection
from app.settings import BLOCK_DATA_DIR
import math
#from .. import settings
############### Location of directories ####################
#pass the path for the bitcoin-node data


'''
**NOTE**: You must manually/programmatically delete the cache file in order to rebuild the cache.
 Don't forget to do this each time you would like to re-parse the blockchain with a higher block height 
 than the first time you saved the cache file as the new blocks will not be included in the cache.
'''
def get_blocks(start, stop):
    start = int(start)
    stop = int(stop)
    net = stop - start
    bucket = 20000
    limit = math.floor(net / bucket)

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
            self.get_output_table(tx)


    def get_output_table(self, tx):
        outputs = []
        for number, output in enumerate(tx.outputs):
            try:
                output_type = output.type
                output_value = output.value
                output_size = output.size
                script_value = output.script.value
                script_operations = output.script.operations
                for _address in output.addresses:
                    record = {
                                'transaction_hash_id': tx.hash,
                                'output_no':number,
                                'output_type':output_type,
                                'output_value':output_value,
                                'size':output_size,
                                'address':_address.address,
                                'output_script_value': script_value,
                                'output_script_operations': script_operations
                            }
                    outputs.append(record)
            except:
                continue

        Output_Table.objects.bulk_create([
                Output_Table(**record) for record in outputs
            ])

    
def run(*args):
    get_blocks(args[0], args[1])
