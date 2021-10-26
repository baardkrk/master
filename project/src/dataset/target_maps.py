from camera import Camera
from util import constrain_interval, kernel
from geometry import Point2D, Point3D, distance_to_3d_line, Line3D
from skimage import draw
import numpy as np


# def tbd(img: np.ndarray, edges, edge_pixels):
#     """
#     img: the image (mostly just used for shape)
#     edges: 3D vector array with index of edges corresponding to index in edge_pixels
#     edge_pixels: An array of edge pixels
#     [edge0[[rr], [cc]], edge1[[rr], [cc]], ...]
#     """
#     depth_image, bodies, camera = loader.frame(idx, kinect_node)

#     cmap = plt.get_cmap('jet')
#     rgba = cmap(depth_image)
#     rgba[:, :, 0] *= 0

#     for body in bodies:
#         bodies_p = [camera.reproject_point(Point3D(i[0], i[1], i[2])) for i in body.reshape(-1, 4)]

#     edge_pixel_array = []
#     for edge in edges:
#         for body in bodies_p:
#             point_a = body[edge[0]]  # Point2D
#             point_b = body[edge[1]]
#             rows, cols = depth_image.shape
#             line_pixels = line_a_b(rows, cols, point_a, point_b)


def magnitude_map(kinect: Camera, rows, cols, edges):
    """ Returning a magnitude map for the given edges """
    line_map = np.zeros((len(edges), rows, cols))
    idx = 0
    for edge in edges:
        start, end = edge[0], edge[1]
        rr, cc = draw.line(start[0], start[1], end[0], end[1])
        rr_s, rr_e = constrain_interval(rr, rows)
        cc_s, cc_e = constrain_interval(cc, cols)
        start = max(rr_s, cc_s)
        end = min(rr_e, cc_e)

        if end != -1:
            rr = rr[start:end]
            cc = cc[start:end]
            line_map[idx] = add_kernels(rr, cc, line_map)
        idx += 1

    return line_map.sum(axis=0)


def get_kernel(point: Point2D, camera: Camera, edge):
    point3d = camera.normalized_image_point(point)
    dst = distance_to_3d_line(point, edge)


def edge_2_line(edge) -> Line3D:
    pass


def add_kernels(rr, cc, line_map):
    kern_map = np.zeros(line_map.shape)
    for idx in range(len(rr)):
        row, col = rr[idx], col[idx]

        kernel_size = int(20000 / (avg_depth(rr[idx], cc[idx], line_map) + 1e-5))
        kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
        k = kernel(int(kernel_size/2))
        # Adding the kernel to the line_map
        irs = max(0, rr[idx] - int(kernel_size/2))
        ire = min(line_map.shape[0], rr[idx] + int(kernel_size / 2) + 1)
        ics = max(0, cc[idx] - int(kernel_size/2))
        ice = min(line_map.shape[1], cc[idx] + int(kernel_size / 2) + 1)
        krs = -1 * min(rr[idx] - kernel_size, 0)
        kre = min(kernel_size, line_map.shape[0] - rr[idx])
        kcs = -1 * min(cc[idx] - kernel_size, 0)
        kce = min(kernel_size, line_map.shape[1] - cc[idx])
        kern_map[irs:ire, ics:ice] = np.where(kern_map[irs:ire, ics:ice] == 0, k[krs:kre, kcs:kce], kern_map[irs:ire, ics:ice])
    return kern_map
