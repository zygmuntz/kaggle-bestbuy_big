'http://fastml.com/best-buy-mobile-contest-big-data/'

import sys, csv, re
from collections import defaultdict

def prepare( query ):
	query = re.sub( r'\W', '', query )
	query = query.lower()
	return query

input_file = sys.argv[1]
test_file = sys.argv[2]
benchmark_file = sys.argv[3]
output_file = sys.argv[4]

i = open( input_file )
reader = csv.reader( i )

t = open( test_file )
b = open( benchmark_file )

headers = reader.next()
mapping = defaultdict( lambda: {} )

counter = 0

for line in reader:
	query = prepare( line[3] )
	sku = line[1]
	# print "%s -> %s" % ( query, sku )
	
	try:
		mapping[query][sku] += 1
	except KeyError:
		mapping[query][sku] = 1

			
	counter += 1
	if counter % 100000 == 0:
		print counter

reader = csv.reader( t )
headers = reader.next()

bench_reader = csv.reader( b, delimiter = " " )
headers = bench_reader.next()

o = open( output_file, 'wb' )
writer = csv.writer( o, delimiter = " " )

n = 0
m = 0

for line in reader:
	n += 1
	query = prepare( line[2] )
	popular_skus = bench_reader.next()
	
	if query in mapping:

		m += 1
		skus = []
		
		for sku in sorted( mapping[query], key=mapping[query].get, reverse = True ):
			skus.append( sku )
	
		skus.extend( popular_skus )
		skus = skus[0:5]
		
	else:
		skus = popular_skus
		
	writer.writerow( skus )
	
	# counter
	if n % 10000 == 0:
		print n
		
print "Used mapping in %s / %s (%s)" % ( m, n, 1.0 * m / n )