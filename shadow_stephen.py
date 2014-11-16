from PIL import Image, ImageFilter
import numpy as np
import glob, os, math, sys

def normalizeImage(s, min):
	img_v = np.array(s)
	max_pixel = img_v.max()
	min_pixel = img_v.min()

	(width, height) = s.size

	new_max = 255.0
	new_min = min
	img_v = img_v - min_pixel

	img_v =  img_v * (new_max - new_min)/(max_pixel - min_pixel) +  new_min

	s = Image.fromarray(img_v.astype('uint8'));		

	return s

def remove_shadow(image_path):
	original = Image.open(image_path)

	normalized = normalizeImage(original, 100)

	original_edges = original.filter(ImageFilter.FIND_EDGES)
	original_edges = normalizeImage(original_edges, 0)
	
	normalized_edges = normalized.filter(ImageFilter.FIND_EDGES)
	normalized_edges = normalizeImage(normalized_edges, 0)

	edge_difference_numpy = np.subtract(original_edges, normalized_edges)

	edge_difference = Image.fromarray(edge_difference_numpy)

	edge_difference.save('./test_picture/1_diff.png')
	original.save('./test_picture/1_orig.png')
	normalized.save('./test_picture/1_norm.png')
	original_edges.save('./test_picture/1_orig_edge.png')
	normalized_edges.save('./test_picture/1_norm_edge.png')

remove_shadow(sys.argv[1])