#!/usr/bin/python

'''
serve-blockheaders.py

Connects to bitcoind using credentials specified in credentials.json
(of the form {"user":"someusername","passwd":"somepassword"} )
and will pull block headers without caching them.
'''

from flask import Flask
app = Flask(__name__)

logfilename = 'serve-blockheaders.log'

import logging
log_handler = logging.FileHandler(logfilename)
log_handler.setLevel(logging.WARNING)
app.logger.addHandler(log_handler)

import json
credentialFile = 'credentials.json'
with open(credentialFile, 'r') as f:
        cred = json.load(f)

from bitcoinrpc.authproxy import AuthServiceProxy
bitcoind = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (cred['user'],cred['passwd']))
print bitcoind.getinfo()

@app.route('/<path:index>')
def lookupHeaders(index):
        if len(index) < 16:
                # presume block height
                blockhash = bitcoind.getblockhash(int(index))
                index = blockhash
        hexblock = bitcoind.getblock(index,False)
        block = hexblock.decode('hex')
        blockheader = block[:80]
        return blockheader.encode('hex')
		
if __name__ == "__main__":
        app.run()
