import xapian
import json
from os.path import expanduser
from os.path import isfile

def search(querystring):
	db_path = expanduser('~') + '/.clingo_db'

	# Open the database we're going to search and set up the querystring.
	db = xapian.Database(db_path)


	# Set up a QueryParser with a stemmer
	queryparser = xapian.QueryParser()
	queryparser.set_stemmer(xapian.Stem('en'))
	queryparser.set_stemming_strategy(queryparser.STEM_SOME)
	queryparser.add_prefix("description", 'S')
	queryparser.add_prefix('tags', 'XD')
	queryparser.add_prefix('filename', 'XO')
	queryparser.add_prefix('content', 'XS')


	# Parse the query
	query = queryparser.parse_query(querystring)


	# Use an Enquire object on the database to run the query
	enquire = xapian.Enquire(db)
	enquire.set_query(query)

	# And print out something about the matches
	matches = []
	for match in enquire.get_mset(0, 10000):
		fields = json.loads(match.document.get_data())
		matches.append(fields)

	for res in matches:
		print '\n\n\n'
		print '* File Name: ', res['filename']
		print '* File Path: ', res['filepath']

if __name__ == '__main__':
	name = raw_input('Enter file name: ')
	search('content:' + name)