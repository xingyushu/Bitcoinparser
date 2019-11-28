#coding:utf-8
from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
from blockchain_parser.block_header import BlockHeader
import time
import os
from blockchain.blockexplorer import get_address,get_block
import json
import blkreader, time
from elasticsearch import Elasticsearch
es = Elasticsearch(hosts="server", port=9200, timeout=200)


# path_list = os.listdir("./")
# filelist = []
# for filename in path_list:
#     if os.path.splitext(filename)[1]==".dat":
#         filelist.append(filename)


# for i in filelist:
#     print(str(i))
    # blk = get_blocks(i)
blk = get_blocks('./../blk00000.dat')
    # blk = get_blocks(str(i))
for raw_block in blk:
        b = Block(raw_block)
        # print(type(b))
        bheader = BlockHeader(raw_block)
        # print(block.hash)
        # b2 = get_block(b.hash)

        a= {
            "hash": b.hash,
            "basic": {
                "prev_block": bheader.previous_block_hash,
                "mrkl_root": bheader.merkle_root,
                # "height": b2.height,
                "time": str(bheader.timestamp),
                "n_tx": b.n_transactions,
                "main_chain": True,
                # "fee": b2.fee,
                "nonce": bheader.nonce,
                "bits": bheader.bits,
                "size": b.size,
                # "received_time": b2.received_time,
                # "relayed_by": b2.relayed_by,
                "ver": bheader.version,
                "difficulty":bheader.difficulty
            }

        }
        blk0001=blkreader.blkfile('./../blk00000.dat')
        # blk0001=blkreader.blkfile(i)
        genesisblock=blk0001.getblock()
        txes = []
        for tx in genesisblock.tx:
             tx1={}
             tx1['tx'] = genesisblock.tx.index(tx)
             tx1['version'] =tx.version
             tx1['size'] = tx.size
             tx1['hash'] = tx.hash
             tx1['ntx'] = tx.numinputs
             tx1["inputs"]=[]
             tx1["outputs"]=[]

             for txin in tx.inputs:
                  txin1={
                     "input":tx.inputs.index(txin),
                     "previous output":txin.prevouthash,
                     "n": txin.prevoutn,
                     "sequence":txin.sequence,
                     "number of outputs":tx.numoutputs
                  }
                  if txin.prevouthash=='0'*64: txin1["coinbase"]=txin.coinbase.__repr__()
                  else: txin1['scriptSig:']=txin.script.encode('hex')
                  tx1["inputs"].append(txin1)

             for txout in tx.outputs:
                  txout1={
                     "output":tx.outputs.index(txout),
                     "value":txout.value,
                     "script": txout.script.encode('hex'),
                     "locktime":tx.locktime

                  }
                  tx1["outputs"].append(txout1)
             txes.append(tx1)


        
        # print(txes)
        a["tx"] = txes
        # print(a)
        msg = json.dumps(a)
        # print(msg)
        # es.indices.create(index='test-index', ignore=400)
        back =es.index(index="btc",doc_type="blocks",id=b.hash,body=msg)
        print(back)
        # create a index in es 
        # insert the data to es  

        command2 = "curl -H 'Content-Type: application/x-ndjson' -XPOST 'http://server:9200/btc/blocks/"+b.hash+"'"+" -d "+"'"+msg+"'"
        # print(command2)
        os.system(str(command2))
        # print("\n")


















