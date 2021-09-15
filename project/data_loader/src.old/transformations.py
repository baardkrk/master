import numpy as np


def reproject_point(kinect_n: str, coord):
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
