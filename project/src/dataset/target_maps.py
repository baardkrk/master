from camera import Camera
from util import constrain_interval, kernel, line_a_b
from geometry import Point2D, Point3D, distance_to_3d_line, Line3D
from skimage import draw
import numpy as np


def target_map(bodies, edges, camera, imsize):
    rows, cols = imsize
    bodies_2D = []  # pixel points for the edges
    bodies_3D = []
    for body in bodies:
        bodies_2D.append([camera.reproject_point(Point3D(i[0], i[1], i[2]))
                         for i in body.reshape(-1, 4)])
        bodies_3D.append([Point3D(i[0], i[1], i[2]) for i in body.reshape(-1, 4)])
    # Creating a array on format:
    # array: [ body0: [ edge0: [im], edge1: [im], ...],
    #          body1: [ edge0: [im], edge1: [im], ...],
    #           ... ]
    edge_array = []
    for body2D, body3D in zip(bodies_2D, bodies_3D):
        for edge in edges:  # Edge is at format (joint_a, joint_b)
            # Draw the 2D edge, and constrain the interval:
            # array of 2D pixels in the line
            line_pixels = line_a_b(rows, cols, body2D[edge[0]], body2D[edge[1]])
            # Add the kernels to the pixel positions
            # 1) Find the Line3D equation for the edge we're currently at
            # 2) Calculate the distance along the projected line going through
            #    each pixel to the Closest point on the Line3D for the edge.
            line_eq = Line3D(body3D[edge[0]], body3D[edge[1]])
            for pixel in line_pixels:  # pixel is 2D point
                # find distance to 3D line through the 2D pixel
                # find 3D location for pixel
                dist = distance_to_3d_line(camera.normalized_image_point(pixel), line_eq)
                # create a kernel based on the distance to the 3D line
                # add that kernel to an output map, and add that output map to the
                # result array
                sigma = int((-(1/100) * dist + max(imsize))/2)
                sigma = sigma if sigma % 2 != 0 else sigma+1
                k = kernel(sigma)
                k_im = kernel_image(k, pixel, imsize)
                print(dist)
    pass


def kernel_image(k, pos, imsize):
    img = np.zeros(imsize)
    k_size = (max(k.shape)//2)+1
    # k = kernel, i = image
    k_row_start = 0
    k_row_end = k.shape[0]
    k_col_start = 0
    k_col_end = k.shape[1]
    i_row_start = pos.row - (k_size-1)
    i_row_end = i_row_start + k.shape[0]
    i_col_start = pos.col - k_size
    i_col_end = i_col_start + k.shape[1]

    if i_row_start < 0:
        k_row_start = i_row_start * (-1)
        i_row_start = 0
    if i_row_end > imsize[0]:
        k_row_end = i_row_end - imsize[0]
        i_row_end = imsize[0]-1
    if pos.col - k_size < 0:
        k_col_start = i_col_start * (-1)
        i_col_start = 0
    if pos.col + k_size >= imsize[1]:
        k_col_end = i_col_end - imsize[1]
        i_col_end = imsize[1]-1
    img[i_row_start:i_row_end+1, i_col_start:i_col_end+1] = \
        k[k_row_start:k_row_end+1, k_col_start:k_col_end+1]
    return img

