import json
from data_loader import FilePaths


class DataSequence:
    def __init__(self, root_path, sequence):
        self.paths = FilePaths(root_path, sequence)
        with open(self.paths.kinect_sync_table, 'r') as psync:
            self.ksync = json.load(psync)
        with open(self.paths.kinect_calib, 'r') as pcalib:
            self.kcalib = json.load(pcalib)
        
    def get_depth_image(self, idx, kinect_n):
        body_3d_scene_file = "body3DScene_" + f'{idx:08}' + ".json"
        print(body_3d_scene_file)
