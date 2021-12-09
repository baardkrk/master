from util import kernel, line_a_b
from geometry import Point3D, distance_to_3d_line, Line3D
import numpy as np


def target_map(bodies, edges, camera, imsize):
    rows, cols = imsize
    bodies_2D = []  # pixel points for the edges
    bodies_3D = []
    for body in bodies:
        bodies_2D.append([camera.reproject_point(Point3D(i[0], i[1], i[2]))
                          for i in body.reshape(-1, 4)])
        bodies_3D.append([camera.point_in_cam(Point3D(i[0], i[1], i[2]))
                          for i in body.reshape(-1, 4)])
    # Creating a array on format:
    # array: [ body0: [ edge0: [im], edge1: [im], ...],
    #          body1: [ edge0: [im], edge1: [im], ...],
    #           ... ]
    edge_array = create_edge_map(bodies_2D, bodies_3D, imsize, edges, camera)
    joint_array = create_joint_map()
    return edge_array, joint_array


def create_edge_map(bodies_2D, bodies_3D, imsize, edges, camera):
    rows, cols = imsize
    # Saving the edges in an array that has the following dimensions:
    # (bodyNum, edgeNum, dme(distance, magnitude, x, y, z), rows (height), cols (width))
    edge_array = np.zeros((len(bodies_2D), 5, rows, cols)) # want the edges at axis=1 remove for viz> len(edges),
    tmp_dst_array = np.zeros((len(bodies_2D), rows, cols))
    for idx, (body2D, body3D) in enumerate(zip(bodies_2D, bodies_3D)):
        body_map = np.zeros((len(edges), 5, rows, cols))
        tmp_dst_map = np.zeros((len(edges), rows, cols))

        for b_idx, edge in enumerate(edges):
            body_map[b_idx], tmp_dst_map[b_idx] = process_edge(edge, imsize, camera, rows, cols, body2D, body3D)

        # body_map = np.amax(body_map, axis=0)
        # Filter edge channels (18) and pick the edges that are closest to the camera
        edge_array[idx] = smash_dimension(body_map)

        tmp_dst_array[idx] = np.amax(tmp_dst_map, axis=0)

    # Filter bodies and pick the ones closest to the camera
    res = smash_dimension(edge_array)
    # TODO create edge array from
    # tmp = np.amax(edge_array[:, 1, 0, :, :], axis=0)
    return res[0, :, :]


def process_edge(edge, imsize, camera, rows, cols, body2D, body3D):
    # Edge is at format (joint_a, joint_b)
    # Draw the 2D edge, and constrain the interval:
    # array of 2D pixels in the line
    line_pixels = line_a_b(rows, cols, body2D[edge[0]], body2D[edge[1]])
    # Add the kernels to the pixel positions
    # 1) Find the Line3D equation for the edge we're currently at
    # 2) Calculate the distance along the projected line going through
    #    each pixel to the Closest point on the Line3D for the edge.
    line_eq = Line3D(body3D[edge[0]], body3D[edge[1]])
    edge_vector = line_eq.u
    lim_points = (body3D[edge[0]], body3D[edge[1]])
    edge_map = np.zeros((len(line_pixels), 5, rows, cols))
    tmp_dst_map = np.zeros((len(line_pixels), rows, cols))
    for e_idx, pixel in enumerate(line_pixels):
        k_im, d_im, x_im, y_im, z_im = process_pixel(pixel, camera, line_eq,
                                                     lim_points, imsize, edge_vector)
        edge_map[e_idx, 0] = k_im
        edge_map[e_idx, 1] = d_im
        edge_map[e_idx, 2] = x_im
        edge_map[e_idx, 3] = y_im
        edge_map[e_idx, 4] = z_im
        tmp_dst_map[e_idx] = d_im

    # Add the edge_vector's (x,y,z) components to their respective maps
    # Edge map shape is: (pixels, kdxyz-channels, rows, cols)
    # idxs = np.argmax(edge_map[:, 1, :, :], axis=0)
    res = smash_dimension(edge_map)
    tmp_dst_map = np.amax(tmp_dst_map, axis=0)
    return res, tmp_dst_map

    # edge_map = edge_map[idxs, :, :, np.arange(edge_map.shape[-1])].T
    # edge_map = np.amax(edge_map, axis=0)
    # edge_map = pick_max(edge_map, 0, 1)
    # return edge_map


def smash_dimension(a):
    ind_0 = np.argmax(a[:, 0, :, :]/(a[:, 1, :, :] + 1e-9), axis=0)    # Shape (3, 4)
    ind_0 = np.argmax(a[:, 1, :, :] * a[:, 0, :, :], axis=0)    # Shape (3, 4)
    ind_2 = np.arange(a.shape[2])[:, np.newaxis] # Shape (3, 1)
    ind_3 = np.arange(a.shape[3])[np.newaxis]    # Shape (1, 4)
    C = a[ind_0, :, ind_2, ind_3]                # Shape (3, 4, 2)
    C = np.transpose(C, (2, 0, 1))               # Shape (2, 3, 4)
    return C


def process_pixel(pixel, camera, line_eq, lim_points, imsize, edge_vector):
    # find distance to 3D line through the 2D pixel
    # find 3D location for pixel
    dist = distance_to_3d_line(camera.normalized_image_point(pixel),
                               line_eq, lim_points)
    # create a kernel based on the distance to the 3D line
    # add that kernel to an output map, and add that output map to the
    # result array
    sigma = 3000 // dist  # Found something that seemed to work
    sigma = sigma if sigma % 2 != 0 else sigma+1
    sigma = max(sigma, 1e-10)
    _, _, k = kernel(sigma)
    k_im = kernel_image(k, pixel, imsize)
    d_im = k_im.copy()
    d_im[d_im > 0] = 1/dist
    x_im = k_im.copy()
    y_im = k_im.copy()
    z_im = k_im.copy()
    x_im[x_im > 0] = edge_vector.x
    y_im[y_im > 0] = edge_vector.y
    z_im[z_im > 0] = edge_vector.z
    return k_im, d_im, x_im, y_im, z_im


def pick_max(a, axis=0, idx=-1):
    print(a.shape)
    indices = np.argmax(a[:, idx, :], axis=axis)
    result = a[indices, :, np.arange(a.shape[-1])].T
    return result


def create_joint_map():
    pass


def kernel_image(k, pos, imsize):
    img = np.zeros(imsize)
    k_max = max(k.shape)
    k_size = k_max // 2  # floor division
    if k_size <= 1:
        return img

    # Assume pos.row/col is zero indexed
    # irs: image row start, # kce: kernel col end ....
    krs = -1 * min(pos.row - k_size, 0)
    kre = k_max-1 + min(0, imsize[1]-1 - (pos.row+k_size)) + 1   # Because indexing
    kcs = -1 * min(pos.col - k_size, 0)
    kce = k_max-1 + min(0, imsize[0]-1 - (pos.col+k_size)) + 1

    irs = max(0, pos.row - k_size)
    ire = min(pos.row + k_size, imsize[1] - 1) + 1
    ics = max(0, pos.col - k_size)
    ice = min(pos.col + k_size, imsize[0] - 1) + 1

    img[ics:ice, irs:ire] = k[kcs:kce, krs:kre]
    return img


# A = np.array([[[1, 2, 3, 4],
#                [0, 1, 2, 1]],
#               [[5, 6, 7, 8],
#                [1, 0, 3, 1]]])
# B = np.array([[[ 1,  2,  3,  4],
#                [ 5,  6,  7,  8],
#                [ 0,  1,  2,  1]],
#               [[ 9, 10, 11, 12],
#                [13, 14, 15, 16],
#                [ 1,  0,  3,  1]],
#               [[17, 18, 19, 20],
#                [21, 22, 23, 24],
#                [ 0,  0,  0,  2]]])

# C = np.array([[[[ 1,  2,  3,  4],
#                 [ 5,  6,  7,  8],
#                 [ 9, 10, 11, 12]],
#                [[13, 14, 15, 16],
#                 [17, 18, 19, 20],
#                 [21, 22, 23, 24]]],
#               [[[25, 26, 27, 28],
#                 [29, 30, 31, 32],
#                 [33, 34, 35, 36]],
#                [[37, 38, 39, 40],
#                 [41, 42, 43, 44],
#                 [45, 46, 47, 48]]]])

# D = np.array([[[[ 1,  2,  3,  4],
#                 [ 5,  6,  7,  8],
#                 [ 9, 10, 11, 12]],
#                [[ 0,  0,  0,  0],
#                 [ 0,  1,  1,  1],
#                 [ 0,  0,  0,  0]]],
#               [[[25, 26, 27, 28],
#                 [29, 30, 31, 32],
#                 [33, 34, 35, 36]],
#                [[ 0,  1,  2,  0],
#                 [ 0,  1,  2,  0],
#                 [ 0,  1,  2,  0]]]])
