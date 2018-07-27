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
def start():
    kill_active_queries()


def kill_active_queries():
	try:
		print("create bitcoin_data_app_output_table index")
		query = "select pid,backend_start from pg_stat_activity where state = 'active'"
		response = execute_query(query)
		print(response)

		for pid in response:
			try:
				query = "select pg_cancel_backend(" + str(pid['pid']) +")"
				response = execute_query(query)
				print(response)
			except Exception as err:
				print(err)
				continue
		
	except Exception as err:
		print(err)

def execute_query(query):
    cursor = connection.cursor()
    cursor.execute(query)

    field_names = [item[0] for item in cursor.description]
    rawData = cursor.fetchall()

    #convert list tuple data to dictionary meaningful data
    result = []
    for row in rawData:
        objDict = {}
        for index, value in enumerate(row):
            objDict[field_names[index]] = value
        result.append(objDict)
    cursor.close()

    return result

def run(*args):
    start()
