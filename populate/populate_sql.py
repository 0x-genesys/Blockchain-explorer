from blockchain_parser.blockchain import Blockchain
import os
import csv
import json
#from models import main_table, input_table, output_table

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
ROOT_DIR = os.path.abspath(os.sep)
#return os.path.abspath(os.sep)

#pass the path for the bitcoin-node data
BLOCK_DATA_DIR = os.path.join(ROOT_DIR,'/home/praful/Bitcoin_data/blocks/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK_DIR = os.path.join(BASE_DIR,'populate/csv_files')

def extract_input_output_main_from_blockchain():

    #filenames = extract_filenames()
    #filenames=['blk00000.dat']
    blockchain = Blockchain(BLOCK_DATA_DIR)
    for block in blockchain.get_unordered_blocks():
        for tx in block.transactions:
            get_main_table(tx, block)
            get_block_and_blockHeader(tx, block)
            for number,output in enumerate(tx.outputs):
                for add in output.addresses:
                    get_output_table(output, number, tx, add)

            for input in tx.inputs:
                get_input_table(input,tx)

def get_main_table(tx, block):
    record = {'transaction_hash':tx.hash,
            'block_height' : block.height,
            'block_size':block.size,
            'is_CoinBase':tx.is_coinbase,
            'V_in':tx.n_inputs,
            'V_out':tx.n_outputs,
            'locktime':tx.locktime,
            'version':tx.version,

            }

def get_block_and_blockHeader(tx, block):
    record = {'transaction_hash':tx.hash,
            'previous_block_hash':block.header.previous_block_hash,
            'merkle_root':block.header.merkle_root,
            'timestamp':block.header.timestamp,
            'block_header_version':block.header.version,
            'bits':block.header.bits,
            'nonce':block.header.nonce,
            'difficulty':block.header.difficulty,
            }


def get_output_table(output, number, tx, add):
    record = {'transaction':tx.hash,
    'output_no':number,
    'output_type':output.type,
    'output_value':output.value,
    'size':output.size,
    'script':output.script,
    'address':add.address,
            }



def get_input_table(input, tx):
    record ={'transaction_hash':tx.hash,
    'transaction_index': input.transaction_index,
    'input_script': input.script,
    'input_sequence_number': input.sequence_number,
    'input_size': input.size,
    'input_hex': input.hex
            }




##########   INITIATILIZING MODEL CLASS VARIABLES FOR DATA LOADING   ################
'''
loader_main_table = main_table()
loader_input_table = input_table()
loader_output_table = output_table()

'''
def main():
    extract_input_output_main_from_blockchain()

if __name__ == '__main__':
    main()
