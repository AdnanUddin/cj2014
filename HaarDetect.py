#!bin/python
import Image, glob, os
from PIL import ImageEnhance, ImageFilter
import numpy as np

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
def compare_img_to_noze(imgVec,boxDim,boxOffset,imgDim, boxLength):
	#tuple markers
	dark1=0
	light1=1
	dark2 =2
	x=0
	y=1

	#total contrast sums
	darkSum=0
	lightSum=0
	
	#iterage through image column wise
	for row in range (0,boxDim[dark1]):
		darkSum += imgVec[boxOffset+(row%imgDim[y])*imgDim[x]+(row/imgDim[y])]
	for row in range (boxDim[dark1],boxDim[light1]):
		lightSum += imgVec[boxOffset+(row%imgDim[y])*imgDim[x]+(row/imgDim[y])]

	for row in range (boxDim[light1],boxDim[dark2]):
		darkSum += imgVec[boxOffset+(row%imgDim[y])*imgDim[x]+(row/imgDim[y])]
	return abs(lightSum - darkSum)

def compare_img_to_eyes(imgVec,boxDim,boxOffset,imgDim,boxWidth):
	#tuple markers
	dark1=0
	light1=1
	dark2 =2
	x=0
	y=1

	#total contrast sums
	darkSum=0
	lightSum=0
	
	#iterate though image row
	for col in range(0,boxDim[dark1]):
		darkSum += imgVec[boxOffset+(col%boxWidth)+(imgDim[x]* (col/boxWidth))]

	for col in range(boxDim[dark1],boxDim[light1]):
		darkSum += imgVec[boxOffset+(col%boxWidth)+(imgDim[x]* (col/boxWidth))]

	for col in range(boxDim[light1],boxDim[dark2]):
		darkSum += imgVec[boxOffset+(col%boxWidth)+(imgDim[x]* (col/boxWidth))]

	return abs(lightSum - darkSum)

def get_best_rect(image):
	x = 0
	y = 1
	
	FaceBox = (170,243)
	NoseBox = (30,35)
	NoseBoxOffsets = (385,685,1050)
	EyesBox = (90,10)
	EyesBoxOffsets = (900,1800,2700)

	imgVector = img_to_vector(image)
	imgDimensions = imgVector.shape
	
	print 'image has size: ' + str(imgDimensions)
	print imgVector[44,56]

	BestScore =0.0
	BestScoreIndex =0
	for offset in range(0,imgDimensions[x]-FaceBox[x]):	
		score = compare_img_to_eyes(imgVector,EyesBoxOffsets,offset,imgDimensions,EyesBox[x])
		score += compare_img_to_nose(imgVector,NozeBoxOffsets,offset,imgDimensions,NozeBox[x])
		if(score>BestScore):
			BestScore = score
			BestScoreOffset = offset

	return BestScoreOffset

#crops an image
def crop_image(image,offset):
	x=0
	y=1
	cropped = image.crop(offset,0,FaceBox[x],FaceBox[y])
	return cropped

#get cropped face
def getFace(image):
	offset = get_best_rect(image)
	cropped = crop_image(image,offset)
	return cropped

if(__name__ == '__main__'):
	
	img = get_Image('face2.gif')
	face = getFace(img)
	face.save('croppedFace.png','PNG')
