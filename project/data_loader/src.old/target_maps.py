import numpy as np
from skimage import draw
from matplotlib import pyplot as plt


def magnitude_map(depth_image: np.ndarray, edges):
    """
    Create a magnitude map for the given points
    :param depth_image:  depth image
    :param edges:       list of 2d points
    :return:    magnitude map of same shape as depth image
    """
    r, c = depth_image.shape
    line_map = np.zeros((len(edges), r, c))
    idx = 0
    for edge in edges:
        start, end = edge[0], edge[1]
        rr, cc = draw.line(start[0], start[1], end[0], end[1])
        rr_s, rr_e = constrain_interval(rr, depth_image.shape[0])
        cc_s, cc_e = constrain_interval(cc, depth_image.shape[1])
        start = max(rr_s, cc_s)
        end = min(rr_e, cc_e)

        if end != -1:
            rr = rr[start:end]
            cc = cc[start:end]
            line_map[idx] = add_kernels(rr, cc, depth_image)
        idx += 1

    return line_map.sum(axis=0)


def add_kernels(rr, cc, depth_img):
    kern_map = np.zeros(depth_img.shape)
    for idx in range(len(rr)):
        kernel_size = int(20000/(avg_depth(rr[idx], cc[idx], depth_img) + 1e-5))
        kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        k = kernel(int(kernel_size/2))
        irs = max(0, rr[idx] - int(kernel_size/2))
        ire = min(depth_img.shape[0], rr[idx] + int(kernel_size/2) + 1)
        ics = max(0, cc[idx] - int(kernel_size/2))
        ice = min(depth_img.shape[1], cc[idx] + int(kernel_size/2) + 1)
        krs = -1 * min(rr[idx] - kernel_size, 0)
        kre = min(kernel_size, depth_img.shape[0] - rr[idx])
        kcs = -1 * min(cc[idx] - kernel_size, 0)
        kce = min(kernel_size, depth_img.shape[1] - cc[idx])
        kern_map[irs:ire, ics:ice] = np.where(kern_map[irs:ire, ics:ice] == 0, k[krs:kre, kcs:kce], kern_map[irs:ire, ics:ice])
    return kern_map


def avg_depth(r, c, img, w=3):
    rs = max(0, r-w)
    re = min(r+w, img.shape[0])
    cs = max(0, c-w)
    ce = min(c+w, img.shape[1])
    return np.average(img[rs:re, cs:ce])

def depth_to_line():
    """calculates the xyz position of the voxel at the input point"""

    pass


def kernel(sigma):
    _x = np.arange(-sigma, sigma + 1, 1)
    _y = np.arange(-sigma, sigma + 1, 1)

    xx, yy = np.meshgrid(_x, _y)
    z = 1 - ((xx/sigma)**2 + (yy/sigma)**2)
    z = np.where(z > 0, z, 0)
    return z


def constrain_interval(arr, max_val):
    idx = 0
    while (arr[idx] < 0 or arr[idx] > max_val-1) and idx < len(arr)-1:
        idx += 1
    if idx >= len(arr):
        idx = -1
    arr_start = idx

    idx = len(arr) - 1
    while (arr[idx] < 0 or arr[idx] > max_val-1) and idx > 0:
        idx -= 1
    if idx < 0:
        idx = -1
    arr_end = idx

    return arr_start, arr_end


if __name__ == '__main__':
    image = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    points = [((3, 0), (18, 14)), ((5, 13), (-5, 17)), ((-10, 4), (20, 3)), ((40, 4), (100, 5)), ((6, 27), (25, -5))]

    img = magnitude_map(image, points)
    plt.imshow(img, interpolation='nearest')
    plt.show()
