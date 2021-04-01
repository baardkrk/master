import numpy as np
import json
from skeleton import Skeleton


class DataLoader:
    """
    Object for accessing files in the training set.
    When loading a sample, the skeleton file has to be chosen first, and then the corresponding
    depth frame is found.
    :param root_path: points to the /data folder.
    :param sequence: points to the sequence we want.
    """
    def __init__(self, root_path, sequence):
        self.depth_dir = "{0}/{1}/kinect_shared_depth".format(root_path, sequence)
        self.kinect_calib = "{0}/{1}/kcalibration_{1}.json".format(root_path, sequence, sequence)
        self.kinect_sync_table = "{0}/{1}/ksynctables_{1}.json".format(root_path, sequence)
        self.panoptic_calib = "{0}/{1}/calibration_{1}.json".format(root_path, sequence)
        self.panoptic_sync_table = "{0}/{1}/synctables_{1}.json".format(root_path, sequence)
        self.body_3d_scene_dir = "{0}/{1}/hdPose3d_stage1_coco19".format(root_path, sequence)

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

        fpath = self.depth_dir + '/' + kinect_node + '/depthdata.dat'
        im = None
        with open(fpath, 'rb') as s_file:
            # offset is multiplied by 2 because uint16 takes to bytes per number
            a = np.fromfile(s_file, dtype=np.uint16, offset=2*f_size*idx, count=f_size)
            a = a.reshape((im_rows, im_cols))
            im = np.fliplr(a)
        return im

    def load_ground_truth_map(self, kinect_node: str, scene_idx: int, limb: int):
        """
        Load the GT map for the specified limb(s) at index scene_idx from the specified KinectNode.
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
        with open(self.kinect_sync_table, "r") as sync_table_file:
            sync_table = json.load(sync_table_file)
        timestamps = sync_table['kinect']['depth'][kinect_node]['univ_time']
        closest = min(range(len(timestamps)), key=lambda i: abs(timestamps[i] - univ_time))
        return closest


if __name__ == '__main__':
    loader = DataLoader('../data', '160226_haggling1')
    print(loader.nearest_depth_idx(429928.912, 'KINECTNODE6'))
