Cumulative Notes
================


Related work
------------

 - Hand crafted features: local shape context (pictoral?), HoG, segmentation
 - Pose from 2D images where joint locations are important will have
   problems with different size people, occlusion, and view-dependentness.


Methods
-------

Recurring NN, where we iteratively refine the ouput of the network by
providing increasingly refined confidence maps for each limb. We hope
that this will help the network learn or infer spacial relations
between observed and occluded limbs. By providing the raw depth map as
well, we hope that the network will learn to constrain occluded limbs
to the visual hull behind various objects.

Training the network from the ground up, because we believe the depth
map features can be fundamentally different to those learned by
training on an RGB input.
Whereas we in the 2D case often abstract away the rich image
information and only use sparse 2D joint locations to the network, we
believe that using spacial information around the joint can refine the
3D location in the case of a depth image. (I.e. we can think of the
collection of points along a limb as a vector pointing us in the
direction of the joint we want to locate.)

We envision a 'Depth-view', perpendicular to the current depth image,
where we will store the depth probability for each joint.
Thus if, say the left side of the subject is facing the camera, we
will get high scores for these joints. By including the perpendicular
depth-view in later refinements the network can infer the spacial
positions of the occluded parts.

Top-down approach where we know the basic shape and dimensions of what
we want to detect in the scene. 

On normalized 3D detections:
Many approach the problem (at least in the 2D-3D estimation case) that
we normalize the 3D output by fixing the positions around a central
bone, usually the hip bone.
Some problems with this in our case is that we want contextual
information about the human in the scene in relation to the
robot?.. no, that we lay the groundwork for detecting multiple people
in the same scene, bottom up, so the robot can identify its own 3D
position in relation to every person in the scene. In addition,
tracking joints in the time continuum will be easier by using the
camera coordinate frame, when we later want to do activity recognition
(and possibly refining the joint detections based on earlier frames)

Architectures
-------------