import xapian
import hashlib
import json
from os.path import expanduser

# This function generates a unique identifier for each file.
def genId(filePath):
	hash_object = hashlib.md5(filePath.encode())
	return (hash_object.hexdigest())

def index(info):

	db_path = expanduser('~') + '/.clingo_db'

	# Create or open the database we're going to be writing to
	db = xapian.WritableDatabase(db_path, xapian.DB_CREATE_OR_OPEN)


	# Set up a TermGenerator that we'll use in indexing.
	termgenerator = xapian.TermGenerator()
	termgenerator.set_stemmer(xapian.Stem("en"))


	# Fields that'll be indexed
	filename = info['filename']
	identifier = genId(info['filepath'])


	# Create a document and tell the term generator to use this.
	doc = xapian.Document() 
	termgenerator.set_document(doc)


	# Index fields with suitable prefixes so a field search could be done.
	termgenerator.index_text(filename, 1, 'XO')


	# Create a blob data 
	doc.set_data(json.dumps(info))


	# We use identifier to ensure that each object ends up in 
	# database once only no matter how many times we run the
	# indexer.
	doc.add_boolean_term(identifier)
	db.replace_document(identifier, doc)


if __name__ == '__main__':

	info = {
		'filepath': '/home/khirod/ryuk.cpp',
		'filename': 'ryuk.cpp'
	}

	index(info)