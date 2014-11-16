from PIL import Image
import numpy as np
import glob, os, math


def normalizeImage(img_path,img_name):
	s = Image.open(img_path)
	img_v = np.array(s)
	#hard coded values
	max_pixel = img_v.max()
	min_pixel = img_v.min()

	(width, height) = s.size



	print 'max: %s , min: %s' %(max_pixel,min_pixel)
	
	# um = um%128
	# ustd = ustd%128
	new_max = 255.0
	new_min = 0.0
	img_v = img_v - min_pixel
	# print img_v
	img_v =  img_v * (new_max - new_min)/(max_pixel - min_pixel) +  new_min

	print img_v
	s = Image.fromarray(img_v.astype('uint8'));
	# 		# npixel = npixel%0xFFFFFF
	# for i in xrange(0,height -1):
	# 	for j in xrange(0,width -1):
	# 		# npixel = (s.getpixel((j,i)) - mean)*ustd/std + um
	# 		#linear normalization
	# 		new_max = 255
	# 		new_min = 0
	# 		npixel = (s.getpixel((j,i)) - min_pixel) * (255/(max_pixel - min_pixel)) +  new_min
	# 		# npixel = npixel%0xFFFFFF
	# 		s.putpixel((j,i), npixel)		

	print "saving file"
	s.save('%s.gif'%img_name)

normalizeImage("./test_picture/1_7_.gif","./test_picture/1_7_n")
normalizeImage("./test_picture/1_9_.gif","./test_picture/1_9_n")
normalizeImage("./test_picture/1_10_.gif","./test_picture/1_10_n")

