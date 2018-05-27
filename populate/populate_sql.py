from blockchain_parser.blockchain import Blockchain
import os
import csv


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
ROOT_DIR = os.path.abspath(os.sep)
#return os.path.abspath(os.sep)

#pass the path for the bitcoin-node data
BLOCK_DATA_DIR = os.path.join(ROOT_DIR,'/home/praful/Bitcoin_data/blocks/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK_DIR = os.path.join(BASE_DIR,'populate/csv_files')
############# main_table #############
previous_block_hash = []
block_height = []
time_stamp = []
fees = []
size = []
main_adresses = []

############## OUTPUT ####################
transaction_hash_in = []
output_no = []
output_type = []
output_value = []
size = []
script = []
address = []
########## INPUT #################
transaction_hash_out = []
transaction_index = []
input_script = []
input_sequence_number = []
input_size = []
input_hex = []

def extract_filenames():
    #var = '/home/praful/Bitcoin_data/blocks/'
    file_names_list = []
    for filename in os.listdir(BLOCK_DATA_DIR):
        if(filename.startswith('blk') and filename.endswith('.dat')):
            file_names_list.append(filename)

            print(filename)
    return file_names_list


def extract_input_output_main_from_blockchain():
    filenames = extract_filenames()

    for c, i in enumerate(reversed(filenames)):
        blockchain = Blockchain(BLOCK_DATA_DIR + i)
        for block in blockchain.get_unordered_blocks():
            for tx in block.transactions:
                for no,output in enumerate(tx.outputs):
                    for add in output.address:
                        get_output_table(output, tx, add)

                for inputs in tx.inputs:
                    get_input_table(inputs)

                get_main_table(tx, block)

def get_main_table(tx, block):

    block_height.append(block.header.height)
    previous_block_hash.append(block.header.previous_block_hash)
    time_stamp.append(block.header.timestamp)



def get_output_table(output, tx, add):
    transaction_hash_out.append(tx.hash)
    output_no.append(no)
    output_type.append(output.type)
    output_value.append(output.value)
    size.append(output.size)
    script.append(output.script)
    address.append(output.addresses)

def get_input_table(inputs, tx):
    transaction_hash_in.append(inputs.transaction_hash)
    transaction_index.append(inputs.transaction_index)
    input_script.append(inputs.script)
    input_sequence_number.append(inputs.sequence_number)
    input_size.append(inputs.size)
    input_hex.append(inputs.hex)
