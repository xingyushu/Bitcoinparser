#coding:utf-8 

from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
import os
# Instantiate the Blockchain by giving the path to the directory
# containing the .blk files created by bitcoind
blk = get_blocks('blk00004.dat')
for raw_block in blk:
        block = Block(raw_block)
        for tx in block.transactions:
                print(tx.hash)
                tx_url="https://blockchain.info/rawtx/"+tx.hash
                command = 'curl'+" "+str(tx_url)
                output = os.popen(command)
                result = output.read()
                #print(result)
                command2 = "curl -H 'Content-Type: application/x-ndjson' -XPOST 'http://172.16.2.56:9200/btctxes/txes/"+tx.hash+"'"+" -d"+" ' "+result+" ' "
                os.system(command2)
