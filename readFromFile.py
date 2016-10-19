'''
Gait recognition system
'''

from pykinect2 import PyKinectV2
import pandas as pd
import math
import numpy as np


# get length of a link between joint0 & joint1
def get_length(joints, joint0, joint1):
    x1 = joints[0, joint0]
    y1 = joints[1, joint0]
    z1 = joints[2, joint0]
    x2 = joints[0, joint1]
    y2 = joints[1, joint1]
    z2 = joints[2, joint1]
    len = ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5
    return len


# get heigh of a person and all links length
def get_all_lengths(joints):
    l = [0 for i in range(19)]
    l[1] = get_length(joints, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck)
    l[2] = get_length(joints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_Neck)
    l[3] = get_length(joints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft)
    l[4] = get_length(joints, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft)
    l[5] = get_length(joints, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft)
    l[6] = get_length(joints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight)
    l[7] = get_length(joints, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowRight)
    l[8] = get_length(joints, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristRight)
    l[9] = get_length(joints, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid)
    l[10] = get_length(joints, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase)
    l[11] = get_length(joints, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_SpineBase)
    l[12] = get_length(joints, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft)
    l[13] = get_length(joints, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_KneeLeft)
    l[14] = get_length(joints, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_SpineBase)
    l[15] = get_length(joints, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight)
    l[16] = get_length(joints, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_KneeRight)
    l[17] = get_length(joints, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft)
    l[18] = get_length(joints, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight)
    # average legs length
    avleg = (l[12] + l[13] + l[15] + l[16]) / 2
    # height
    l[0] = l[1] + l[2] + l[9] + l[10] + avleg + 0.25
    return l

    # get angle between two links
    #          joint1
    #         /
    #   joint0
    #         \
    #          joint2


# get angle between two links
#          joint1
#         /
#   joint0
#         \
#          joint2
def get_angle(joints, joint0, joint1, joint2):
    x0 = joints[0, joint0]
    y0 = joints[1, joint0]
    z0 = joints[2, joint0]
    x1 = joints[0, joint1]
    y1 = joints[1, joint1]
    z1 = joints[2, joint1]
    x2 = joints[0, joint2]
    y2 = joints[1, joint2]
    z2 = joints[2, joint2]

    xd1 = x1 - x0
    yd1 = y1 - y0
    zd1 = z1 - z0

    xd2 = x2 - x0
    yd2 = y2 - y0
    zd2 = z2 - z0

    cosphi = (xd1 * xd2 + yd1 * yd2 + zd1 * zd2) / (
        (xd1 ** 2 + yd1 ** 2 + zd1 ** 2) ** 0.5 * (xd2 ** 2 + yd2 ** 2 + zd2 ** 2) ** 0.5)
    phi = math.acos(cosphi)
    return phi


columns = ['SB', 'SM', 'Nk', 'Hd', 'SL', 'EL', 'WL', 'HL', 'SR', 'ER', 'WR', 'HR', 'HiL', 'KL', 'AL', 'FL', 'HiR', 'KR',
           'AR', 'FR', 'SS', 'HTL', 'TL', 'HTR', 'TR']
df = pd.read_csv('Yulia_4.csv', sep='\t')
s = int(df.shape[0] / 3)
for i in range(0, s):
    joints = df[3 * i:3 * i + 3].as_matrix(columns=columns)
    a = get_all_lengths(joints)
    print(a[0])
