import urllib.request
from bitcoinrpc.authproxy import AuthServiceProxy

api = "127.0.0.1:8000/core/run/?"

def main():
	access = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%('karan', 'blockwala@123'))
	try:
		end = access.getblockcount()
	except Exception as e:
		print "Problems connecting to bitcoin wallet:"
		end = 550000 #5.5 lakh

	print("Hello World!")
	start = 0

	bucket_size = 20000
	buckets = end/bucket_size

	for i in buckets:
		start = i * bucket_size
		end = (i+1) * bucket_size
		append_str = "start="+str(start)+"&stop="+str(end)
		complete_api = api + append_str
		contents = urllib.request.urlopen(complete_api).read()
		# start=0&stop=10000


if __name__== "__main__":
  main()