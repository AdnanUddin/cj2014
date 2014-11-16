import numpy as np
import glob, os
from PIL import Image
import sys, json, argparse

execfile("percentage_error.py")

SIZE_X = 320
SIZE_Y = 243
average_relative_face_image_path = "average.gif"
eigen_faces_images_by_pixels_relative_path = "U"
eigenface_database_relative_path = "V"
eigenface_to_person_database_relative_path = "I.json"


def look_for_x(db, image_path):
	average_face_image_path = db + "/" + average_relative_face_image_path
	eigen_faces_images_by_pixels_path = db + "/" + eigen_faces_images_by_pixels_relative_path
	eigenface_database_path = db + "/" + eigenface_database_relative_path
	eigenface_to_person_json_path = db + "/" + eigenface_to_person_database_relative_path

	print "average_face_image_path: " + average_face_image_path
	print "eigen_faces_images_by_pixels_path: " + eigen_faces_images_by_pixels_path
	print "eigenface_database_path: " + eigenface_database_path
	print "eigenface_to_person_json_path: " + eigenface_to_person_json_path

	avg_pixels = list(Image.open(average_face_image_path).getdata()) #fetch the average image
	difference_face = create_difference_face(image_path, avg_pixels) #create a difference face image

	dump_to_picture(difference_face, "difference_face.gif")	

	difference_face_vector = np.reshape(difference_face, SIZE_X * SIZE_Y) #turn that difference face into a vector

	eigenfaces_images_by_pixels_list = np.load(eigen_faces_images_by_pixels_path) #load the gigantic people and their eigenface constructions matrix
	#eigenfaces_images_by_pixels_numpy_array_obj = np.asarray(eigenfaces_images_by_pixels_list) #turn the above into a numpy object
	print eigenfaces_images_by_pixels_list.shape
	print difference_face_vector.shape
	
	input_eigenface_vector = np.dot(eigenfaces_images_by_pixels_list.T, difference_face_vector) #multiply the vector by the eigenface construction matrix to get its weightings

	s = np.diag(np.load(db+'/'+'s'))
	s = np.load(db + "/" + 's')

	#input_eigenface_vector = np.dot(input_eigenface_vector, s)

	eigenface_database_list = np.load(eigenface_database_path) #load the weightings database (each person's weightings)

	eigenface_results = list()

	lowest_error = -1
	lowest_error_index = None

	itter_counter = 0;
	for eigenface_in_database in eigenface_database_list: #for each image in our database, we compare their weightings to our weighting. and return the index of the person with lowest error
		print input_eigenface_vector.shape
		print s.shape
		error = compute_error(input_eigenface_vector, np.dot(eigenface_in_database , s))
		eigenface_results.append(error)
		if(lowest_error < error):
			lowest_error_index = itter_counter
			lowest_error = error
		itter_counter = itter_counter + 1

	print "The lowest_error occurs at index: " + str(lowest_error_index) + " with value: " + str(lowest_error)
	print ("INPUT EIGEN VECTOR")
	print input_eigenface_vector
	print("\n\n\n\nTHE CLOSEST MATCH")
	print eigenface_database_list[lowest_error_index]
 
	eigenface_to_person_list = json.loads(open(eigenface_to_person_json_path).read()) #load a json file that maps the image number to a person
	return eigenface_to_person_list[lowest_error_index] #return the person

def dump_to_picture(image, name):
	im = Image.new('L', (SIZE_X, SIZE_Y))
	im.putdata(image)
	im.save(name)

def compute_error(vector_a, vector_b):
	return compute_percentage_error(vector_a, vector_b)

def create_difference_face(image_path, avg_pixels):
    im = Image.open(image_path)    
    pixels = list(im.getdata())
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

    print look_for_x(db, image_path)

if __name__ == '__main__':
    main()
