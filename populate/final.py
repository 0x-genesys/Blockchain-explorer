#from sql_populate import settings
#from django.conf.settings import *
#import sys
#from BASE_DIR.python-bitcoin-blockchain-parser-master.blockchain_parser.blockchain import Blockchain
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
def extract_output_from_blockchain():
    # List variables for populating blockchain in json, csv
    transaction_hash = []
    output_no = []
    output_type = []
    output_value = []
    size = []
    script = []
    address = []
    #var = '/home/praful/Bitcoin_data/blocks/'
    filenames = extract_filenames()

    for c, i in enumerate(reversed(filenames)):
        blockchain = Blockchain(BLOCK_DATA_DIR + i)
        for block in blockchain.get_unordered_blocks():
            for tx in block.transactions:
                for no, output in enumerate(tx.outputs):
                    transaction_hash.append(tx.hash)
                    output_no.append(no)
                    output_type.append(output.type)
                    output_value.append(output.value)
                    size.append(output.size)
                    script.append(output.script)
                    address.append(output.addresses)
    print ("extract_output_from_blockchain is working")
    return transaction_hash, output_no, output_type, output_value, size, script, address,

def extract_filenames():
    #var = '/home/praful/Bitcoin_data/blocks/'
    file_names_list = []
    for filename in os.listdir(BLOCK_DATA_DIR):
        if(filename.startswith('blk') and filename.endswith('.dat')):
            file_names_list.append(filename)

            print(filename)
    return file_names_list



def extract_input_from_blockchain():
    #var = '/home/praful/Bitcoin_data/blocks/'
    transaction_hash = []
    transaction_index = []
    input_script = []
    input_sequence_number = []

    input_size = []

    input_hex = []
    print("initiated")
    filenames = extract_filenames()
    for c, i in enumerate(reversed(filenames)):
        blockchain = Blockchain(BLOCK_DATA_DIR + i)
        for block in blockchain.get_unordered_blocks():
            for tx in block.transactions:
                for inputs in tx.inputs:
                    transaction_hash.append(inputs.transaction_hash)
                    transaction_index.append(inputs.transaction_index)
                    input_script.append(inputs.script)
                    input_sequence_number.append(inputs.sequence_number)
                    input_size.append(inputs.size)
                    input_hex.append(inputs.hex)
    print ("extract_input_from_blockchain is working")
    return transaction_hash, transaction_index, input_script, input_sequence_number, input_size, input_hex, 'input'



def generate_csv():
    transaction_hash, transaction_index, input_script, input_sequence_number, input_size, input_hex, flag = extract_input_from_blockchain()
    transaction, output_no, output_type, output_value, size, script, address = extract_output_from_blockchain()
    filenames = extract_filenames()
    #myFilePath = '/home/praful/extras/'
    print("generate_csv initiated")
    if(flag == 'input'):
        with open(BLOCK_DIR + 'input' + '.csv', "wb") as f:
            fieldnames = ['transaction_hash', 'transaction_index', 'input_script', 'input_sequence_number', 'input_size', 'input_hex']
            writer = csv.DictWriter(f, dialect='excel',fieldnames = fieldnames)#, encoding='utf-8')
            writer.writeheader()
            for i in range(len(transaction_hash)):

                record = {'transaction_hash':transaction_hash[i],
                'transaction_index': transaction_index[i],
                'input_script': input_script[i],
                'input_sequence_number': input_sequence_number[i],
                'input_size': input_size[i],
                'input_hex': input_hex}

                writer.writerow(record)


    else :


        with open(BLOCK_DIR + '_output' + '.csv', "wb") as f:
            fieldnames = ['transaction', 'output_no', 'output_type', 'output_value', 'size script', 'address']
            writer = csv.DictWriter(f, dialect='excel',fieldnames = fieldnames)#, encoding='utf-8')
            writer.writeheader()
            for i in range(len(transaction)):

                record = {'transaction':transaction,
                 'output_no':output_no,
                  'output_type':output_type,
                   'output_value':output_value,
                    'size':size, 'script':script,
                     'address':address}

            writer.writerow(record)




def main():
    #print(ROOT_DIR)
    #print(BLOCK_DATA_DIR)
    extract_filenames()
    extract_input_from_blockchain()
    generate_csv()
    print(" input files are populated")
    extract_output_from_blockchain()
    print('output files are populated')

if __name__ == '__main__':
    main()
