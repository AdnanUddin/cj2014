from PIL import Image
import glob, os, math

# test image matrix


def normalizeImage(img_path,img_name):
	s = Image.open(img_path)
	#hard coded values
	meanList = []
	stdList = []
	um = 193.99
	ustd = 3.35
	(width, height) = s.size
	# print s.size 
	# print height
	# img_data = list(s.getdata())
	# # compare all pixels in row
	# for j in xrange(0, height -1 ):
	# 	for i in xrange(0, width -1):
	# 		if (img_data[j*width + i] != s.getpixel((i,j)) ):
	# 			print "not equal"
	# 			break;

	# #compare img_data with get pixels
	# for i in xrange(0, width*height - 1)
	max_pixel = 255/2
	min_pixel = max_pixel
	for i in xrange(0,height - 1):
		# mean of ith column
		mean = 0.0;
		# mean1 = numpy.mean(img_data[i:height-1:width]);
		for j in xrange(0,width- 1):
			pixel = s.getpixel((j,i))
			mean += pixel
			if ( j > (width - 80) and j < (width + 80) ):
				if (max_pixel < pixel):
					max_pixel = pixel
				if (min_pixel > pixel):
					min_pixel = pixel
			# print s.getpixel((j,i))
		mean /= width
		um = um + mean/(height)
		# print mean
		# std = 0.0
		# for j in xrange(0,width -1):
		# 	std = math.pow(s.getpixel((j,i)) - mean, 2)
		# 	# print test_str	

		# std = math.sqrt(std/(width-1))
		# ustd = ustd + std/(height)


	print 'max: %s , min: %s' %(max_pixel,min_pixel)
	
	# um = um%128
	# ustd = ustd%128
	for i in xrange(0,height -1):
		for j in xrange(0,width -1):
			# npixel = (s.getpixel((j,i)) - mean)*ustd/std + um
			new_max = 255
			new_min = 0
			npixel = (s.getpixel((j,i)) - min_pixel) * (255/(max_pixel - min_pixel)) +  new_min
			# npixel = npixel%0xFFFFFF
			s.putpixel((j,i), npixel)		

	print "saving file"
	s.save('%s.gif'%img_name)

normalizeImage("./test_picture/1_7_.gif","./test_picture/1_7_n")
normalizeImage("./test_picture/1_9_.gif","./test_picture/1_9_n")
normalizeImage("./test_picture/1_10_.gif","./test_picture/1_10_n")

