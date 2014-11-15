#!usr/bin/python
import Image,glob,os

def convert_DB_To_PNG(picturesDir):
	files = glob.glob(picturesDir+"/*.gif")

	for imageFile in files:
		filepath,filename = os.path.split(imageFile)
		filtername,exts = os.path.splitext(filename)
		print "Processing: " + imageFile, filtername
		im = Image.open(imageFile)
		im.save(picturesDir+'/'+filtername+'.png','PNG')
if(__name__ == '__main__')
	convert_DB_To_PNG("training dataset")
