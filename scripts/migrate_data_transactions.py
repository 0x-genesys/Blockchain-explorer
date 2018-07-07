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
        print(block.hash)
        transaction_hash_array = []
        for index, tx in enumerate(block.transactions):
            record = {
                        'transaction_hash':tx.hash,
                        'block_hash_id' : block.hash,
                        'timestamp': block.header.timestamp,
                        'block_size': block.size,
                        'is_CoinBase':'True',
                        'V_in':tx.n_inputs,
                        'V_out':tx.n_outputs,
                        'locktime':tx.locktime,
                        'version':tx.version,
                        'transaction_hash_size':tx.size
                    }

            transaction_hash_array.append(record)

        print("transaction_hash_array>>>>>> " + str(len(transaction_hash_array)))
        Transaction_Table.objects.bulk_create([
                Transaction_Table(**record) for record in transaction_hash_array
            ])

def run(*args):
    get_blocks()
