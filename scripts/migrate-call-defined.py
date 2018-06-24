import math
import sys
import urllib.request

api = "http://54.169.180.30/core/run/?"

def main():
	print("Hello World!")
	start =  sys.argv[1]
	end =  sys.argv[2]
	print(start)
	print(end)
	bucket_size = 2000

	bucket_start = int(start)/bucket_size
	bucket_start = int(math.ceil(bucket_start))
	
	bucket_end = int(end)/bucket_size
	buckets_end = int(math.ceil(bucket_end))
	
	print("\n+buckets "+str(bucket_start)+" to "+str(buckets_end))

	for i in range(bucket_start, buckets_end):
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
