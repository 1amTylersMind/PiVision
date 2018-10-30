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
        frame = image[box[0]:box[1],box[2]:box[3],1]   # For whatever reason 1 works better than 0,2
        matrices.append(ndi.convolve(frame,f0,origin=0))
        reel.append([plt.imshow(ndi.convolve(frame,f0,origin=0),'gray_r')])
    a = animation.ArtistAnimation(f, reel, interval=1000, blit=True, repeat_delay=1000)
    plt.show()
    return matrices


def pi_see(box):
    os.system("echo 'Updating Image Library'")
    os.system('git pull origin')
    return image_playback(box)


def read_page(matrices):
    slice_stack = []
    for matrix in matrices:
        # scanning_data = scan_image(matrix)
        img_slices = box_filter_maker(matrix)
        slice_stack.append(img_slices)

    # Process the slice stack looking for deviations in noise
    # test = slice_stack.pop(1)[6]
    image_processing(slice_stack)


def image_processing(sliceStack):
    for slab in sliceStack:
        for iMat in slab.values():
            test = np.array(iMat).flatten()
            signal = []
            buff = []
            buffsz = 25
            for point in test:
                buff.append(point)
                if len(buff) == buffsz:
                    signal.append(np.sum(np.array(buff)))
                    buff = []
            samples = int(test.shape[0] / buffsz)
            plt.plot(np.linspace(0, samples, samples), signal)
            plt.show()


def box_filter_maker(matrix):
    bounds = matrix.shape
    philBox = [[1,1,1,1,1],
               [1,0,0,0,1],
               [1,0,0,0,1],
               [1,0,0,0,1],
               [1,1,1,1,1]]
    invPhil  = np.ones(np.array(philBox).shape) - np.array(philBox)
    boxRow = np.concatenate((philBox, philBox, philBox,
                             philBox, philBox, philBox,
                             philBox, philBox, philBox,
                             philBox),1)
    grid = np.concatenate((boxRow, boxRow, boxRow, boxRow,
                           boxRow, boxRow, boxRow, boxRow,
                           boxRow, boxRow, boxRow), 0)

    # should i slice'N'dice Image to lower mem overhead ?
    # No, that makes it worse bc conv is cyc more expensive
    plt.imshow(ndi.convolve(matrix, invPhil,origin=0), 'gray_r')
    plt.show()

    qx = int(bounds[0]/4)
    qy = int(bounds[1]/4)

    slices = {1: matrix[0:qx, 0:qy],
              2: matrix[qx:2*qx, 0:qy],
              3: matrix[2*qx:3*qx, 0:qy],
              4: matrix[3*qx:4*qx, 0:qy],
              5: matrix[0:qx, qy:2*qy],
              6: matrix[qx:2*qx, qy:2*qy],
              7: matrix[2*qx:3*qx, qy:2*qy],
              8: matrix[3*qx:4*qx, qy:2*qy],
              9: matrix[0:qx, 2*qy:3*qy],
              10:matrix[qx:2*qx, 2*qy:3*qy],
              11:matrix[2*qx:3*qx, 2*qy:3*qy],
              12:matrix[3*qx:4*qx, 2*qy:3*qy],
              13:matrix[0:qx, 3*qy:4*qy],
              14:matrix[qx:2*qx, 3*qy:4*qy],
              15:matrix[2*qx:3*qx, 3*qy:4*qy],
              16:matrix[3*qx:4*qx, 3*qy:4*qy]}

    # f = plt.figure()
    # film = []
    # for mat in slices.values():
    #     film.append([plt.imshow(ndi.convolve(mat,invPhil,origin=0),'gray_r')])
    # a = animation.ArtistAnimation(f,film,interval=300,blit=True,repeat_delay=900)
    # # Dont need to watch the whole thing actually
    return slices


def scan_image(matrix):
    f = plt.figure()
    avg = np.average(matrix)
    minima = np.min(matrix)
    maxima = np.min(matrix)
    xdim = matrix.shape[0]
    ydim = matrix.shape[1]
    Qxs = np.linspace(0,xdim,10)
    Qys = np.linspace(0,ydim,10)
    scan = []
    i = 0
    for qx in Qxs:
        Xi = int(qx)
        for qy in Qys:
            if i > 0:
                Yi = int(qy)
                square = matrix[0:Yi, 0:Xi]
                scan.append([plt.imshow(square, 'gray_r')])
            i += 1
    a = animation.ArtistAnimation(f,scan,interval=500,blit=True,repeat_delay=1000)
    plt.show()
    return scan


def main():
    box = np.array([700, 1500, 1000, 1800])
    images = pi_see(box)
    read_page(images)
    # test = images.pop()
    # print test.shape
    # plt.imshow(test)
    # plt.title('Unedited Frame (color adjustment)')
    # plt.show()
    # plt.imshow(ndi.convolve(test, f0, origin=0), 'gray_r')
    # plt.title('Frame with filtering')
    # plt.show()
    # read_page(images)



if __name__ == '__main__':
    main()
