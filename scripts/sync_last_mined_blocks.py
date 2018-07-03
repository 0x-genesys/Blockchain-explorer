from bitcoinrpc.authproxy import AuthServiceProxy
import psycopg2
import subprocess



DEBUG = True

if DEBUG:
	sync_loc = "/Users/karanahuja/Workspace/INTERNAL-projects/bitcoin-block-explorer/scripts/sync.sh"
else:
	sync_loc = "/Users/karanahuja/Workspace/INTERNAL-projects/bitcoin-block-explorer/scripts/sync.sh"



def sync():
	start = 0
	end = 0

	#TAKE OUT START FROM PSQL
	connection = connect()
	cursor = connection.cursor()
	print(cursor)
	cursor.execute('SELECT * FROM bitcoin_data_app_block_table ORDER BY block_height DESC limit 1')
	rows = cursor.fetchall()
	for row in rows:
		start = (row[0])

	cursor.close()
	
	#TAKE OUT END FROM BLOCKCHAIN
	access = connect_blockchain_rpc()
	end = None
	try:
		end = access.getblockcount()
	except Exception as e:
		print(e)
		print("Problems connecting to bitcoin wallet:")

	print(start)
	print(end)

	#commandline and shell scripts
	if not DEBUG:
		subprocess.check_output(['karan-virtualenv-start'])

	subprocess.check_output(['ls'])

	subprocess.check_call(["sh", sync_loc, str(start), str(end)])

	if not DEBUG:
		subprocess.check_output(['deactivate'])


def connect_blockchain_rpc():
	if DEBUG:
		access = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%('root', 'root'))
	else:
		access = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%('karan', 'blockwala@123'))
	return access

def connect():
	try:
		conn = psycopg2.connect(dbname='bitcoin', user='karan', host='localhost', port='5432', password='blockwala@123')
		return conn
	except:
		print "I am unable to connect to the database"
		return None

if  __name__ == "__main__":
	sync()