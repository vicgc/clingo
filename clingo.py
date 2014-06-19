import argparse
import hashlib
import xapian

from xapian_indexer import index
from os.path import abspath
from os.path import expanduser
from os.path import isfile

def getIndexedContent(filename):

	# this path may be filepath or mntpath
	_path = abspath(filename)
	_uid = (hashlib.md5(_path.encode())).hexdigest()

	db_path = expanduser('~') + '/.clingodb'
	db = xapian.Database(db_path)

	print '_abspath: ', _path
	print '_uid: ', _uid

	queryparser = xapian.QueryParser()
	query = queryparser.parse_query(_uid)

	enquire = xapian.Enquire(db)
	enquire.set_query(query)

	print 'Here'

	for match in enquire.get_mset(0, 1):
		print 'Type of: ', type(match.document.get_data())
		return (match.document.get_data())


def checkValidity(name, _type):
	if isfile(name) == False:
		print 'Needed a file.'
		return None

	try:
		if _type == 'tags':
			tags = raw_input("Enter your tags [space separated]: ")
			return tags

		elif _type == 'desc':
			desc = raw_input("Enter a description for this file: ")
			return desc

	except KeyboardInterrupt:
		print 'Exiting Gracefully..'
		return None

	return None


def main():
	parser = argparse.ArgumentParser()

	parser.add_argument("-t", "--addtags", help="add tags to a file.")
	parser.add_argument("-d", "--adddescription", help="add description to a file.")

	args = parser.parse_args()

	if args.addtags:
		tags = checkValidity(args.addtags, 'tags')

		if tags == None:
			return

		else:
			# write indexing code
			_newinfo = getIndexedContent(args.addtags)
			_newinfo['tags'] = tags
			index(_newinfo)

	if args.adddescription:
		desc = checkValidity(args.adddescription, 'desc')

		if desc == None:
			return
			
		else:
			# write indexing code
			_newinfo = getIndexedContent(args.adddescription)
			_newinfo['description'] = desc
			index(_newinfo)

if __name__ == '__main__':
	main()