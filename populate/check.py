from blockchain_parser.blockchain import Blockchain
import os
import csv
import sys
#from blockchain_parser.blockchain  blockch import Blockchain

# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
var = '/home/praful/Bitcoin_data/blocks/blk00001.dat'
blockchain = Blockchain(sys.argv[1])
for block in blockchain.get_unordered_blocks():
    for tx in block.transactions:
        for number, output in enumerate(tx.outputs):
        #for i in tx.inputs:
        #    print("script=%s"%(i.script))
            for index, add in enumerate(output.addresses):


                print("tx=%s outputno=%d type=%s value=%s address=%s block_size=%s " %
                (tx.hash, number, output.type, output.value, add.address, block.size))
