import numpy as np
from geometry import Point2D, Point3D


class Camera:
    def __init__(self, k_matrix, m_matrix):
        self.im_cols = 512
        self.im_rows = 424
        self.k = k_matrix
        self.m = m_matrix
        self.c_x = k_matrix[0, 2]
        self.c_y = k_matrix[1, 2]
        self.f_x = k_matrix[0, 0]
        self.f_y = k_matrix[1, 1]

    def project_point(self, point: Point2D, img):
        """ Project a point to 3D coordinates """
        x = (point.x - self.c_x) * img[point.row, point.col] / self.f_x
        y = (point.y - self.c_y) * img[point.row, point.col] / self.f_y
        z = img[point.row, point.col]
        return x, y, z

    def normalized_image_point(self, point: Point2D) -> Point3D:
        """ Project a point into the normalized image plane """
        x = (point.x - self.c_x) / self.f_x
        y = (point.y - self.c_y) / self.f_y
        z = 1
        return Point3D(x, y, z)

    def project_frame(self, depth_frame):
        """ Project all points in a depth frame into 3D coordinates """
        points = np.array([self.project_point(Point2D(ix, iy), depth_frame)
                           for iy, ix in np.ndindex(depth_frame.shape)])
        return points

    def reproject_point(self, point: Point3D) -> Point2D:
        """ Find the 2D point of the 3D point """
        coord = np.array([[point.x], [point.y], [point.z]])
        extrinsic = np.matmul(self.m, np.append(coord, 1).transpose())
        extrinsic = np.matmul(np.eye(3, 4), extrinsic.transpose())
        extrinsic = np.array([extrinsic[0] / extrinsic[2], extrinsic[1] / extrinsic[2], 1])
        # adding translation, because color_sensor:
        extrinsic = np.add(extrinsic, np.array([.02, 0, 0]))
        intrinsic = np.matmul(self.k, extrinsic.transpose())
        column, row = intrinsic[0], intrinsic[1]
        return Point2D(int(column), int(row))

    def point_in_cam(self, point: Point3D) -> Point3D:
        coord = np.array([[point.x], [point.y], [point.z]])
        extrinsic = np.matmul(self.m, np.append(coord, 1).transpose())
        extrinsic = np.matmul(np.eye(3, 4), extrinsic.transpose())
        return Point3D(extrinsic[0], extrinsic[1], extrinsic[2])
