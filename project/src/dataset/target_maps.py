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
    edge_array = np.zeros((len(bodies_2D), rows, cols))
    idx = 0
    for body2D, body3D in zip(bodies_2D, bodies_3D):
        body_map = np.zeros((len(edges), rows, cols))
        b_idx = 0
        for edge in edges:  # Edge is at format (joint_a, joint_b)
            # Draw the 2D edge, and constrain the interval:
            # array of 2D pixels in the line
            line_pixels = line_a_b(rows, cols, body2D[edge[0]], body2D[edge[1]])
            # Add the kernels to the pixel positions
            # 1) Find the Line3D equation for the edge we're currently at
            # 2) Calculate the distance along the projected line going through
            #    each pixel to the Closest point on the Line3D for the edge.
            line_eq = Line3D(body3D[edge[0]], body3D[edge[1]])
            lim_points = (body3D[edge[0]], body3D[edge[1]])
            edge_map = np.zeros((len(line_pixels), rows, cols))
            e_idx = 0
            for pixel in line_pixels:  # pixel is 2D point
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
                # print(f'Sigma: {sigma}, Dist: {dist}')
                _, _, k = kernel(sigma)
                k_im = kernel_image(k, pixel, imsize)
                edge_map[e_idx] = k_im
                e_idx += 1
            edge_map = np.amax(edge_map, axis=0)
            # Apply vectors (TODO)
            body_map[b_idx] = edge_map
            b_idx += 1
        body_map = np.amax(body_map, axis=0)
        edge_array[idx] = body_map
        idx += 1
    edge_array = np.amax(edge_array, axis=0)
    return edge_array


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
