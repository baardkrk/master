Data perparation of the Panoptic Studio Dataset
=======================================================

- 2 TB of the dataset was downloaded. 
- Pose was translated to the format described.
- Depth frames and pose frames was matched up.
- A frame was sampeled every 4 seconds to get a variety of poses.
- The frames was augmented by
   - rotation
   - random noise 
   - 3D blocks 
   - missing entire regions
   


Tutorial notes
----------------
Some datapoints/skeletons are incomplete. In the training set
Vicon is a readymade mocap system
Because of how the views for the kinect cameras are captured (around 1m above the floor,
and 2.7m tilted down) the model will only learn to recognize poses from these
viewpoints. It is possible that the model will not be able to generalize the recognition
when the view is different. For example if the view is closer to the floor.
(Title suggestion: Cat perspective)

(on why kinect: the panoptic studio is very big, and cannot easily be used in another
place. This means we cannot use it in the field)


VGA, HD, Kinect
531 GB/min

10 kinects
### Synchronization
Total amount of data>
145MB/s
depth 30 fps, 512x424x2 Byte/pixel
IR 512 x 424 x 2 Byte/pixel
Body keypoints, audio

Depth sensor // adding more sensors to capture 3D maps without maps
Placed 1m and 2.7m above the floor, in two rings with diameter 5m and 5 kinects in each
ring. 
- not very accurate 3D reconstruction, because of distance from the subject.
artifacts from different capture times. Was fixed by synchronizing audio signals.
using a gigbit capture node. 
The kinects dont aquire the color and depth frames at exactly the same time.
Has rolling shutter.
Visible in fast motion as disparity artifact.
Calibrated using checkerboard.
Multiple sensors might interfer with each other. (counteracted by spacing out the kinects
as much as possible).

Silent movies underlines our ability to convey intention and ideas via body language.
Nuances are embedded in hands and faces


### Skeleton Reconstruction
Got the skeletons from the openpose method, and assigning voxels in 3D space to the
detected keypoints?

Calibrated Multiview Input -> Fine-grained 2D detection -> Triangulated 3D detections
-- Multiview RGB-D depth maps -> 3D Point Clouds

Not neccessarily the center of the joint. Can have drift. Solved this temporarily by
sorting the detections, and hoping that the 3D triangulation from the most confident
detections are the center for each joint.

#### Hand skeletons
Using synthedic data, didn't work because it is not realistic enough
With multi view systems, it was possible to do triangulation from two or more views. This
means that views where it was difficult to detect the hand keypoints could be inferred
from other views where the keypoints were clearly visible.
using RANSAC for triangulation, in multiple iterations

