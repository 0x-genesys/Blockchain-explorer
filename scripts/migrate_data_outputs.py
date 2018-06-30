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


def get_blocks():
    blockchain = Blockchain(BLOCK_DATA_DIR)
    for block in blockchain.get_unordered_blocks():
        get_tx_table(block)


def get_tx_table(block):
    for tx in block.transactions:
        get_output_table(tx)


def get_output_table(tx):
    output_to_create = []
    for number, output in enumerate(tx.outputs):
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

    Output_Table.objects.bulk_create([
            Output_Table(**record) for record in output_to_create
        ])