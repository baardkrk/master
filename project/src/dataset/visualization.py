from matplotlib import pyplot as plt
from target_maps import magnitude_map
from loader import DataLoader
from geometry import Point3D
from util import line_a_b
import numpy as np
import math
import open3d as o3d

edges = [
    (0, 1), (0, 2), (1, 15), (15, 16), (0, 3), (3, 4), (4, 5),
    (2, 6), (6, 7), (7, 8), (1, 17), (17, 18), (0, 9), (9, 10),
    (10, 11), (2, 12), (12, 13), (13, 14)
]


"""
What would make the most sense is to draw all the edges of a specific type, all at once.

"""


def show_depth_frame(kinect_node, idx, loader: DataLoader):
    depth_frame, _, _ = loader.frame(idx, kinect_node)
    plt.imshow(depth_frame, cmap='magma', interpolation='nearest')
    plt.colorbar()
    plt.show()


def show_depth_frame_as_pointcloud(kinect_node, idx, loader: DataLoader):
    depth_image, _, camera = loader.frame(idx, kinect_node)
    points = camera.project_frame(depth_image)

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])


def display_skeleton(kinect_node, idx, loader):
    depth_image, bodies, camera = loader.frame(idx, kinect_node)

    cmap = plt.get_cmap('jet')
    rgba = cmap(depth_image)

    bodies_p = []
    for body in bodies:
        bodies_p.append([camera.reproject_point(Point3D(i[0], i[1], i[2]))
                         for i in body.reshape(-1, 4)])
    edge_vectors = []
    for edge in edges:
        for body in bodies:
            edge_vectors.append(body)
        print(body)
    edge_pixel_array = []
    for edge in edges:
        for body in bodies_p:
            point_a = body[edge[0]]  # Point2D
            point_b = body[edge[1]]
            rows, cols = depth_image.shape
            line_pixels = line_a_b(rows, cols, point_a, point_b)
            edge_pixel_array.append(line_pixels)
            # for pixel in line_pixels:
            #     rgba[pixel.col, pixel.row] = 255

    plt.imshow(depth_image, interpolation='nearest', cmap='jet')
    plt.imshow(rgba)
    plt.show()


def body_3d_coords(body_array):
    coords = []
    skeleton = body_array.reshape(-1, 4).transpose()
    for i in skeleton:
        print(i)
        coords.append(Point3D(skeleton[i][0], skeleton[i][1], skeleton[i][2]))
    return coords


def read_bodies(bodies):
    skeletons = []
    xs = np.array([], dtype=float)
    ys = np.array([], dtype=float)
    zs = np.array([], dtype=float)
    for body in bodies:
        body = np.array(body)
        skeleton = body.reshape(-1, 4).transpose()
        xs = np.concatenate([xs, skeleton[0, :]])
        ys = np.concatenate([ys, skeleton[1, :]])
        zs = np.concatenate([zs, skeleton[2, :]])
        skeletons.append(skeleton)
    return skeletons, zs, ys, zs


def skeleton_visualization_3d(loader: DataLoader, idx: int):
    bodies, univ_time = loader._bodies_univ_time(idx)
    skeletons, xs, ys, zs = read_bodies(bodies)

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')
    # Plot landmarks
    ax.scatter(xs, ys, zs)
    # Draw lines between edges in each skeleton
    for skeleton in skeletons:
        for edge in edges:
            coords_x = [skeleton[0, edge[0]], skeleton[0, edge[1]]]
            coords_y = [skeleton[1, edge[0]], skeleton[1, edge[1]]]
            coords_z = [skeleton[2, edge[0]], skeleton[2, edge[1]]]
            ax.plot(coords_x, coords_y, coords_z)
    # Ensure equal axis
    max_range = np.array([xs.max() - xs.min(), ys.max() - ys.min(), zs.max() - zs.min()]).max() / 2.0

    mid_x = (xs.max() + xs.min()) * 0.5
    mid_y = (ys.max() + ys.min()) * 0.5
    mid_z = (zs.max() + zs.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.show()


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


if __name__ == '__main__':
    loader = DataLoader('../data', '160226_haggling1')

    # epanechnikov_2d(5, 5)
    # skeleton_visualization_3d(loader, 144)  # [x]
    # show_depth_frame('KINECTNODE6', 144, loader)  # [x]
    # show_depth_frame_as_pointcloud('KINECTNODE6', 144, loader)  # [x]
    display_skeleton('KINECTNODE6', 144, loader)  # [ ]
    # skeleton = Skeleton(np.zeros(76))
    # print(skeleton.joint_coordinates(SkeletonJoint.L_ELBOW))
