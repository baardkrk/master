import numpy as np
from matplotlib import pyplot as plt
from data_loader import FilePaths

def load_depth_frame(fpath, idx):
    """
    Read a depth frame
    @param fpath: Filepath to depthdata binary
    @param idx:   Index where the frame should be read (indexed from 0)
    @return:      Numpy uint16 array
    """
    im_cols = 512
    im_rows = 424
    f_size = im_cols * im_rows

    im = None
    with open(fpath, 'rb') as s_file:
        # offset is multiplied by 2 because uint16 takes to bytes per number
        a = np.fromfile(s_file, dtype=np.uint16, offset=2*f_size*idx, count=f_size)
        a = a.reshape((im_rows, im_cols))
        im = np.fliplr(a)
    return im


def show_depth_frame(fpath, idx):
    array = load_depth_frame(fpath, idx)
    plt.imshow(array, interpolation='nearest')
    plt.show()


if __name__ == '__main__':
    file_paths = FilePaths('../data', '160226_haggling1')
    show_depth_frame(file_paths.depth_file('KINECTNODE6'), 4592)
    # show_depth_frame("../data/160226_haggling1/kinect_shared_depth/KINECTNODE6/depthdata.dat", 4592)
