import numpy as np
import json
import re


class DataLoader:
    """
    Object for accessing files in the training set.
    When loading a sample, the skeleton file has to be chosen first, and then the corresponding
    depth frame is found.
    :param root_path: points to the /data folder.
    :param sequence: points to the sequence we want.
    """
    def __init__(self, root_path, sequence):
        self.depth_dir = f'{root_path}/{sequence}/kinect_shared_depth'
        self.kinect_calib = f'{root_path}/{sequence}/kcalibration_{sequence}.json'
        self.kinect_sync_table = f'{root_path}/{sequence}/ksynctables_{sequence}.json'
        self.panoptic_calib = f'{root_path}/{sequence}/calibration_{sequence}.json'
        self.panoptic_sync_table = f'{root_path}/{sequence}/synctables_{sequence}.json'
        self.body_3d_scene_dir = f'{root_path}/{sequence}/hdPose3d_stage1_coco19'
        self.sensors = None
        self.color_sensors = None
        with open(self.kinect_calib, 'r') as calib_file:
            calib = json.load(calib_file)
            self.sensors = calib['sensors']
        with open(self.panoptic_calib, 'r') as calib_file:
            calib = json.load(calib_file)
            self.color_sensors = [c for c in calib['cameras'] if c['type'] == 'kinect-color']
        # The kinect nubmer mapping tells us which index in the self.sensors array
        # the corresponding kinectnode is.
        self.kinect_number_mapping = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def load_depth_frame(self, kinect_node: str, idx: int):
        """
        Read a depth frame
        :param kinect_node:  Name of the kinect node, KINECTNODE[1-10]
        :param idx:          Index where the frame should be read (indexed from 0)
        :return:             Numpy uint16 array
        """
        im_cols = 512
        im_rows = 424
        f_size = im_cols * im_rows

        fpath = f'{self.depth_dir}/{kinect_node}/depthdata.dat'
        im = None
        with open(fpath, 'rb') as s_file:
            # offset is multiplied by 2 because uint16 takes to bytes per number
            a = np.fromfile(s_file, dtype=np.uint16, offset=2*f_size*idx, count=f_size)
            a = a.reshape((im_rows, im_cols))
            im = np.fliplr(a)
        return im

    def load_body_file(self, idx: int):
        """
        Load the body3DScene file at the specified index
        :param idx: Index of the body3DScene file
        :return:    an array of bodies, and the univ_time for this file
        """
        fpath = self.body_3d_scene_dir + f'/body3DScene_{idx:08}.json'
        with open(fpath, 'r') as scene_file:
            metafile = json.load(scene_file)
        univ_time = metafile['univTime']
        bodies = [joint_array['joints19'] for joint_array in metafile['bodies']]
        return np.array(bodies, dtype=float), univ_time
        
    def calculate_ground_truth_map(self, kinect_node: str, scene_idx: int, limb: int):
        """
        Load the GT map for the specified limb(s) at index scene_idx from the specified 
        KinectNode.
        :param kinect_node:  Name of the kinect node, KINECTNODE[1-10]
        :param scene_idx:    Index of the 3d scene
        :param limb:         Index of limb from the skeleton
        :return:             Vector field of limb directions
        """
        scene_time = 100
        im_cols = 512
        im_rows = 424
        f_size = im_cols * im_rows

    def nearest_depth_idx(self, univ_time: float, kinect_node: str):
        """
        Find the nearest kinect index to the input univ_time
        :param univ_time:   Timestamp for 3d scene
        :param kinect_node: The kinect node
        :return:            Index of the closest depth frame
        """
        with open(self.kinect_sync_table, 'r') as sync_table_file:
            sync_table = json.load(sync_table_file)
        timestamps = sync_table['kinect']['depth'][kinect_node]['univ_time']
        closest = min(range(len(timestamps)), key=lambda i: abs(timestamps[i] - univ_time))
        return closest

    def project_points(self, kinect_n: str, depth_frame):
        """Project points from a depth frame into 3D coordinates"""
        kinect_number = int(re.search(r'\d+', kinect_n).group())
        sensor = self.sensors[self.kinect_number_mapping.index(kinect_number)]
        k_depth = np.array(sensor['K_depth'])
        c_xd = k_depth[0, 2]
        c_yd = k_depth[1, 2]
        f_xd = k_depth[0, 0]
        f_yd = k_depth[1, 1]

        points = np.array([self.project_point(c_xd, c_yd, f_xd, f_yd, ix, iy, depth_frame) for ix, iy in np.ndindex(depth_frame.shape)])
        return points

    def project_point(self, cx, cy, fx, fy, iy, ix, img):
        """Project a point into 3D coordinates"""
        # x = col, y = row
        x = (ix - cx) * img[iy, ix] / fx
        y = (iy - cy) * img[iy, ix] / fy
        z = img[iy, ix]
        return x, y, z

    def reproject_point(self, kinect_n: str, coord):
        """
        Find the row, column position of the given 3d point in the kinect
        :param kinect_n: kinect node ("KINECTNODE[1-10])")
        :param coord:    world coordinates in a 3x1 vector (3 rows, 1 column)
        :return:         row, column in the given kinect depth image
        """
        kinect_number = int(re.search(r'\d+', kinect_n).group())
        sensor = self.sensors[self.kinect_number_mapping.index(kinect_number)]
        sensor_name = f'50_{kinect_number:02}'
        color_sensor = next(s for s in self.color_sensors if s['name'] == sensor_name)

        # m_world = np.array(sensor['M_world2sensor'], dtype=float)
        # m_depth = np.array(sensor['M_depth'], dtype=float)
        k_depth = np.array(sensor['K_depth'])
        distort_d = np.array(sensor['distCoeffs_depth'])

        # _m = np.matmul(m_depth, m_world) * 10
        _m = np.concatenate((np.array(color_sensor['R']), np.array(color_sensor['t'])), axis=1)
        _m = np.concatenate((_m, np.array([[0, 0, 0, 1]])), axis=0)

        _extrinsic = np.matmul(_m, np.append(coord, 1).transpose())
        _extrinsic = np.matmul(np.eye(3, 4), _extrinsic.transpose())
        _extrinsic = np.array([_extrinsic[0]/_extrinsic[2], _extrinsic[1]/_extrinsic[2], 1])
        _extrinsic = np.add(_extrinsic, np.array([.02, 0, 0]))
        _intrinsic = np.matmul(k_depth, _extrinsic.transpose())

        column, row = _intrinsic[0], _intrinsic[1]
        # Apply distortion
        # x = projectPoints(coord, k_depth, _r, _t, distort_d)
        # return x
        return int(row), int(column)

    def reproject_points(self, kinect_n, coord: np.ndarray):
        kinect_number = int(re.search(r'\d+', kinect_n).group())
        sensor_name = f'50_{kinect_number:02}'
        sensor = self.sensors[self.kinect_number_mapping.index(kinect_number)]
        color_sensor = next(s for s in self.color_sensors if s['name'] == sensor_name)

        # camera intrinsics/extrinsics
        k_depth = np.array(sensor['K_depth'])
        _m = np.concatenate((np.array(color_sensor['R']), np.array(color_sensor['t'])), axis=1)
        _m = np.concatenate((_m, np.array([[0, 0, 0, 1]])), axis=0)
        coord = np.concatenate((coord, [np.ones(coord.shape[1])]), axis=0)

        ex = np.matmul(_m, coord)
        ex = np.matmul(np.eye(3, 4), ex)
        ex = np.array([ex[0, :]/ex[2, :], ex[1, :]/ex[2, :], np.ones(ex.shape[1])])
        ex = np.add(ex, np.array([[0.02, 0, 0]]).T)

        intr = np.matmul(k_depth, ex)
        columns, rows = intr[0, :]/intr[2, :], intr[1, :]/intr[2, :]

        return rows.astype(int), columns.astype(int)
