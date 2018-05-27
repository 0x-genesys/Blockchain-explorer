import sys
from blockchain_parser.blockchain import Blockchain
from blockchain_parser.address import Address
import os
# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
file_names_list = []
var = '/home/praful/Bitcoin_data/blocks/'
for filename in os.listdir('/home/praful/Bitcoin_data/blocks/'):
    if(filename.startswith('blk') and filename.endswith('.dat')):
        file_names_list.append(filename)
        print(filename)
myFilePath = '/home/praful/extras/'
for c, i in enumerate(file_names_list):
    blockchain = Blockchain(var + i)
    with open(myFilePath + i + c + '.csv', "wb") as f:

    fieldnames=['transactions','input_no' ,'output_no', 'output_type', 'value']

    writer = csv.DictWriter(f, dialect='excel',fieldnames = fieldnames)#, encoding='utf-8')



    writer.writeheader()
    #blockchain = Blockchain(sys.argv[1])
    for block in blockchain.get_unordered_blocks():
        #print(block)
        for tx in block.transactions:
            #print(tx)
            #for no, output in enumerate(tx.outputs):
            #    print("tx=%s outputno=%d type=%s value=%s size=%d script=%s address=%s" % (tx.hash, no, output.type, output.value, output.size, output.script, output.addresses))
            transaction = []
            input_no = []
            output_no = []

            output_type = []

            value = []



            transaction.append(tx.hash)
            input_no.append(tx.inputs)

            output_no.append(no)

            output_type.append(output.type)

            value.append(output.type)





            record = {'transactions':transaction[0], 'input_no':input_no[0], 'output_no':output_no[0], 'output_type':output_type[0], 'value':value[0]}

            #pickup_list.append(record)

            transaction.remove(transaction[0])

            input_no.remove(input_no[0])

            value.remove(value[0])

            output_no.remove(output_no[0])

            output_type.remove(output_type[0])




            a = c=+1

            writer.writerow(record)


        for input in tx.inputs:
            print("tx=%s script=%s transaction_hash=%s transaction_index=%s"%(tx.hash, input.script, input.transaction_hash, input.transaction_index))

        #address_gen = Address(tx)
        #for add in address_gen.address:
        #    print(add)
'''
blockchain = Blockchain(sys.argv[1])
for block in blockchain.get_ordered_blocks(sys.argv[1] + '/index', end=1000):
    print("height=%d block=%s" % (block.height, block.hash))
'''
