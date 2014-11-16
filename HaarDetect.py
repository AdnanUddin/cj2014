#!bin/python
import glob, os
from PIL import ImageEnhance, ImageFilter, Image
import numpy as np

FaceBox = (170,243)


def normalizeImage(s):
	img_v = np.array(s)
	max_pixel = img_v.max()
	min_pixel = img_v.min()

	(width, height) = s.size



	print 'max: %s , min: %s' %(max_pixel,min_pixel)
	new_max = 255.0
	new_min = 0.0
	img_v = img_v - min_pixel

	img_v =  img_v * (new_max - new_min)/(max_pixel - min_pixel) +  new_min

	s = Image.fromarray(img_v.astype('uint8'));		

	print "saving file"
	# s.save('%s.gif'%img_name)
	return s


#returns a PIL imgage obj
def get_Image(imageFile):
	filepath,filename = os.path.split(imageFile)
	filtername,exts = os.path.splitext(filename)
	print "Processing: " + imageFile, filtername
	im = Image.open(imageFile)
	return im

#returns a sharpened image objec
def sharpen_Image(image, sharpness=1.6):
	sharpener = ImageEnhance.Sharpness(image)
	sharpened_image = sharpener.enhance(sharpness)
	return sharpened_image

#find edges of face
def find_edge(image):
	edged_img = image.filter(ImageFilter.FIND_EDGES)
	return edged_img

#enhace contrast
def more_contrast(image):
	cont_obj = ImageEnhance.Contrast(image)
	cont_img = cont_obj.enhance(3)
	return cont_img

#image to vector
def img_to_vector(image):
	return np.array(img)

#compare box to image
def compare_img_to_nose(subImage,NoseBox,NoseBoxOffsets):
	#total contrast sums
	darkSum=0
	lightSum=0
	
	x1=NoseBoxOffsets[0]
	y1=NoseBoxOffsets[1]
	x2=NoseBoxOffsets[2]
	y2=NoseBoxOffsets[3]

	noseW = NoseBox[0]
	noseH = NoseBox[1]

	noseDark = subImage[y1:(y1+noseH),x1:(x1+noseW)]
	darkSum = sum(sum(noseDark))

	noseLight = subImage[y1:(y1+noseH),(x1+noseW):(x1+noseW*2)]
	lightSum = sum(sum(noseLight))

	
	noseDark = subImage[y2:(y2+noseH),x2:(x2+noseW)]
	lightSum += sum(sum(noseDark))

	noseLight = subImage[y2:(y2+noseH),(x2+noseW):(x2+noseW*2)]
	darkSum += sum(sum(noseLight))

	return abs(lightSum - darkSum)

def compare_img_to_eyes(subImage,EyesBox,EyesBoxOffsets):
	#total contrast sums
	darkSum=0
	lightSum=0
	
	x=EyesBoxOffsets[0]
	y=EyesBoxOffsets[1]
	darkH = (EyesBox[0]-EyesBox[2])/2
	lightH = EyesBox[2]
	eyesW = EyesBox[0]

	eyesDark1 = subImage[y:(y+darkH),x:(x+eyesW)]
	darkSum = sum(sum(eyesDark1))

	eyesLight = subImage[(y+darkH):(y+darkH+lightH),x:(x+eyesW)]
	lightSum = sum(sum(eyesLight))

	eyesDark2 = subImage[(y+darkH+lightH):(y+darkH*2+lightH),x:(x+eyesW)]
	lightSum = sum(sum(eyesDark2))

	return abs(lightSum - darkSum)

def get_best_rect(image):
	x=0	
	cols = 1
	
	NoseBox = (15,30)
	NoseBoxOffsets = (0,116,FaceBox[0]-NoseBox[0]*2,116)

	EyesBox = (90,30,10)
	EyesBoxOffsets = (30,116)

	imgVector = img_to_vector(image)
	imgDimensions = imgVector.shape
	
	print 'image has size: ' + str(imgDimensions)

	BestScore =0.0
	BestScoreIndex =0
	for offset in range(0,imgDimensions[cols]-FaceBox[0]):	
		subImage = imgVector[:,offset:(offset+FaceBox[x])]
	#	score = compare_img_to_eyes(subImage,EyesBox,EyesBoxOffsets)
		score = compare_img_to_nose(subImage,NoseBox,NoseBoxOffsets)
		if(score>BestScore):
			BestScore = score
			BestScoreOffset = offset
			#print BestScoreOffset

	return BestScoreOffset

#crops an image
def crop_image(image,offset,width,height):
	cropped = image.crop((offset,0,width+offset,height))
	# cropped = image.crop((offset,0,width,height))

	return cropped

#get cropped face
def getFace(image):
	offset = get_best_rect(image)
	cropped = crop_image(image,offset,FaceBox[0],FaceBox[1])
	return cropped

if(__name__ == '__main__'):
	
	img = get_Image("./test_picture/1_7_.gif")
	face = getFace(img)
	face = normalizeImage(face)
	face.save('croppedFace2.png','PNG')
