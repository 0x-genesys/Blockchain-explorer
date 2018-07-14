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

def get_blocks():
    blockchain = Blockchain(BLOCK_DATA_DIR)
    for block in blockchain.get_unordered_blocks():
        get_tx_table(block)


def get_tx_table(block):
    for tx in block.transactions:
        get_input_table(tx)


def get_input_table(tx):
        inputs_to_insert = []
        for _input in tx.inputs:
            try:
                print("_input.transaction_hash. "+str(_input.transaction_hash))

                record = {
                            'transaction_hash_id': tx.hash,
                            'previous_transaction_hash':  _input.transaction_hash,
                            'transaction_index': _input.transaction_index,
                            'input_sequence_number': _input.sequence_number,
                            'input_size': _input.size,
                            'input_address':None,
                            'input_value': None,
                            'input_script_type': None,
                            'input_script_value': _input.script.value,
                            'input_script_operations': _input.script.operations
                         }
                         
                #We take out address from previous transaction hash and output no.
                outputs = Output_Table.objects.only('address', 'output_value').filter(transaction_hash_id=_input.transaction_hash, output_no=int(_input.transaction_index))

                for output in outputs:
                    print("output['address'] " + str(output))
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
    get_blocks()