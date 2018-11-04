import numpy as np, matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.ndimage.interpolation import zoom
from scipy.ndimage import median_filter
from sklearn.cluster import KMeans
from skimage import measure
import sys, os

n=100
sobel_x = np.c_[
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
]

sobel_y = np.c_[
    [1,2,1],
    [0,0,0],
    [-1,-2,-1]
]


def swap(fname,destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


def find_all_images():
    cmd = 'p=$PWD;cd /; find -name *.jpg >> $p/pics.txt; cd $p;'
    os.system(cmd)
    pictures = swap('pics.txt', True)
    print str(len(pictures)) + " Pictures Found"
    return pictures


def color_separate(imat):
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(15,5))
    matrices = {}
    for c, ax in zip(range(3),axs):
        tmp_im = np.zeros(imat.shape, dtype="uint8")
        tmp_im[:,:,c] = imat[:,:,c]
        ax.imshow(tmp_im)
        ax.set_axis_off()
        matrices[c] = tmp_im
    plt.show()
    return matrices 


def apply_sigmoid(imat):
    return -np.log(1/((1 + imat)/255)-1)    


def undo_sigmoid(imat):
    return (1+1/(np.exp(-imat) + 1)*255).astype("uint8")


def rotation_matrix_colorspace(theta):
    return np.c_[[1,0,0],
                 [0,np.cos(theta),-np.sin(theta)],
                 [0,np.sin(theta),np.cost(theta)]
                 ]


def median_filter_all_colors(im):
    """
    Applies a median filer to all color channels
    """
    ims = []
    window_size= (0.2,0.2,1)
    im_small = zoom(im,window_size)
    for d in range(3):
        im_conv_d = median_filter(im[:,:,d], size=im.shape)
        ims.append(im_conv_d)

    im_conv = np.stack(ims, axis=2).astype("uint8")    
    return im_conv


def sobel_edges(im):
    ims = []
    im_small = zoom(im, (0.2,0.2,1))
    for d in range(3):
        sx = convolve2d(im_small[:,:,d], sobel_x, mode="same", boundary="symm")
        sy = convolve2d(im_small[:,:,d], sobel_y, mode="same", boundary="symm")
        ims.append(np.sqrt(sx*sx + sy*sy))

    im_conv = np.stack(ims, axis=2).astype("uint8")
    plt.imshow(im_conv)
    plt.show()
    return im_conv


def kmeans_clustering(imat):
    im_small = zoom(imat, (0.2,0.2,1))
    h,w = im_small.shape[:2]
    im_small_long = im_small.reshape((h * w, 3))
    im_small_wide = im_small_long.reshape((h,w,3))

    km = KMeans(n_clusters=3)
    km.fit(im_small_long)

    cc = km.cluster_centers_.astype(np.uint8)
    out = np.asarray([cc[i] for i in km.labels_]).reshape((h,w,3))
    
    plt.imshow(out)
    plt.show()
    seg = np.asarray([(1 if i == 1 else 0)
                  for i in km.labels_]).reshape((h,w))

    contours = measure.find_contours(seg, 0.5, fully_connected="high")

    simplified_contours = [measure.approximate_polygon(c, tolerance=5) for c in contours]

    plt.figure(figsize=(5,10))

    for n, contour in enumerate(simplified_contours):
        plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
    
    plt.ylim(h,0)
    plt.axes().set_aspect('equal')
    plt.show()
    return cc, out, seg


def main():
    # pictures = find_all_images()
    imat = np.array(plt.imread(sys.argv[1]))

    # Separate into R, G and B plots
    colors = color_separate(imat)
    edges = sobel_edges(imat)
    cc, svg, segments = kmeans_clustering(imat)

    
if __name__ == '__main__':
    main()

