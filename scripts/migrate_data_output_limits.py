from blockchain_parser.blockchain import Blockchain
import os
import gc
import csv
import json
import threading
from bitcoin_data_app.models import Transaction_Table, Input_Table, Output_Table, Block_Table
from django.http import JsonResponse
from django.db import connection
from app.settings import BLOCK_DATA_DIR
#from .. import settings
############### Location of directories ####################
#pass the path for the bitcoin-node data


def get_blocks(start, stop):
    blockchain = Blockchain(BLOCK_DATA_DIR)
    print("BLOCKS accessed")
    print("start "+str(start))
    print("stop "+str(stop))

    for block in blockchain.get_ordered_blocks(BLOCK_DATA_DIR + '/index', start=int(start), end=int(stop)):
        outputs = get_tx_table(block)

        print("WRITING " + str(len(outputs)))
        Output_Table.objects.bulk_create([
            Output_Table(**record) for record in outputs
        ])


def get_tx_table(block):
    outputs = []

    for tx in block.transactions:
        outputs = outputs + get_output_table(tx)

    return outputs

        


def get_output_table(tx):
    output_to_create = []
    for number, output in enumerate(tx.outputs):
        try:
            for _address in output.addresses:
                print("Output for "+ tx.hash)
                record = {
                            'transaction_hash_id': tx.hash,
                            'output_no':number,
                            'output_type':output.type,
                            'output_value':output.value,
                            'size':output.size,
                            'address':_address.address,
                            'output_script_value': output.script.value,
                            'output_script_operations': output.script.operations
                        }
                output_to_create.append(record)
        except:
            continue

    return output_to_create

    
def run(*args):
    get_blocks(args[0], args[1])