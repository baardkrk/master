import math
import numpy as np
from skimage import draw
from geometry import Point3D, Point2D, Line3D, Vec3D, distance_to_3d_line


def line_to_array(d_array: np.ndarray, edges):
    """
    Returns an a set of arrays of row/column pairs for the input edges. The input
    edges are pairs of 2d points that a line should be drawn between.
    """
    edge_array = []
    idx = 0
    for edge in edges:
        start, end = edge[0], edge[1]
        rr, cc = draw.line(start[0], start[1], end[0], end[1])
        rr_s, rr_e = constrain_interval(rr, d_array.shape[0])
        cc_s, cc_e = constrain_interval(cc, d_array.shape[1])
        start = max(rr_s, cc_s)
        end = min(rr_e, cc_e)

        if end != -1:
            rr = rr[start:end]
            cc = cc[start:end]
            line_pixels = [(rr[i], cc[i]) for i in range(len(cc))]
            edge_array.append(line_pixels)
        idx += 1
    return edge_array


def line_a_b(img_rows: int, img_cols: int, point_a: Point2D, point_b: Point2D):
    """
    Return the constrained line pixel locations for the line going from
    point_a to point_b in the image.
    """
    rr, cc = draw.line(point_a.row, point_a.col, point_b.row, point_b.col)
    rr_s, rr_e = constrain_interval(rr, img_rows)
    cc_s, cc_e = constrain_interval(cc, img_cols)
    start = max(rr_s, cc_s)
    end = min(rr_e, cc_e)
    if end != -1:
        rr = rr[start:end]
        cc = cc[start:end]
        line_pixels = [Point2D(rr[i], cc[i]) for i in range(len(cc))]
    return line_pixels


def constrain_interval(arr, max_val):
    idx = 0
    while (arr[idx] < 0 or arr[idx] > max_val - 1) and idx < len(arr) - 1:
        idx += 1
    if idx >= len(arr):
        idx = -1
    arr_start = idx

    idx = len(arr) - 1
    while (arr[idx] < 0 or arr[idx] > max_val - 1) and idx > 0:
        idx -= 1
    if idx < 0:
        idx = -1
    arr_end = idx
    return arr_start, arr_end


def kernel(sigma):
    _x = np.arange(-sigma, sigma+1, 1)
    _y = np.arange(-sigma, sigma+1, 1)

    xx, yy = np.meshgrid(_x, _y)
    z = 1 - ((xx / sigma) ** 2 + (yy / sigma) ** 2)
    z = np.where(z > 0, z, 0)
    return _x, _y, z


def epanechnikov_2d(sigma, distance):
    _x = np.arange(-distance, distance + 2, 1)
    _y = np.arange(-distance, distance + 2, 1)
    xx, yy = np.meshgrid(_x, _y)
    z = ((2/(math.pi * sigma ** 2)) * (1 - ((xx/sigma)**2 + (yy/sigma)**2)))
    z = np.where(z > 0, z, 0)

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111)
    ax.pcolor(_x, _y, z)
    plt.show()


def add_max(org, kernels, centres):
    """
    Add the value of a kernel (of arbitrary size, on an arbitrary location),
    to an array if the value in the array is not larger than the value in the filter.
    """
    return org


def add_kernel(org: np.ndarray, kernel: np.ndarray, center):
    """
    Add the value of the kernel (of arbitrary size, on the location 'center'), to an array
    if the value in the array is not larger than the value in the kernel.
    """
    # place filter at the array, and exclude any locations that are out of bounds
    c_r, c_c = center.row, center.column
    k_r, k_c = kernel.shape
    row_start = max(0, k_r/2 - c_r)
    pass


if __name__ == '__main__':
    from matplotlib import pyplot as plt

    _x, _y, z = kernel(7)
    print(z)
    print(z.shape)
    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111)
    ax.pcolor(_x, _y, z)
    plt.show()
