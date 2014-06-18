import mimetypes
import hashlib

def getContent(path):
	_type = mimetypes.guess_type(path)[0]

	if _type.split('/')[0] == 'text':
		fd = open(path) 
		content = fd.read()
		return ' '.join(content.split())
	
	return None

		

if __name__ == '__main__':
	getContent('/home/khirod/Projects/clingo/myFS.py')

