import argparse
import hashlib
import xapian
import json

from xapian_indexer import index
from os.path import abspath
from os.path import expanduser
from os.path import isfile
from os.path import exists

def getIndexedContent(filename):

	_path = abspath(filename)	# final absolute path of the filename

	# if ~/.clingoconfig exists then
	_clingoconfigpath = expanduser('~') + '/.clingoconfig'
	if exists(_clingoconfigpath):
		print 'Checking Existence'
		f = open(_clingoconfigpath)
		content = (f.read()).split(' ')

		rootdir = content[0]
		mntdir = content[1]

		pos = (abspath(filename)).find(mntdir)

		if pos != -1:
			_path = rootdir + '/' + (abspath(filename))[len(mntdir):]


	# We have the correct _path found here.

	# Get the hashed identifier
	_uid = (hashlib.md5(_path.encode())).hexdigest()

	db_path = expanduser('~') + '/.clingodb'
	db = xapian.Database(db_path)

	queryparser = xapian.QueryParser()
	query = queryparser.parse_query(_uid)

	enquire = xapian.Enquire(db)
	enquire.set_query(query)

	for match in enquire.get_mset(0, 1):
		return (json.loads((match.document.get_data())))

	return None


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

			if _newinfo == None:
				print 'Have you indexed this file inside clingo?'
				return

			_newinfo['tags'] = tags
			index(_newinfo)

	if args.adddescription:
		desc = checkValidity(args.adddescription, 'desc')

		if desc == None:
			return
			
		else:
			# write indexing code
			_newinfo = getIndexedContent(args.adddescription)
			
			if _newinfo == None:
				print 'Have you indexed this file inside clingo?'
				return

			_newinfo['description'] = desc
			index(_newinfo)

if __name__ == '__main__':
	main()