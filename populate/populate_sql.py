from blockchain_parser.blockchain import Blockchain
import os
import csv
import json
#from populate import models
from populate.models import Transaction_Table, Input_Table, Output_Table, Block_Table
#from .. import settings
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
ROOT_DIR = os.path.abspath(os.sep)
#return os.path.abspath(os.sep)

#pass the path for the bitcoin-node data
BLOCK_DATA_DIR = os.path.join(ROOT_DIR,'/home/praful/Bitcoin_data/blocks/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK_DIR = os.path.join(BASE_DIR,'populate/csv_files')

def extract_input_output_main_from_blockchain(request):


    #filenames = extract_filenames()
    #filenames=['blk00000.dat']
    print("running")
    blockchain = Blockchain(BLOCK_DATA_DIR)
    for block in blockchain.get_ordered_blocks(BLOCK_DATA_DIR + '/index',start=0, end=210000):
        for index, tx in enumerate(block.transactions):
            #get_block_header(tx, block)
            get_block(tx, block, index)
            get_main_table(tx, block)

            for input in tx.inputs:
                get_input_table(input,tx)

            for number,output in enumerate(tx.outputs):
                for add in output.addresses:
                    get_output_table(output, number, tx, add)




def get_block(tx, block, index):
    record = {'block_hash':block.hash,
    'block_header':block.header,
    'block_no_of_transactions':block.n_transactions,
    'block_size':block.size,
    'block_height':block.height,
    #'Block Header data
    'block_header_version':block.header.version,
    'previous_block_hash':block.header.previous_block_hash,
    'merkle_root':block.header.merkle_root,
    'timestamp':block.header.timestamp,
    'bits':block.header.bits,
    'nonce':block.header.nonce,
    'difficulty':block.header.difficulty,
    }

    #print(record)
    loader_block_table = Block_Table(**record)
    loader_block_table.save()


def get_main_table(tx, block):
    record = {'transaction_hash':tx.hash,
            'block_height' : Block_Table.objects.get(block_height=block.height),
            'block_size':block.size,
            'is_CoinBase':'True',
            'V_in':tx.n_inputs,
            'V_out':tx.n_outputs,
            'locktime':tx.locktime,
            'version':tx.version,
            #'raw_hex':tx.hash,
            }
    print(record)
    loader_main_table = Transaction_Table(**record)
    loader_main_table.save()


def get_input_table(input, tx):
    record ={'transaction_hash':Transaction_Table.objects.get(transaction_hash=tx.hash),
    'transaction_index': input.transaction_index,
    'input_script': input.script,
    'input_sequence_number': input.sequence_number,
    'input_size': input.size,
    #'input_hex': input.hex
            }
    loader_input_table = Input_Table(**record)
    loader_input_table.save()

def get_output_table(output, number, tx, add):
    record = {'transaction_hash':Transaction_Table.objects.get(transaction_hash=tx.hash),
    'output_no':number,
    'output_type':output.type,
    'output_value':output.value,
    'size':output.size,
    'script':output.script,
    'address':add.address,
            }
    loader_output_table = Output_Table(**record)
    loader_output_table.save()
