from PIL import Image
import glob, os, numpy as np

differencefaces_folder = 'difference_faces'
eigenfaces_folder = 'eigenfaces'
SIZE_X = 320
SIZE_Y = 243

def compute_sorted_eigenvecs(A):
    U, s, Vt = np.linalg.svd(A, full_matrices = False)
    V = Vt.T
    ind = np.argsort(s)[::-1]
    U = U[:, ind]
    s = s[ind]
    V = V[:, ind]
    return U, s, V.T

def normalize_vec(v):
    v -= min(v)
    v /= max(v)
    v *= 256
    return v

def compute_eigenfaces():
    images = glob.glob(os.path.join(differencefaces_folder, '*.gif'))

    #fill the array
    A = np.zeros((len(images), SIZE_X*SIZE_Y))
    for i, image in enumerate(images):
        im = Image.open(image)
        A[i] = list(im.getdata())
        
    A = A.T
    
    U, s, Vt = np.linalg.svd(A, full_matrices = False)

    return U, s, Vt.T

def reconstruct_im(re, i):
    data = re[:, i]
    im = Image.new('L', (SIZE_X, SIZE_Y))
    im.putdata(data)
    im.save('re%i.gif' % i)

if __name__ == '__main__':
    U, s, V = compute_eigenfaces()
    S = np.diag(s)
    re = np.dot(U, np.dot(S, V.T))
    reconstruct_im(re, 0)
    reconstruct_im(re, 10)
    reconstruct_im(re, 20)
    reconstruct_im(re, 30)
    reconstruct_im(re, 40)
    reconstruct_im(re, 50)
    reconstruct_im(re, 119)
    
