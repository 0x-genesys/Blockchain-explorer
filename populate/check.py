from blockchain_parser.blockchain import Blockchain
import os
import csv
import sys
#from blockchain_parser.blockchain  blockch import Blockchain
ROOT_DIR = os.path.abspath(os.sep)
#return os.path.abspath(os.sep)

#pass the path for the bitcoin-node data
BLOCK_DATA_DIR = os.path.join(ROOT_DIR,'/home/praful/Bitcoin_data/blocks/')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK_DIR = os.path.join(BASE_DIR,'populate/csv_files')
# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blockchain = Blockchain(BLOCK_DATA_DIR)
'''
for block in blockchain.get_unordered_blocks():
    for tx in block.transactions:
        for no, output in enumerate(tx.outputs):
            print("tx=%s outputno=%d type=%s value=%s" % (tx.hash, no, output.type, output.value))
'''
# To get the blocks ordered by height, you need to provide the path of the
# `index` directory (LevelDB index) being maintained by bitcoind. It contains
# .ldb files and is present inside the `blocks` directory
for block in blockchain.get_ordered_blocks(BLOCK_DATA_DIR+ '/index', end=1000):
    print("height=%d block=%s" % (block.height, block.hash))
