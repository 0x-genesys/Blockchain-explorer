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
from scripts.migrate_data_blocks import extract_input_output_main_from_blockchain
from scripts.migrate_data_transactions import get_blocks as get_blocks_for_transactions
from scripts.migrate_data_outputs import get_blocks as  get_blocks_for_outputs
from scripts.migrate_data_inputs import get_blocks as  get_blocks_for_inputs
from django.db import connection
import django

#Start the entire migration sync
# although blocks limit are being taken as arguments
#output and input are syncd entirely
#to sync per block use migrate_data
def start(start, stop):
    extract_input_output_main_from_blockchain(start, stop)
    get_blocks_for_transactions()
    #get_blocks_for_outputs()
    #create_pre_indexes()
    #get_blocks_for_inputs()
    #create_post_indexes()
    #create_input_indexes()
    #Call inputs manually after making index on output's tx id else super slow


def create_pre_indexes():
	cursor = connection.cursor()

	try:
		cursor.execute('''create index output_tx_hash_output_no on bitcoin_data_app_output_table(transaction_hash_id, output_no)''')
	except (django.db.utils.ProgrammingError) as err:
		print("Already exists")


	cursor.close()


def create_post_indexes():
	cursor = connection.cursor()

	try:
		cursor.execute('''create index transaction_block_hash_id on bitcoin_data_app_transaction_table(block_hash_id)''')
	except (django.db.utils.ProgrammingError) as err:
		print("Already exists")

	try:
		cursor.execute('''create index transaction_tx_hash on bitcoin_data_app_transaction_table(transaction_hash)''')
	except (django.db.utils.ProgrammingError) as err:
		print("Already exists")

	try:
		cursor.execute('''create index input_address_index on bitcoin_data_app_output_table(address)''')
	except (django.db.utils.ProgrammingError) as err:
		print("Already exists")

	try:
		cursor.execute('''create index block_height_index on bitcoin_data_app_block_table(block_height)''')
	except (django.db.utils.ProgrammingError) as err:
		print("Already exists")

	cursor.close()


def create_input_indexes():
	try:
		cursor.execute('''create index input_tx_hash on bitcoin_data_app_input_table(transaction_hash_id)''')
	except (django.db.utils.ProgrammingError) as err:
		print("Already exists")

	try:
		cursor.execute('''create index output_address_index on bitcoin_data_app_input_table(input_address)''')
	except (django.db.utils.ProgrammingError) as err:
		print("Already exists")
	

#NOTE TX and ouput will be fully synced
#If you need to sync selective use migrate_data.py
def run(*args):
    start(args[0], args[1])
