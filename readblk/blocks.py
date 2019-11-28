#coding:utf-8
from blockchain_parser.blockchain import Blockchain,get_files,get_blocks
from blockchain_parser.block import Block
from blockchain_parser.block_header import BlockHeader
import time
import os
from blockchain.blockexplorer import get_address,get_block
import json
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
path_list = os.listdir("./")
filelist = []
for filename in path_list:
    if os.path.splitext(filename)[1]==".dat":
        filelist.append(filename)
# print(filelist)

# for i in filelist:
#     print(i)
#     blk = get_blocks(i)


blk = get_blocks('./../blk00000.dat')
for raw_block in blk:
    b = Block(raw_block)
    bheader = BlockHeader(raw_block)
    # print(block.hash)
    b2 = get_block(b.hash)

    a= {
        "hash": b.hash,
        "basic": {
            "prev_block": bheader.previous_block_hash,
            "mrkl_root": bheader.merkle_root,
            "height": b2.height,
            "time": str(bheader.timestamp),
            "n_tx": b.n_transactions,
            "main_chain": True,
            "fee": b2.fee,
            "nonce": bheader.nonce,
            "bits": bheader.bits,
            "size": b.size,
            "received_time": b2.received_time,
            "relayed_by": b2.relayed_by,
            "ver": bheader.version,
            "difficulty":bheader.difficulty
            # "tx":b2.transactions
        }

    }
    txes = []
    for tx in b.transactions:
        # print(tx.hash)
        tx1 = {}
        d = tx.__dict__
        for k in d:
            tx1[k]=d[k]

        tx1["inputs"]=[]
        tx1["outputs"]=[]

        for i in d["inputs"]:
            id= i.__dict__
            n ={}
            for k in id:
                n[k] = id[k]
            tx1["inputs"].append(n)

        for i in d["outputs"]:
            id= i.__dict__
            n ={}
            for k in id:
                n[k] = id[k]
            tx1["outputs"].append(n)
        txes.append(tx)

    
    print(txes)
    a["tx"] = str(txes)
    print(a)


















