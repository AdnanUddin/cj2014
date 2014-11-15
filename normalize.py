from PIL import Image
import glob, os, math

# test image matrix
s = Image.open("./training dataset/9_9_.gif")
um = 193.99
ustd = 3.35
(width, height) = s.size
# print s.size 
# print height
img_data = list(s.getdata())
# compare all pixels in row
for j in xrange(0, height -1 ):
	for i in xrange(0, width -1):
		if (img_data[j*width + i] != s.getpixel((i,j)) ):
			print "not equal"
			break;

# #compare img_data with get pixels
# for i in xrange(0, width*height - 1)
mean = []

for i in xrange(0,height - 1):
	# mean of ith column
	mean = 100.0;
	# mean1 = numpy.mean(img_data[i:height-1:width]);
	for j in xrange(0,width- 1):
		mean += s.getpixel((j,i))
	mean /= width 
	# print mean
	# get std
	std = 0.0
	for j in xrange(0,width -1):
		std = math.pow(s.getpixel((j,i)) - mean, 2)
		test_str = '%s , %s' %(j,i)
		# print test_str	

	std = math.sqrt(std/(width-1))
	# print std
	for j in xrange(0,width -1):
		npixel = (s.getpixel((j,i)) - mean)*ustd/std + um
		
		s.putpixel((j,i), npixel)		


s.save("normalized.gif")
	#standard deviation

	# print mean


	#do work

