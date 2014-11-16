import argparse, glob, os, json, re, numpy as np
import HaarDetect as pre_processing
from PIL import Image

#TODO!!! Round 2 pics will be what size?
SIZE_X = 170
SIZE_Y = 243
SIZE = (SIZE_X, SIZE_Y)

def save_pic(data, path):
    avg_im = Image.new('L', SIZE)
    avg_im.putdata(data)
    avg_im.save(path)

def save_map(images, db):
    filenames = [os.path.split(im)[-1] for im in images]
    pat = '^(\d*)_\d*_\.gif$'

    indices = [re.findall(pat, fname)[0] for fname in filenames]
    with open(os.path.join(db, 'I.json'), 'w') as f:
        json.dump(indices, f)

def reconstruct_im(i, U, s, V):
    S = np.diag(s)
    recon = np.dot(U, np.dot(S, V.T))

    data = recon[:, i]
    return data

def compute_eigenfaces(pics, db):
    images = glob.glob(os.path.join(pics, '*.gif'))
    N = len(images)

    #save the map from index to names
    save_map(images, db)

    #fill the array of images
    A = np.zeros((N, SIZE_X*SIZE_Y))
    for i, image in enumerate(images):
        im = Image.open(image) #do not apply preprocessing
        im = pre_processing.haar_main(image) #apply preprocessing
        A[i] = list(im.getdata())

    #compute and store mean picture
    m = A.mean(0)
    save_pic(m, os.path.join(db, 'average.gif'))

    #get the difference pictures
    for i in range(N):
        A[i, :] = A[i, :] - m
    
    L = np.dot(A, A.T)
    w, v = np.linalg.eig(L)
    v = np.real(v) #discard the imaginary numbers

    U = np.dot(A.T, v)

    #normalize
    for i in range(N):
        U[:, i] /= np.linalg.norm(U[:, i])

    #get coefficients
    C = np.zeros((N, N))
    for i in range(N):
        C[i] = np.dot(U.T, A[i]).T

    return U, C

def save_vecs(U, C, db):
    U.dump(os.path.join(db, 'U'))
    C.dump(os.path.join(db, 'C'))
    
def main():
    parser = argparse.ArgumentParser(description = 'Create new face recongition database')
    parser.add_argument('pics', type=str, nargs='?', default='training dataset/', help='Path to folder with training pics')    
    parser.add_argument('db', type=str, nargs='?', default='DB/', help='Output folder for database. Will be created if doesn\'t exist')

    args = parser.parse_args()
    pics, db = args.pics, args.db

    if not os.path.exists(db):
        os.makedirs(db)

    U, C = compute_eigenfaces(pics, db)

    save_vecs(U, C, db)
    
if __name__ == '__main__':
    main()
