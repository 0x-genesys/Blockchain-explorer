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
############### Location of directories ####################
#pass the path for the bitcoin-node data

MAX_NUM_OF_THREAD = 1

def extract_input_output_main_from_blockchain(start, stop):

    print("BLOCKS accessed")
    print("start "+str(start))
    print("stop "+str(stop))
    thread_class_sync = myThreadSync(str(start), str(stop))
    thread_class_sync.start()



class myThreadSync(threading.Thread):

    def __init__(self, local_start, local_stop):
        threading.Thread.__init__(self)
        self.local_start = local_start
        self.local_stop = local_stop

    def run(self):
        blockchain = Blockchain(BLOCK_DATA_DIR)
        connection.autocommit = False
        for block in blockchain.get_ordered_blocks(BLOCK_DATA_DIR + '/index', start=(int(self.local_start)+1), end=(int(self.local_stop)+1)):
            print("--------------run block "+str(block.height))
            self.get_block(block)
            if int(block.height) % 10 == 0:
                connection.commit()
            print("---------------stop block "+str(block.height))
            gc.collect()
        print("DONE")
        connection.close()
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

        print("starting for block "+str(block.height))
        block_object = Block_Table.objects.filter(block_hash=block.hash)
        if not block_object:
            loader_block_table = Block_Table(**record)
            loader_block_table.save()
        else:
            print("Entry is already present")

        self.get_tx_table(block)


    def get_tx_table(self, block):
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

            transaction = Transaction_Table.objects.filter(transaction_hash=tx.hash)
            if not transaction:
                #transaction does not exist so save it and its inputs and outputs
                transaction_hash_array.append(record)
                self.get_output_table(tx)
                self.get_input_table(tx)

        print("starting for tx "+str(tx.hash))
        Transaction_Table.objects.bulk_create([
                Transaction_Table(**record) for record in transaction_hash_array
            ])


    def get_input_table(self, tx):
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
                            'input_script_value': _input.script.value
                         }
                #We take out address from previous transaction hash and output no.
                # outputs = Output_Table.objects.only('address', 'output_value').filter(transaction_hash_id=_input.transaction_hash, output_no=int(_input.transaction_index))

                # print("outputs " + str(outputs))

                # for output in outputs:
                    # print("output['address'] " + str(output))
                    # record['input_address'] = output.address
                    # record['input_value'] = output.output_value
                    # record['input_script_type'] = output.output_type
                print("starting for inputs from "+str( _input.transaction_hash))
                inputs_to_insert.append(record)
            except:
                continue

        Input_Table.objects.bulk_create([
                Input_Table(**record) for record in inputs_to_insert
            ])


    def get_output_table(self, tx):
        output_to_create = []
        for number, output in enumerate(tx.outputs):
            try:
                for _address in output.addresses:
                    print("Output for "+ tx.hash)
                    record = {
                                'transaction_hash_id': tx.hash,
                                'output_no':number,
                                'output_type':output.type,
                                'output_value':output.value,
                                'size':output.size,
                                'address':_address.address,
                                'output_script_value': output.script.value,
                            }
                    print("starting for outputs of "+str(_address.address))
                    output_to_create.append(record)
            except:
                continue
        Output_Table.objects.bulk_create([
                Output_Table(**record) for record in output_to_create
            ])

def run(*args):
    print(args)
    extract_input_output_main_from_blockchain(args[0], args[1])
