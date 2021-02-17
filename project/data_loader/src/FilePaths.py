class FilePaths:
    def __init__(self, root_path, sequence):
        self.depth_dir = "{0}/{1}/kinect_shared_depth".format(root_path, sequence)
        self.kinect_calib = "{0}/{1}/kcalibration_{1}.json".format(root_path, sequence, sequence)
        self.kinect_sync_table = "{0}/{1}/ksynctables_{1}.json".format(root_path, sequence)
        self.panoptic_calib = "{0}/{1}/calibration_{1}.json".format(root_path, sequence)
        self.panoptic_sync_table = "{0}/{1}/synctables_{1}.json".format(root_path, sequence)
        self.body_3d_scene_dir = "{0}/{1}/hdPose3d_stage1_coco19".format(root_path, sequence)
