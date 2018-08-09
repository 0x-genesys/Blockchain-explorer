from bitcoinrpc.authproxy import AuthServiceProxy
import psycopg2
import subprocess

def sync(debug):

	if debug:
		sync_loc = "/Users/karanahuja/Workspace/INTERNAL-projects/bitcoin-block-explorer/scripts/sync.sh"
	else:
		sync_loc = "/data/bitcoin-sql-migrator/scripts/sync.sh"


	#TAKE OUT START FROM PSQL
	start = None
	connection = connect_read_db(debug)
	cursor = connection.cursor()
	print(cursor)
	cursor.execute('SELECT block_height FROM bitcoin_data_app_block_table ORDER BY timestamp DESC limit 1')
	rows = cursor.fetchall()
	for row in rows:
		start = (row[0])
	cursor.close()
	


	#TAKE OUT END FROM BLOCKCHAIN
	access = connect_blockchain_rpc(debug)
	end = None
	try:
		end = access.getblockcount()
	except Exception as e:
		print(e)
		print("Problems connecting to bitcoin wallet:")

	print(start)
	print(end)

	#commandline and shell scripts
	# if not debug:
	# 	subprocess.check_output(['karan-virtualenv-start'])

	print("Stopping Bitcoin Core :   ----->")
	subprocess.check_output(['karan-bitcoin-stop'])
	print("XX Bitcoin Core Stopped XX")
	subprocess.check_call(["sh", sync_loc, str(start), str(end)])
	print("Migration complete :)")
	print("Starting Bitcoin Core :   ----->")
	subprocess.check_output(['karan-bitcoin-start'])

	
	# if not DEBUG:
		# subprocess.check_output(['deactivate'])


def connect_blockchain_rpc(debug):
	if debug:
		print("debug true")
		access = AuthServiceProxy("http://%s:%s@explorer.blockwala.io:8332"%('karan', 'blockwala@123'))
		# access = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%('root', 'root'))
	else:
		access = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%('karan', 'blockwala@123'))
	return access

def connect_read_db(debug):
	try:
		if debug:
			conn = psycopg2.connect(dbname='bitcoin', user='karan', host='explorer.blockwala.io', port='5432', password='blockwala@123')
		else:
			conn = psycopg2.connect(dbname='bitcoin', user='karan', host='localhost', port='5432', password='blockwala@123')
		return conn
	except:
		print("I am unable to connect to the database")
		return None

#NOTE TX and ouput will be fully synced
#If you need to sync selective use migrate_data.py
def run(*args):
    sync(args[0])