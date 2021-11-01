import numpy as np
import json
import re
from camera import Camera
from os import listdir
from os.path import isfile, join


class DataLoader:
    """
    Object for loading data.
    Data is accessed through frame- and kinect-number.
    One DataLoader object is needed per sequence. Use of this class would
    therefore be:
    DataLoader sequence_name = DataLoader(data_path, sequence_name)
    depth_image, _ = sequence_name.frame(idx)
    """
    def __init__(self, data_path: str, sequence: str):
        self.depth_dir = f'{data_path}/{sequence}/kinect_shared_depth'
        self.kinect_calib = f'{data_path}/{sequence}/kcalibration_{sequence}.json'
        self.kinect_sync_table = f'{data_path}/{sequence}/ksynctables_{sequence}.json'
        self.panoptic_calib = f'{data_path}/{sequence}/calibration_{sequence}.json'
        self.panoptic_sync_table = f'{data_path}/{sequence}/synctables_{sequence}.json'
        self.body_3d_scene_dir = f'{data_path}/{sequence}/hdPose3d_stage1_coco19'
        self.sensors = None
        self.color_sensors = None
        with open(self.kinect_calib, 'r') as calib_file:
            calib = json.load(calib_file)
            self.sensors = calib['sensors']
        with open(self.panoptic_calib, 'r') as calib_file:
            calib = json.load(calib_file)
            self.color_sensors = [c for c in calib['cameras'] if c['type'] == 'kinect-color']
        # The kinect number mapping tells us which index in the self.sensors array
        # the corresponding kinect node is.
        self.kinect_number_mapping = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.kinect_nodes = ['KINECTNODE1', 'KINECTNODE2', 'KINECTNODE3', 'KINECTNODE4',
                             'KINECTNODE5', 'KINECTNODE6', 'KINECTNODE7', 'KINECTNODE8',
                             'KINECTNODE9', 'KINECTNODE10']
        self.cameras = [Camera(*self._k_m_matrix(n)) for n in self.kinect_nodes]

    def frame(self, idx: int, kinect_node: str):
        """
        Return depth image, and bodies and the camera at idx for the specified node.
        Bodies are at format: [x0, y0, z0, score0, x1, y1, ...]
        """
        bodies, univ_time = self._bodies_univ_time(idx)
        depth_idx = self._nearest_depth(univ_time, kinect_node)
        depth_image = self._depth_image(depth_idx, kinect_node)
        camera = self._get_camera(kinect_node)

        return depth_image, bodies, camera

    def min_max(self):
        files = [int(re.findall(r'\d+', f)[1]) for f in listdir(self.body_3d_scene_dir)]
        files.sort()
        return files[0], files[-1]

    def _get_camera(self, kinect_node: str):
        return self.cameras[self.kinect_nodes.index(kinect_node)]

    def _bodies_univ_time(self, idx: int):
        """
        Load the body3DScene file at the specified index
        returns both an array of skeletons and the univ_time
        for this idx
        """
        fpath = f'{self.body_3d_scene_dir}/body3DScene_{idx:08}.json'
        with open(fpath, 'r') as scene_file:
            metafile = json.load(scene_file)
        univ_time = metafile['univTime']
        bodies = [joint_array['joints19'] for joint_array in metafile['bodies']]
        return np.array(bodies, dtype=float), univ_time

    def _nearest_depth(self, univ_time: float, kinect_node: str):
        """
        Find the nearest depth image to the univ_time for the given node
        """
        sync_table = None
        with open(self.kinect_sync_table, 'r') as sync_table_file:
            sync_table = json.load(sync_table_file)
        timestamps = sync_table['kinect']['depth'][kinect_node]['univ_time']
        closest = min(range(len(timestamps)), key=lambda i: abs(timestamps[i] - univ_time))
        return closest

    def _depth_image(self, depth_idx: int, kinect_node: str):
        im_cols = 512
        im_rows = 424
        f_size = im_cols * im_rows

        fpath = f'{self.depth_dir}/{kinect_node}/depthdata.dat'
        im = None
        with open(fpath, 'rb') as s_file:
            # offset is multiplied by 2 because uint16 takes two bytes per number
            a = np.fromfile(s_file, dtype=np.uint16, offset=2*f_size*depth_idx, count=f_size)
            a = a.reshape((im_rows, im_cols))
            im = np.fliplr(a)
        return im

    def _k_m_matrix(self, kinect_node: str):
        kinect_number = int(re.search(r'\d+', kinect_node).group())
        sensor = self.sensors[self.kinect_number_mapping.index(kinect_number)]
        sensor_name = f'50_{kinect_number:02}'
        color_sensor = next(s for s in self.color_sensors if s['name'] == sensor_name)
        k_matrix = np.array(sensor['K_depth'])
        m_matrix = np.concatenate((np.array(color_sensor['R']), np.array(color_sensor['t'])), axis=1)
        m_matrix = np.concatenate((m_matrix, np.array([[0, 0, 0, 1]])), axis=0)
        return k_matrix, m_matrix
