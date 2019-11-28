import sys
import copy
import time
from decimal import Decimal
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from elasticsearch import Elasticsearch
import elasticsearch.helpers


def txs_to_es(rpc_connection, es, txs, block):
	tx_index = 'btc_transaction'
	blk_index = 'btc_block'
	doc_type = 'raw'
	request_timeout = 60

	for tx in txs:
		fee = Decimal(0)
		total_out = Decimal(0)
		total_in = Decimal(0)
		if 'coinbase' in tx['vin'][0]:
			tx['iscoinbase'] = True
			tx['vin'][0]['value'] = 50 / float(block['height']/210000 + 1)
			total_out = tx['vout'][0]['value']
		else:
			tx['iscoinbase'] = False
			for item in tx['vin']:
				txid = item['txid']
				vout = item['vout']
				try:
					the_tx = es.get(index=index, doc_type=doc_type, id=txid)
					the_tx = the_tx['_source']
				except:
					the_tx = rpc_connection.getrawtransaction(txid)
					the_tx = rpc_connection.decoderawtransaction(the_tx)
				for out in the_tx['vout']:
					if out['n'] == vout:
						item['value'] = out['value']
						item['addresses'] = out['scriptPubKey']['addresses']
						total_in += Decimal(str(item['value']))
			for item in tx['vout']:
				total_out += item['value']
			fee = total_in - total_out
		tx['fee'] = fee
		tx['volume'] = total_out 
			
		del tx['hex']
		del tx['txid']

		tx['blockheight'] = block['height']
		tx['blockhash'] = block['hash']

	actions = [
		{
			"_op_type": "index",
			"_index": tx_index,
			"_type": doc_type,
			"_id": tx['hash'],
			"_source": tx
		}
		for tx in txs	
	]

	del block['tx']
	del block['confirmations']
	del block['nextblockhash']
	del block['versionHex']

	block_action = {
		"_op_type": "index",
		"_index": blk_index,
		"_type": doc_type,
		"_id": block['hash'],
		"_source": block
	}

	actions.append(block_action)
	try:
		elasticsearch.helpers.bulk(es, actions, request_timeout=request_timeout)
		return 1
	except Exception, e:
		print 'txs_to_es', e
		return -1


def main(height, best):
	rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (rpc_user, rpc_password, rpc_ip, rpc_port))
	es = Elasticsearch("%s:%d" % (es_ip, es_port))

	while height < best:
		print 'height: %d' % height
		try:
			block_hash = rpc_connection.getblockhash(height)
			block = rpc_connection.getblock(block_hash, 2)
		except Exception as e:
			print e
			time.sleep(3)
			rpc_connection = AuthServiceProxy('http://%s:%s@%s:%d' % (rpc_user, rpc_password, rpc_ip, rpc_port))
		else:
			txs = block['tx']
			txs_result = txs_to_es(rpc_connection, es, txs, block)
			if txs_result == 1:
				height += 1


if __name__ == '__main__':
	rpc_user = 'bitcoin'
	rpc_password = '123456'
	rpc_ip = '127.0.0.1'
	rpc_port = 8332
	es_ip = "server"
	es_port = 9200

	height = int(sys.argv[1])
	best = int(sys.argv[2])

	main(height, best)