import matplotlib.pyplot as plt, matplotlib.animation as animation
import os, numpy as np
import scipy.ndimage as ndi

f0 = [[0,0,1,0,0],
      [0,1,1,1,0],
      [1,1,1,1,1],
      [0,1,1,1,0],
      [0,0,1,0,0]]

f1 = [[0,0,2,0,0],
      [0,1,1,1,0],
      [2,1,2,1,2],
      [0,1,1,1,0],
      [0,0,2,0,0]]

c1 = [[1,1,1],
      [1,0,0],
      [1,0,0]]

c2 = [[1,1,1],
      [0,0,1],
      [0,0,1]]

def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n',''))
    if destroy:
        os.system('rm '+fname)
    return data


def image_playback(box):
    f = plt.figure()
    os.system('ls remoteImagery/ >> images.txt')
    pictures = swap('images.txt', True)
    print str(len(pictures)) + " Pictures Found "
    reel = []
    matrices = []
    for picture in pictures:
        image = plt.imread('remoteImagery/' + picture)
        frame = image[box[0]:box[1],box[2]:box[3],1]
        matrices.append(frame)
        reel.append([plt.imshow(ndi.convolve(frame,f0,origin=0),'gray_r')])
    a = animation.ArtistAnimation(f, reel, interval=1000, blit=True, repeat_delay=1000)
    plt.show()
    return matrices


def pi_see(box):
    os.system("echo 'Updating Image Library'")
    os.system('git pull origin')
    return image_playback(box)


def read_page(matrices):
    f = plt.figure()
    film = []


def main():
    box = np.array([700, 1500, 1000, 1800])
    images = pi_see(box)
    test = images.pop()
    print test.shape
    plt.imshow(images.pop())
    plt.title('Unedited Frame (color adjustment)')
    plt.show()
    plt.imshow(ndi.convolve(test, f0, origin=0), 'gray_r')
    plt.title('Frame with filtering')
    plt.show()
    read_page(images)



if __name__ == '__main__':
    main()
