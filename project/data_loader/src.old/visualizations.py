from matplotlib import pyplot as plt
from target_maps import magnitude_map
from data_loader import DataLoader
from skeleton import Skeleton, SkeletonJoint, SkeletonLimbs
import numpy as np
import math
import open3d as o3d


edges = [
    (0, 1), (0, 2), (1, 15), (15, 16), (0, 3), (3, 4), (4, 5),
    (2, 6), (6, 7), (7, 8), (1, 17), (17, 18), (0, 9), (9, 10),
    (10, 11), (2, 12), (12, 13), (13, 14)
]


def show_depth_frame(kinect_node, idx, loader: DataLoader):
    bodies, univ_time = loader.load_body_file(idx)
    kinect_idx = loader.nearest_depth_idx(univ_time, kinect_node)
    array = loader.load_depth_frame(kinect_node, kinect_idx)
    plt.imshow(array, cmap='magma', interpolation='nearest')
    plt.colorbar()
    plt.show()


def show_depth_frame_as_pointcloud(kinect_node, idx, loader: DataLoader):
    bodies, univ_time = loader.load_body_file(idx)
    kinect_idx = loader.nearest_depth_idx(univ_time, kinect_node)
    depth_frame = loader.load_depth_frame(kinect_node, kinect_idx)
    points = loader.project_points(kinect_node, depth_frame)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.visualization.draw_geometries([pcd])


def display_skeleton(kinect_node, idx, loader):
    bodies, univ_time = loader.load_body_file(idx)
    skeleton_list = [Skeleton(x) for x in bodies]

    kinect_idx = loader.nearest_depth_idx(univ_time, kinect_node)
    img = loader.load_depth_frame(kinect_node, kinect_idx)

    cmap = plt.get_cmap('jet')
    rgba = cmap(img)
    rgba[:, :, 0] *= 0
    for skeleton in skeleton_list:
        joints = skeleton_2d_points(skeleton, loader, kinect_node)

        edges = []
        for limb in SkeletonLimbs:
            point_a = joints[limb.value[0].value]
            point_b = joints[limb.value[1].value]
            edges.append(((point_a[0], point_a[1]), (point_b[0], point_b[1])))

        mag_map = magnitude_map(img, edges)
        rgba[:, :, 0] += mag_map
        # img = np.multiply(img, mag_map)

    plt.imshow(img, interpolation='nearest', cmap='jet')
    plt.imshow(rgba)
    plt.show()


def display_skeletons_batch(kinect_node, idx, loader):
    bodies, univ_time = loader.load_body_file(idx)
    kinect_idx = loader.nearest_depth_idx(univ_time, kinect_node)
    img = loader.load_depth_frame(kinect_node, kinect_idx)
    cmap = plt.get_cmap('jet')
    rgba = cmap(img)
    rgba[:, :, 0] *= 0

    for body in bodies:
        coords = body.reshape(-1, 4)[:, :3].T
        rows, cols = loader.reproject_points(kinect_node, coords)
        edge_coords = [((rows[e[0]], cols[e[0]]), (rows[e[1]], cols[e[1]])) for e in edges]
        mag_map = magnitude_map(img, edge_coords)
        rgba[:, :, 0] += mag_map

    plt.imshow(img, interpolation='nearest', cmap='jet')
    plt.imshow(rgba)
    plt.show()


def skeleton_2d_points(skeleton: Skeleton, loader: DataLoader, kinect_node: str):
    joints = []
    for joint in SkeletonJoint:
        joints.append(loader.reproject_point(kinect_node, skeleton.joint_coordinates(joint)))
    # joints = loader.reproject_point(kinect_node, skeleton.coordinates[0:3, :])
    return joints


def skeleton_visualization_3d(loader: DataLoader, idx: int):
    bodies, univ_time = loader.load_body_file(idx)
    skeletons = []
    xs = np.array([], dtype=float)
    ys = np.array([], dtype=float)
    zs = np.array([], dtype=float)
    # Extract body coordinates
    for body in bodies:
        body = np.array(body)
        skeleton = body.reshape(-1, 4).transpose()
        xs = np.concatenate([xs, skeleton[0, :]])
        ys = np.concatenate([ys, skeleton[1, :]])
        zs = np.concatenate([zs, skeleton[2, :]])
        skeletons.append(skeleton)

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')
    # Plot landmarks
    ax.scatter(xs, ys, zs)
    # Draw lines between edges in each skeleton
    for skeleton in skeletons:
        for edge in SkeletonLimbs:
            coords_x = [skeleton[0, edge.value[0].value], skeleton[0, edge.value[1].value]]
            coords_y = [skeleton[1, edge.value[0].value], skeleton[1, edge.value[1].value]]
            coords_z = [skeleton[2, edge.value[0].value], skeleton[2, edge.value[1].value]]
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


def stack_skeletons(loader: DataLoader):
    pass


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

    # display_skeletons_batch('KINECTNODE6', 144, loader)
    # show_depth_frame_as_pointcloud('KINECTNODE6', 144, loader)
    # epanechnikov_2d(5, 5)
    # skeleton_visualization_3d(loader, 144)
    # show_depth_frame('KINECTNODE6', 144, loader)
    display_skeleton('KINECTNODE6', 144, loader)
    # skeleton = Skeleton(np.zeros(76))
    # print(skeleton.joint_coordinates(SkeletonJoint.L_ELBOW))
