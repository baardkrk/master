"""
Module for skeleton related code
"""
import numpy as np
from enum import Enum


class SkeletonJoint(Enum):
    NECK = 0
    NOSE = 1
    BODY_CENTER = 2  # Center of hips
    L_SHOULDER = 3
    L_ELBOW = 4
    L_WRIST = 5
    L_HIP = 6
    L_KNEE = 7
    L_ANKLE = 8
    R_SHOULDER = 9
    R_ELBOW = 10
    R_WRIST = 11
    R_HIP = 12
    R_KNEE = 13
    R_ANKLE = 14
    L_EYE = 15
    L_EAR = 16
    R_EYE = 17
    R_EAR = 18


class SkeletonLimbs(Enum):
    NECK = (SkeletonJoint.NECK, SkeletonJoint.NOSE)
    SPINE = (SkeletonJoint.NECK, SkeletonJoint.BODY_CENTER)
    L_CHEEK = (SkeletonJoint.NOSE, SkeletonJoint.L_EYE)
    L_HEAD = (SkeletonJoint.L_EYE, SkeletonJoint.L_EAR)
    L_CLAVICLE = (SkeletonJoint.NECK, SkeletonJoint.L_SHOULDER)
    L_OVERARM = (SkeletonJoint.L_SHOULDER, SkeletonJoint.L_ELBOW)
    L_UNDERARM = (SkeletonJoint.L_ELBOW, SkeletonJoint.L_WRIST)
    L_HIP = (SkeletonJoint.BODY_CENTER, SkeletonJoint.L_HIP)
    L_THIGH = (SkeletonJoint.L_HIP, SkeletonJoint.L_KNEE)
    L_SHIN = (SkeletonJoint.L_KNEE, SkeletonJoint.L_ANKLE)
    R_CHEEK = (SkeletonJoint.NOSE, SkeletonJoint.R_EYE)
    R_HEAD = (SkeletonJoint.R_EYE, SkeletonJoint.R_EAR)
    R_CLAVICLE = (SkeletonJoint.NECK, SkeletonJoint.R_SHOULDER)
    R_OVERARM = (SkeletonJoint.R_SHOULDER, SkeletonJoint.R_ELBOW)
    R_UNDERARM = (SkeletonJoint.R_ELBOW, SkeletonJoint.R_WRIST)
    R_HIP = (SkeletonJoint.BODY_CENTER, SkeletonJoint.R_HIP)
    R_THIGH = (SkeletonJoint.R_HIP, SkeletonJoint.R_KNEE)
    R_SHIN = (SkeletonJoint.R_KNEE, SkeletonJoint.R_ANKLE)


class Skeleton:
    def __init__(self, coordinates):
        input_coord = coordinates.reshape(19, 4)
        # self.coordinates = np.array([[0.00, 2.34, 0.00, 0.00],
        #                              [0.00, 3.05, 0.00, 0.00],
        #                              [0.00, 0.00, 0.00, 0.00],
        #                              [1.05, 2.34, 0.00, 0.00],
        #                              [1.36, 0.86, 0.00, 0.00],
        #                              [1.36, -0.32, 0.00, 0.00],
        #                              [0.78, 0.00, 0.00, 0.00],
        #                              [1.02, -1.98, 0.00, 0.00],
        #                              [1.02, -3.98, 0.00, 0.00],
        #                              [-1.05, 2.34, 0.00, 0.00],
        #                              [-1.36, 0.86, 0.00, 0.00],
        #                              [-1.36, -0.32, 0.00, 0.00],
        #                              [-0.78, 0.00, 0.00, 0.00],
        #                              [-1.02, -1.98, 0.00, 0.00],
        #                              [-1.02, -3.98, 0.00, 0.00],
        #                              [0.30, 3.30, 0.00, 0.00],
        #                              [0.50, 3.15, 0.00, 0.00],
        #                              [-0.30, 3.30, 0.00, 0.00],
        #                              [-0.50, 3.15, 0.00, 0.00]], dtype=float)
        # Replacing body coordinates where confidence > 0
        # self.coordinates = np.where(np.array([input_coord[:, -1] > self.coordinates[:, -1], ]*4).transpose(),
        #                             input_coord, self.coordinates)
        self.coordinates = coordinates.reshape((-1, 4)).transpose()
        self.edges = []

    def joint_coordinates(self, joint: SkeletonJoint):
        """Returns a column-vector on the format [[x],[y],[z]]"""
        return self.coordinates[:3, joint.value].transpose()
