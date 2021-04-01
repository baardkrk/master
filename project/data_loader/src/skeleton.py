"""
Module containing skeleton constants
"""
from enum import Enum


class SkeletonIdxs(Enum):
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
    NECK = (SkeletonIdxs.NECK, SkeletonIdxs.NOSE)
    SPINE = (SkeletonIdxs.NECK, SkeletonIdxs.BODY_CENTER)
    L_CHEEK = (SkeletonIdxs.NOSE, SkeletonIdxs.L_EYE)
    L_HEAD = (SkeletonIdxs.L_EYE, SkeletonIdxs.L_EAR)
    L_CLAVICLE = (SkeletonIdxs.NECK, SkeletonIdxs.L_SHOULDER)
    L_OVERARM = (SkeletonIdxs.L_SHOULDER, SkeletonIdxs.L_ELBOW)
    L_UNDERARM = (SkeletonIdxs.L_ELBOW, SkeletonIdxs.L_WRIST)
    L_HIP = (SkeletonIdxs.BODY_CENTER, SkeletonIdxs.L_HIP)
    L_THIGH = (SkeletonIdxs.L_HIP, SkeletonIdxs.L_KNEE)
    L_SHIN = (SkeletonIdxs.L_KNEE, SkeletonIdxs.L_ANKLE)
    R_CHEEK = (SkeletonIdxs.NOSE, SkeletonIdxs.R_EYE)
    R_HEAD = (SkeletonIdxs.R_EYE, SkeletonIdxs.R_EAR)
    R_CLAVICLE = (SkeletonIdxs.NECK, SkeletonIdxs.R_SHOULDER)
    R_OVERARM = (SkeletonIdxs.R_SHOULDER, SkeletonIdxs.R_ELBOW)
    R_UNDERARM = (SkeletonIdxs.R_ELBOW, SkeletonIdxs.R_WRIST)
    R_HIP = (SkeletonIdxs.BODY_CENTER, SkeletonIdxs.R_HIP)
    R_THIGH = (SkeletonIdxs.R_HIP, SkeletonIdxs.R_KNEE)
    R_SHIN = (SkeletonIdxs.R_KNEE, SkeletonIdxs.R_ANKLE)
