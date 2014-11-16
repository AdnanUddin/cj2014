#!/usr/bin/python

import sys

if(__name__=='__main__'):
	if(len(sys.argv)==2):
		filename =  sys.argv[1]
		if not '_' in filename:
			print "Wrong format"
		else:
			parts = filename.split('_')
			print parts[0]
	else:
		print "Wrong number of arguments"

