#!/usr/bin/python

import sys
import numpy
from PIL import Image
false = False
true = True

import look_for_x as core_engine
import HaarDetect as pre_processing

def check_args():
	if(len(sys.argv)==2):
		filename =  sys.argv[1]
		if not '_' in filename:
			print "Wrong format"
			return false
		else:
			return true
	else:
		print "Wrong number of arguments"
		return false

def main():
	if check_args() == false:
		sys.exit(1)
	image_path = sys.argv[1]

	#below should be a numpy object
	pre_processed_PIL_image = Image.open(image_path) # replace with shabbir's code

	print core_engine.look_for_x_by_object('DB', pre_processed_PIL_image)
    
if __name__ == '__main__':
    main()

'''
1.) pipe filename into haarDetect, returns numpy object
2.) pipe numpy object into look_for_x_in.py

'''

