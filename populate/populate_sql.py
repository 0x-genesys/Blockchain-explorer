from blockchain_parser.blockchain import Blockchain
import os
import csv
import json
import threading
#from populate import models
from populate.models import Transaction_Table, Input_Table, Output_Table, Block_Table
from django.http import JsonResponse

#from .. import settings
############### Location of directories ####################
#pass the path for the bitcoin-node data

ROOT_DIR = os.path.abspath(os.sep)
# BLOCK_DATA_DIR = os.path.join(ROOT_DIR,'/home/praful/Bitcoin_data/blocks')
BLOCK_DATA_DIR = os.path.join(ROOT_DIR,'/Users/karanahuja/Library/Application Support/Bitcoin/blocks/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK_DIR = os.path.join(BASE_DIR,'populate/csv_files')

MAX_NUM_OF_THREAD = 20
threadLimiter = threading.BoundedSemaphore(MAX_NUM_OF_THREAD)



def extract_input_output_main_from_blockchain(request):
        
        blockchain = Blockchain(BLOCK_DATA_DIR)
        print("blocks accessed")
        threads = []
        for block in blockchain.get_ordered_blocks(BLOCK_DATA_DIR + '/index',start=0, end=210000):
            thread1 = myThread(block)
            thread1.start()
            threads.append(thread1)

            for thread in threads:
                thread.join()

            count_thread = threading.active_count()

            while count_thread > MAX_NUM_OF_THREAD:
                print("threading active_count >>>>>>>>>>>>"+str(count_thread))
                continue

        return JsonResponse({"res":""}, status=200)



class myThread(threading.Thread):

    def __init__(self, block):
        threading.Thread.__init__(self)
        self.block = block

    def run(self):
        print("run block "+str(self.block.height))
        self.get_block(self.block)
        print("len of tx "+str(len(self.block.transactions)))

        for index, tx in enumerate(self.block.transactions):
            print("run tx "+str(tx.hash))
            self.get_tx_table(tx, self.block)

            for input in tx.inputs:
                self.get_input_table(input,tx)

            for number,output in enumerate(tx.outputs):
                for add in output.addresses:
                    self.get_output_table(output, number, tx, add)

        exit()

    def get_block(self, block):
        record = {
            'block_hash':block.hash,
            'block_header':block.header,
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

        # print(record)

        loader_block_table = Block_Table(**record)

        loader_block_table.save()



    def get_tx_table(self, tx, block):
        record = {
                'transaction_hash':tx.hash,
                'block_height' : Block_Table.objects.get(block_height=block.height),
                'block_size':block.size,
                'is_CoinBase':'True',
                'V_in':tx.n_inputs,
                'V_out':tx.n_outputs,
                'locktime':tx.locktime,
                'version':tx.version,
                #'raw_hex':tx.hash,
                }
        # print(record)
        loader_main_table = Transaction_Table(**record)
        loader_main_table.save()


    def get_input_table(self, input, tx):
        record ={
                'transaction_hash':Transaction_Table.objects.get(transaction_hash=tx.hash),
                'transaction_index': input.transaction_index,
                'input_script': input.script,
                'input_sequence_number': input.sequence_number,
                'input_size': input.size,
                #'input_hex': input.hex
                }

        loader_input_table = Input_Table(**record)
        loader_input_table.save()

    def get_output_table(self, output, number, tx, add):
        record = {
                    'transaction_hash':Transaction_Table.objects.get(transaction_hash=tx.hash),
                    'output_no':number,
                    'output_type':output.type,
                    'output_value':output.value,
                    'size':output.size,
                    'script':output.script,
                    'address':add.address,
                  }

        loader_output_table = Output_Table(**record)
        loader_output_table.save()







print("Exiting Thread")
#return 0
#def main(request):
