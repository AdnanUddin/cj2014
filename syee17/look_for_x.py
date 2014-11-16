import numpy as np
import glob, os
from PIL import Image
import sys, json, argparse

execfile("percentage_error.py")

SIZE_X = 320
SIZE_Y = 243
average_relative_face_image_path = "average.gif"
eigen_faces_images_by_pixels_relative_path = "U"
eigenface_coefficeints_database_relative_path = "C"
eigenface_to_person_database_relative_path = "I.json"

def _look_for_x_core(db, difference_face):
    average_face_image_path = db + "/" + average_relative_face_image_path
    eigen_faces_images_by_pixels_path = db + "/" + eigen_faces_images_by_pixels_relative_path
    eigenface_to_person_json_path = db + "/" + eigenface_to_person_database_relative_path
    eigenface_coefficients_database_path = db + "/" + eigenface_coefficeints_database_relative_path

    difference_face_vector = np.reshape(difference_face, SIZE_X * SIZE_Y) #turn that difference face into a vector

    U = np.load(eigen_faces_images_by_pixels_path) #load the gigantic people and their eigenface constructions matrix

    C = np.load(eigenface_coefficients_database_path) #load the coefficients that we will need

    input_coefficients = np.dot(U.T, difference_face_vector)

    coefficients_error_list = list()

    lowest_error = -1
    lowest_error_index = None

##    for i, coefficient_vector in enumerate(C): #for each image in our database, we compare their weightings to our weighting. and return the index of the person with lowest error
##        error = dist(coefficient_vector, input_coefficients)
##        print error
##        if(lowest_error < error):
##            lowest_error_index = i
##            lowest_error = error
##        coefficients_error_list.append(error)
    
    dists = [dist(c, input_coefficients) for c in C]
    min_dist = min(dists)
    min_index = dists.index(min_dist)
 
    eigenface_to_person_list = json.loads(open(eigenface_to_person_json_path).read()) #load a json file that maps the image number to a person

    print('DIST: %i' % min_dist)
    return eigenface_to_person_list[min_index] #return the person

def look_for_x_by_path(db, image_path):
    average_face_image_path = db + "/" + average_relative_face_image_path
    eigen_faces_images_by_pixels_path = db + "/" + eigen_faces_images_by_pixels_relative_path
    eigenface_to_person_json_path = db + "/" + eigenface_to_person_database_relative_path
    eigenface_coefficients_database_path = db + "/" + eigenface_coefficeints_database_relative_path

    avg_pixels = list(Image.open(average_face_image_path).getdata()) #fetch the average image
    difference_face = create_difference_face_by_path(image_path, avg_pixels) #create a difference face image

    return _look_for_x_core(db, difference_face)

def look_for_x_by_object(db, num_py_image):
    average_face_image_path = db + "/" + average_relative_face_image_path
    eigen_faces_images_by_pixels_path = db + "/" + eigen_faces_images_by_pixels_relative_path
    eigenface_to_person_json_path = db + "/" + eigenface_to_person_database_relative_path
    eigenface_coefficients_database_path = db + "/" + eigenface_coefficeints_database_relative_path

    avg_pixels = list(Image.open(average_face_image_path).getdata()) #fetch the average image
    difference_face = create_difference_face_by_object(num_py_image, avg_pixels) #create a difference face image

    return _look_for_x_core(db, difference_face)

def dump_to_picture(image, name):
    im = Image.new('L', (SIZE_X, SIZE_Y))
    im.putdata(image)
    im.save(name)

def my_error(vector_a, vector_b):
    value = (np.subtract(vector_a, vector_b))**2
    return value    

def dist(va, vb):
    return sum((va - vb)**2)
        

def compute_error(vector_a, vector_b):
    return (vector_a - vector_b)**2
    #return compute_percentage_error(vector_a, vector_b)

def create_difference_face_by_path(image_path, avg_pixels):
    return create_difference_face_by_object(Image.open(image_path), avg_pixels)

def create_difference_face_by_object(numpy_image, avg_pixels):
    pixels = list(numpy_image)
    new_pixels = [pixels[i] - p for i, p in enumerate(avg_pixels)]
    return new_pixels

def main():
    ### PARSING COMMAND LINE
    parser = argparse.ArgumentParser(description = 'Create new face recongition database')
    parser.add_argument('db', type=str, nargs='?', default='DB', help='Path to database folder')    
    parser.add_argument('image_path', type=str, nargs='?', default=None, help='path to image we wnat to check')

    args = parser.parse_args()
    db, image_path = args.db, args.image_path

    if not os.path.exists(db):
        print "Database not found"
        return False

    print ("Utilizing database: " + db)

    #print look_for_x(db, image_path)

if __name__ == '__main__':
    main()
