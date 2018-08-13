from blockchain_parser.blockchain import Blockchain
import os
import gc
import csv
import json
import threading
import sys
from bitcoin_data_app.models import Transaction_Table, Input_Table, Output_Table, Block_Table
from django.http import JsonResponse
from django.db import connection
from app.settings import BLOCK_DATA_DIR
############### Location of directories ####################
#pass the path for the bitcoin-node data


def extract_block_from_sql(block_number):
    block = get_block(block_number)
    txs = Transaction_Table.objects.filter(block_hash_id=block.block_hash)
    outputs = Output_Table.objects.filter(transaction_hash_id__in=create_tx_array(txs))
    check_if_big_tx_occurred(txs,outputs)


def check_if_big_tx_occurred(txs, outputs):
    for tx in txs:
        print(tx.transaction_hash)
        total_amount_moved = 0
        for output in outputs:
            if tx.transaction_hash == output.transaction_hash_id:
                amount = int(output.output_value)
                amount_in_btc = amount / 100000000
                total_amount_moved = total_amount_moved + amount_in_btc
                
        print("amount_in_btc "+str(amount_in_btc)+"for "+tx.transaction_hash)

        if(amount_in_btc > 1000):
            print("huge movement")
            #tweet here

def get_block(block_number):
    block = Block_Table.objects.filter(block_height=block_number)
    if len(block) == 0:
        print("block not found")
        sys.exit()
    else:
        block = block[0]
    return block


def create_tx_array(txs):
    tx_array = []
    for tx in txs:
        tx_array.append(tx.transaction_hash)

    return tx_array


def run(*args):
    print(args)
    extract_block_from_sql(args[0])
