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


def image_playback():
    f = plt.figure()
    os.system('ls remoteImagery/ >> images.txt')
    pictures = swap('images.txt', True)
    print str(len(pictures)) + " Pictures Found "
    reel = []
    for picture in pictures:
        image = plt.imread('remoteImagery/' + picture)
        reel.append([plt.imshow(image)])
    a = animation.ArtistAnimation(f, reel, interval=1000, blit=True, repeat_delay=1000)
    plt.show()


os.system("echo 'Updating Image Library'")
os.system('git pull origin')


image_playback()
