import numpy as np
from matplotlib import pyplot as plt


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

"""
Matlab code:
function [im] = readDepthIndex_1basedIdx(fname, idx)
    % Read depth frame at file index (1-based) idx
    % Each frame is 512x424 16-bit uint.
    fid = fopen(fname, 'rb');
    fseek(fid, 2*512*424*(idx-1), 'bof');
    data1 = fread(fid, 512*424, 'uint16=>uint16');
    fclose(fid);
    % Data is stored in row-major.
    im = double(reshape(data1, 512, 424))';
    im = im(:,end:-1:1,:); % Flip left-right
end  
"""



if __name__ == '__main__':
    show_depth_frame("../data/160226_haggling1/kinect_shared_depth/KINECTNODE6/depthdata.dat", 4592)
