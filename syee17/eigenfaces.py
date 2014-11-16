from scipy import misc
from scipy import linalg as scipy_linalg
import numpy as np
import glob, os
from PIL import Image

image_format = "gif"

def asdf(image_directory_input = '../difference_faces'):
	total_array = list();
	image_directory_input = glob.glob(os.path.join(image_directory_input, '*.' + image_format))
	counter = 0;

	image_x_length = -1;
	image_y_length = -1;
	
	for image_path in image_directory_input:
		counter = counter + 1
		#for image in image directory of dif - average:
		image = misc.imread(image_path)
		print "loading the image <<" + image_path + ">> into memory which is of size " + str(image.shape);
		vector = np.reshape(image, image.shape[0] * image.shape[1])
		image_x_length = image.shape[0]
		image_y_length = image.shape[1]
		total_array.append(vector)
		#end loop

	print "We've itterated over: " + str(counter) + " images"

	#total_array is a #pixels x #images
	#total_array_transpose is #images, #pixels
	total_array = np.asarray(total_array)
	total_array_transpose = total_array.T
	print total_array.shape
	print total_array_transpose.shape

	small_matrix = np.dot(total_array, total_array_transpose)

	eigen_values, eigen_vectors = scipy_linalg.eig(small_matrix)
	print "EIGEN VALUES: " + str(len(eigen_values)) + "\n" 
	print eigen_values
	print "EIGEN VECTORS: " + str(eigen_vectors.shape) + "\n";

	eigen_vector_counter = 0
	for eigen_vector in eigen_vectors:
		eigen_vector_counter = eigen_vector_counter + 1
		#eigen_vector = np.array(eigen_vector)[np.newaxis].T
		eigen_vector = np.reshape(eigen_vector, (eigen_vector.size, 1))
		print "Eigen vector: " + str(eigen_vector_counter) + " of length: " + str(eigen_vector.shape)
		#sprint eigen_vector #shoudl be 1 x 120
		print "Attempting to perform the operation: eigen_vector * total_array[eigen_vector_counter - 1]"
		print "eigen_image_vector is of size: " + str(len(eigen_vector))
		vector = np.array(total_array[eigen_vector_counter - 1])[np.newaxis]
		vector_transpose = vector.T
		print "total_array[eigen_vector_counter -1] is of size: " + str(vector.shape)
		print "total_array[eigen_vector_counter -1] tranpsosed is of size: " + str(vector_transpose.shape)
		eigen_image_vector = np.dot(eigen_vector, vector)
		print "THE RECONSTUCTION IS: " + str(eigen_image_vector.shape)
		eigen_image_vector_sum = np.sum(eigen_image_vector, axis=0)
		print "The summation Is: " + str(eigen_image_vector_sum.shape)
		print "Attempting to turn the matrix back into the original " + str(image_x_length) + " by " + str(image_y_length)
		eigen_image_picture = np.reshape(eigen_image_vector_sum, (image_x_length, image_y_length))
		image = Image.new('L', (image_x_length, image_y_length))
		image.putdata(eigen_image_picture)
		image.save(str(eigen_vector_counter) + '.gif');

	#for eigen_vectors as eigen_vector
		#eigenvector is #images x 1
	#composition = np.dot(eigen_vector, total_array_transpose);

if __name__ == '__main__':
    asdf()