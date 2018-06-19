from blockchain_parser.blockchain import Blockchain
import os
import csv
import json
import threading
from bitcoin_data_app.models import Transaction_Table, Input_Table, Output_Table, Block_Table
from django.http import JsonResponse
from bitcoin_data_handler.settings import BLOCK_DIR, BLOCK_DATA_DIR
#from .. import settings
############### Location of directories ####################
#pass the path for the bitcoin-node data



MAX_NUM_OF_THREAD = 300
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
            self.get_input_table(tx)
            self.get_output_table(tx)

        exit()

    def get_block(self, block):

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

        # print(record)
        block_object = Block_Table.objects.filter(block_hash=block.hash)
        if not block_object:
            loader_block_table = Block_Table(**record)
            loader_block_table.save()
        else:
            print("Entry is already present")



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
                'transaction_hash_size':tx.size,

                }

        tx_object = Transaction_Table.objects.filter(transaction_hash=tx.hash)
        if not tx_object:
            loader_main_table = Transaction_Table(**record)
            loader_main_table.save()
        else:
            print("Entry is already present")



    def get_input_table(self, tx):
        
        for _input in tx.inputs:
            record = {
                        'transaction_hash':Transaction_Table.objects.get(transaction_hash=tx.hash),
                        'transaction_index': _input.transaction_index,
                        'input_sequence_number': _input.sequence_number,
                        'input_size': _input.size,
                        'input_address':None, #todo pointer to object, resolve this
                        'input_script_type': None,
                        'input_script_value': _input.script.value,
                        'input_script_operations': _input.script.operations
                     }


            script_type = None

            if _input.script.is_return is True:
                script_type = 'return'
            elif _input.script.is_p2sh is True:
                script_type = 'p2sh'
            elif _input.script.is_pubkey is True:
                script_type = 'pubkey'
            elif _input.script.is_pubkeyhash is True:
                script_type = 'pubkeyhash'
            elif _input.script.is_multisig is True:
                script_type = 'multisig'
            elif _input.script.is_unknown is True:
                script_type = 'unknown'

            record['input_script_type'] = script_type

            loader_input_table = Input_Table(**record)
            loader_input_table.save()



    def get_output_table(self, tx):
        for number, output in enumerate(tx.outputs):
            for _address in output.addresses:
                record = {
                            'transaction_hash':Transaction_Table.objects.get(transaction_hash=tx.hash),
                            'output_no':number,
                            'output_type':output.type,
                            'output_value':output.value,
                            'size':output.size,
                            'address':_address.address,
                            'output_script_value': output.script.value,
                            'output_script_operations': output.script.operations
                          }



                loader_output_table = Output_Table(**record)
                loader_output_table.save()
