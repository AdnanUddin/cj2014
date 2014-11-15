#computes the difference faces

from PIL import Image
import glob, os

dataset_folder = 'training dataset'
avg_im_path = 'average_face.gif'
differencefaces_folder = 'difference_faces'

def compute_differenceface():
    images = glob.glob(os.path.join(dataset_folder, '*.gif'))
    avg_pixels = list(Image.open(avg_im_path).getdata())

    #compute deviated image from mean
    for image_path in images:
        im = Image.open(image_path)    
        pixels = list(im.getdata())
        new_pixels = [abs(p - pixels[i]) for i, p in enumerate(avg_pixels)]
        
        new_im = Image.new(im.mode, im.size)
        new_im.putdata(new_pixels)
        image_name = os.path.split(image_path)[-1]
        new_im.save(os.path.join(differencefaces_folder, image_name))

if __name__ == '__main__':
    if not os.path.exists(differencefaces_folder):
        os.mkdir(differencefaces_folder)    
    
    compute_differenceface()    
