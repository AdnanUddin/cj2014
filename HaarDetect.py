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

	new_max = 255.0
	new_min = 0.0
	img_v = img_v - min_pixel

	img_v =  img_v * (new_max - new_min)/(max_pixel - min_pixel) +  new_min

	s = Image.fromarray(img_v.astype('uint8'));		

	return s


#returns a PIL imgage obj
def get_Image(imageFile):
	filepath,filename = os.path.split(imageFile)
	filtername,exts = os.path.splitext(filename)
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
def more_contrast(image,amount=3):
	cont_obj = ImageEnhance.Contrast(image)
	cont_img = cont_obj.enhance(amount)
	return cont_img

#smooth image
def smooth_Image(image):
	return image.filter(ImageFilter.SMOOTH_MORE)
def blur_Image(image):
	return image.filter(ImageFilter.BLUR)

#image to vector
def img_to_vector(image):
	return np.array(img)

#compare image to sides
def compare_img_to_sides(subImage,SidesBox,SidesBoxOffsets):
	#total contrast sums
	darkSum=0
	lightSum=0
	
	x1=SidesBoxOffsets[0]
	y1=SidesBoxOffsets[1]
	x2=SidesBoxOffsets[2]
	y2=SidesBoxOffsets[3]

	sidesW = SidesBox[0]
	sidesH = SidesBox[1]

	sidesDark = subImage[y1:(y1+sidesH),x1:(x1+sidesW)]
	darkSum = sum(sum(sidesDark))

	sidesLight = subImage[y1:(y1+sidesH),(x1+sidesW):(x1+sidesW*2)]
	lightSum = sum(sum(sidesLight))

	
	sidesDark = subImage[y2:(y2+sidesH),x2:(x2+sidesW)]
	lightSum += sum(sum(sidesDark))

	sidesLight = subImage[y2:(y2+sidesH),(x2+sidesW):(x2+sidesW*2)]
	darkSum += sum(sum(sidesLight))

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

#compare image to the hairline
def compare_img_to_hairline(subImage, HairBox,HairBoxOffsets):
	#total contrast sums
	darkSum=0
	lightSum=0

	x = HairBoxOffsets[0]
	y = HairBoxOffsets[1]
	hairH = HairBox[1]
	hairW = HairBox[0]

	hairDark = subImage[x:(x+hairW),y:(y+hairH)]
	darkSum = sum(sum(hairDark))
	
	hairlight = subImage[x:(x+hairW),(y+hairH):(y+hairH*2)]
	lightSum = sum(sum(hairlight))

	return abs(lightSum - darkSum)

	
def get_best_rect(image):
	x=0	
	cols = 1
	
	sidesBox = (15,30)
	sidesBoxOffsets = (0,116,FaceBox[0]-sidesBox[0]*2,116)
	
	hairBox = (70,20)
	hairBoxOffsets = (50,0)

	EyesBox = (90,30,10)
	EyesBoxOffsets = (30,100)

	imgVector = img_to_vector(image)
	imgDimensions = imgVector.shape
	
	BestScore =0.0
	BestScoreIndex =0
	for offset in range(0,imgDimensions[cols]-FaceBox[0]):	
		subImage = imgVector[:,offset:(offset+FaceBox[x])]
		#score = compare_img_to_eyes(subImage,EyesBox,EyesBoxOffsets)
		score = compare_img_to_sides(subImage,sidesBox,sidesBoxOffsets)
		score += compare_img_to_hairline(subImage,hairBox,hairBoxOffsets)
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

def haar_main(image_file_path):
	img = Image.open(image_file_path)
	face = normalizeImage(img)
	face = smooth_Image(face)
	face = sharpen_Image(face,30)
	face = blur_Image(face)
	return getFace(face)

if(__name__ == '__main__'):
	
	files = glob.glob("training dataset"+"/*.gif")

	for imageFile in files:
		filepath,filename = os.path.split(imageFile)
		filtername,exts = os.path.splitext(filename)
		print "Processing: " + imageFile, filtername
		img = Image.open(imageFile)
		face = normalizeImage(img)
		face = smooth_Image(face)
		face = sharpen_Image(face,30)
		face = blur_Image(face)
		
		face = getFace(img)
		face.save('../cropped/'+filtername+'CROPPED.gif')
