#-*- coding: utf-8 -*-
import os
from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
import sys
reload(sys)
sys.setdefaultencoding('utf8')

blk = get_blocks('blk00000.dat')
for raw_block in blk:
        block = Block(raw_block)
	block_url="https://blockchain.info/rawblock/"+block.hash
	command = 'curl'+" "+str(block_url)
	output = os.popen(command)
	result = output.read()
	    #print(result)
	command2 = "curl -H 'Content-Type: application/x-ndjson' -XPOST 'http://server:9200/btcblocks/blocks/"+block.hash+"'"+" -d"+" ' "+result+" ' "
	os.system(command2)

