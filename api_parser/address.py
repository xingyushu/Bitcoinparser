#-*- coding: utf-8 -*-
from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


blk = get_blocks('blk00001.dat')
for raw_block in blk:
        block = Block(raw_block)
        for tx in block.transactions:
                for no, output in enumerate(tx.outputs):
                        print(output.addresses[0].address)
                        add1= output.addresses[0].address
                        # check0 = "http://172.16.2.56:9200/btcaddr/addrs/"+add1
                        # check = 'curl'+" "+str(check0)
                        # checkoutput = os.popen(check)
                        # checkresult =checkoutput.read()
                        address_url="https://blockchain.info/rawaddr/"+add1
                        command = 'curl'+" "+str(address_url)
                        # if checkresult == None:
                        output = os.popen(command)
                        result = output.read()
                        command2 = "curl -H 'Content-Type: application/x-ndjson' -XPOST 'http://172.16.2.56:9200/btcaddr/addrs/"+add1+"'"+" -d"+" ' "+result+" ' "
                        os.system(command2)
