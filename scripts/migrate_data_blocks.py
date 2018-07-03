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

def extract_input_output_main_from_blockchain(start, stop):

    blockchain = Blockchain(BLOCK_DATA_DIR)
    print("BLOCKS accessed")
    print("start "+str(start))
    print("stop "+str(stop))
    count = 0
    blocks = []

    for block in blockchain.get_ordered_blocks(BLOCK_DATA_DIR + '/index', start=int(start), end=int(stop)):
        record = {
            'block_hash':block.hash,
            'block_header':block.header.previous_block_hash,
            'block_no_of_transactions':block.n_transactions,
            'block_size':block.size,
            'block_height':block.height,
            'block_header_version':block.header.version,
            'previous_block_hash':block.header.previous_block_hash,
            'merkle_root':block.header.merkle_root,
            'timestamp':block.header.timestamp,
            'bits':block.header.bits,
            'nonce':block.header.nonce,
            'difficulty':block.header.difficulty
        }
        print(str(block.height))
        blocks.append(record)
        if count % 50 == 0:
            Block_Table.objects.bulk_create([
                Block_Table(**record) for record in blocks
            ])
            blocks = []
        count = count + 1


def run(*args):
    print(args)
    extract_input_output_main_from_blockchain(args[0], args[1])
