import httplib2
from bitcoinrpc.authproxy import AuthServiceProxy
access = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%('karan', 'blockwala@123'))
try:
        blockCount = access.getblockcount()
except Exception as e:
	print(str(e))
else:
        try:
                response, trueBlockCount = httplib2.Http().request("http://blockexplorer.com/q/getblockcount/")
        except Exception as e:
                print("Unable to get true blockcount from blockexplorer:"+str(e))
        else:
                if (int(trueBlockCount) - 5) > blockCount :
                        print ("blockchain not up to date: true block count is: "+str(trueBlockCount)+", while bitcoind is at: "+str(blockCount))
