#computes the average face and saves it as "average_face.gif"
#put it in parent folder of "training dataset"

from PIL import Image
import glob, os

def compute_average_face(dataset_folder = 'training dataset'):
    images = glob.glob(os.path.join(dataset_folder, '*.gif'))
    
    SIZE_X = 320
    SIZE_Y = 243
    num_images = len(images)
    sum_pixels = [0]*(SIZE_X*SIZE_Y)

    #sums all the pixels from the images
    for image_path in images:
        im = Image.open(image_path)    
        pixels = list(im.getdata())
        for i, p in enumerate(pixels):
            sum_pixels[i] += p

    avg_pixels = [p/num_images for p in sum_pixels]

    #create image with average face
    avg_im = Image.new('L', (SIZE_X, SIZE_Y))
    avg_im.putdata(avg_pixels)
    
    avg_im.save('average_face.gif')

if __name__ == '__main__':
    compute_average_face()
