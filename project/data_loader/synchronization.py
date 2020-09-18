import numpy as np
import json


KINECT_DEPTH_DIR = "{}/{}/kinect_shared_depth"
KINECT_CALIB_FILE_PATH = "{}/{}/kcalibration_{}.json"
KINECT_SYNC_TABLE_FILE_PATH = "{}/{}/ksynctables_{}.json"
PANOPTIC_CALIB_FILE_PATH = "{}/{}/calibration_{}.json"
PANOPTIC_SYNC_TABLE_FILE_PATH = "{}/{}/synctables_{}.json"


def load(root_path, sequence):
    KINECT_DEPTH_DIR = "{}/{}/kinect_shared_depth".format(root_path, sequence)
    KINECT_CALIB_FILE_PATH = "{}/{}/kcalibration_{}.json".format(root_path, sequence, sequence)
    KINECT_SYNC_TABLE_FILE_PATH = "{}/{}/ksynctables_{}.json".format(root_path, sequence, sequence)
    PANOPTIC_CALIB_FILE_PATH = "{}/{}/calibration_{}.json".format(root_path, sequence, sequence)
    PANOPTIC_SYNC_TABLE_FILE_PATH = "{}/{}/synctables_{}.json".format(root_path, sequence, sequence)


def read_synctable():
    pass


def get_sync_values(timestamp, kinect_n):
    """
    Finds the indices for a set of synchronized kinect depth frames and skeletons.
    @param timestamp: The timestamp we want synchronized values for
    @param kinect_n:  The kinect number we want the indices for
    """
    
    pass
