import matplotlib.pyplot as plt, matplotlib.animation as animation
import os, numpy as np
import scipy.ndimage as ndi


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


os.system('ls remoteImagery/ >> images.txt')
pictures = swap('images.txt',True)
print str(len(pictures)) + " Pictures Found "
image = plt.imread('remoteImagery/'+pictures.pop())
plt.imshow(image)
plt.show()