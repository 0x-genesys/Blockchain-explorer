import math
import sys
import urllib.request
from bitcoinrpc.authproxy import AuthServiceProxy

api = "http://127.0.0.1:8000/core/run/?"

def main():
	print("Hello World!")
	start =  sys.argv[0]
	end =  sys.argv[1]

	bucket_size = 20000
	buckets = int(end)/bucket_size
	buckets = math.ceil(buckets)
	print("\n+buckets "+str(buckets))

	for i in range(buckets):
		print("\n\n\n ..... "+str(i))
		start = i * bucket_size
		end = (i+1) * bucket_size
		print("\nstart ... "+str(start))
		print("\nend ... "+str(end))
		append_str = "start="+str(start)+"&stop="+str(end)
		complete_api = api + append_str
		print("\ncomplete api ... "+str(complete_api))
		contents = urllib.request.urlopen(complete_api).read()
		print(contents)
		# start=0&stop=10000


if __name__== "__main__":
  main()
