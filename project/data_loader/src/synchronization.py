import numpy as np
import json

"""
The synchronization program takes a body3DScene-index, and provides the corresponding 
timestamp for each kinect.
"""

def get_kinect_idx(body_3d_index, kinect_n):
    """
    Finds the index that corresponds to the given body3DScene index for a given
    kinect. This index can be used to find the appropriate depth-frame from 
    the kinects depthdata.dat file. 
    @param body_3d_index: The body3DScene index we want to find the kinect-index for
    @param kinect_n:      The kinect we want
    @return  The kinect-index corresponding to the body3DScene-index.
    """
    

def read_synctable():
    pass


def get_sync_values(timestamp, kinect_n):
    """
    Finds the indices for a set of synchronized kinect depth frames and skeletons.
    @param timestamp: The timestamp we want synchronized values for
    @param kinect_n:  The kinect number we want the indices for
    """
    
    pass
