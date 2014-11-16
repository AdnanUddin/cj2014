import argparse, glob, os, json, re, numpy as np
from PIL import Image

#TODO!!! Round 2 pics will be what size?
SIZE_X = 320
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

    data = re[:, i]
    return data

def compute_eigenfaces(pics, db):
    images = glob.glob(os.path.join(pics, '*.gif'))

    #save the map from index to namnes
    save_map(images, db)

    #fill the array of images
    A = np.zeros((len(images), SIZE_X*SIZE_Y))
    for i, image in enumerate(images):
        im = Image.open(image)
        A[i] = list(im.getdata())

    #compute and store mean picture
    m = A.mean(0)
    save_pic(m, os.path.join(db, 'average.gif'))
    
    #get the difference pictures
    for i in range(A.shape[0]):
        A[i, :] = A[i, :] - m

    U, s, Vt = np.linalg.svd(A.T, full_matrices = False)
    V = Vt.T

    #sort eigenfaces by order of importance
    #ind = np.argsort(s)[::-1]
    #U = U[:, ind]
    #s = s[ind]
    #V = V[:, ind]

    return U, s, V

def save_vecs(vecs, db):
    U, s, V = vecs
    U.dump(os.path.join(db, 'U'))
    V.dump(os.path.join(db, 'V'))
    s.dump(os.path.join(db, 's'))

def main():
    ### PARSING COMMAND LINE
    parser = argparse.ArgumentParser(description = 'Create new face recongition database')
    parser.add_argument('pics', type=str, nargs='?', default='training dataset/', help='Path to folder with training pics')    
    parser.add_argument('db', type=str, nargs='?', default='DB/', help='Output folder for database. Will be created if doesn\'t exist')

    args = parser.parse_args()
    pics, db = args.pics, args.db

    if not os.path.exists(db):
        os.makedirs(db)

    vecs = compute_eigenfaces(pics, db)

    save_vecs(vecs, db)
    
if __name__ == '__main__':
    main()
