import numpy as np
import json
import matplotlib.pyplot as plt
#%matplotlib inline
plt.rcParams['image.interpolation'] = 'nearest'

# Setup paths
data_path = 'data/'
seq_name = '160226_haggling1'

hd_skel_json_path = data_path+seq_name+'/hdPose3d_stage1_coco19/'
colors = plt.cm.hsv(np.linspace(0, 1, 10)).tolist()

# Load camera calibration parameters (for visualizing cameras)
with open(data_path+seq_name+'/calibration_{0}.json'.format(seq_name)) as cfile:
    calib = json.load(cfile)

# Cameras are identified by a tuple of (panel#,node#)
cameras = {(cam['panel'],cam['node']):cam for cam in calib['cameras']}

# Convert data into numpy arrays for convenience
for k,cam in cameras.items():    
    cam['K'] = np.matrix(cam['K'])
    cam['distCoef'] = np.array(cam['distCoef'])
    cam['R'] = np.matrix(cam['R'])
    cam['t'] = np.array(cam['t']).reshape((3,1))


# Choose only HD cameras for visualization
hd_cam_idx = zip([0] * 30,range(0,30))
hd_cameras = [cameras[cam].copy() for cam in hd_cam_idx]


from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev = -90, azim=-90)
#ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')
ax.axis('auto')

# Draw selected camera subset in blue
# for cam in hd_cameras:
#     cc = (-cam['R'].transpose()*cam['t'])
#     ax.scatter(cc[0], cc[1], cc[2], '.', color=[0,0,1])


# Select HD Image index
hd_idx = 400


'''
## Visualize 3D Body
'''
# Edges between joints in the body skeleton
body_edges = np.array([[1,2],[1,4],[4,5],[5,6],[1,3],[3,7],[7,8],[8,9],[3,13],[13,14],[14,15],[1,10],[10,11],[11,12]])-1

try:
    # Load the json file with this frame's skeletons
    skel_json_fname = hd_skel_json_path+'body3DScene_{0:08d}.json'.format(hd_idx)
    with open(skel_json_fname) as dfile:
        bframe = json.load(dfile)

    # Bodies
    for ids in range(len(bframe['bodies'])):
        body = bframe['bodies'][ids]
        skel = np.array(body['joints19']).reshape((-1,4)).transpose()

        for edge in body_edges:
            ax.plot(skel[0,edge], skel[1,edge], skel[2,edge], color=colors[body['id']])

except IOError as e:
    print('Error reading {0}\n'.format(skel_json_fname)+e.strerror)

plt.show()
