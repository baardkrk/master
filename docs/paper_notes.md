3D human pose estimation from 2D images
=======================================

3D Human Pose Estimation with Relational Networks
-------------------------------------------------
https://arxiv.org/pdf/1805.08961.pdf

 - 3D pose from 2D image
 - Pairs of features from each body part, average is used to estimate 3D pose 
 - Divides into deformable groups: arms, legs, head, torso
 - Average the features from each group to generate feature vectors used in 3D pose
   regression
 - Randomly drops pairs of features during training -> simulates missing joint groups
   (Simulates occlusion of entire group?)
 - Uses 2D observations of joint locations as input to the 3D location mapping.
 - 

 - Finding joint location for each person in the scene separatley
 - Gets a normalized output, surpressing information about height
 - It will still train on images where all joints are labeled, thus it may not extrapolate
 - Uses Procrustes superimposition to validate the pose information. (I.e. scale ->
   translate -> rotate) (Called Protocol 2 in the paper)
 - Protocol 1 only aligns the 'root' joints of the estimated pose and the GT to calculate
   error.
 - Does not handle missing joints from different groups simultaneously well


Bayesian Image Based 3D Pose Estimation
---------------------------------------
https://link.springer.com/chapter/10.1007/978-3-319-46484-8_34


A simple yet effective baseline for 3d human pose estimation
------------------------------------------------------------
https://arxiv.org/pdf/1705.03098.pdf

 - Uses a feedforward network
 - Depth from single image, see references [12,26,34,39]
 - Top-down inspired, assuming the shape of the human in the scene
 - Sparse 2D projections used to 'lift' 3D pose
 - Using Hourglass Network to find 2D locations which are fed to the 'lifting' net
 - See reference [23] for binary decision tree about split between joint and parent
 - See [2,7,36,49,55,56] for sparse combinations (think this is related to the
   'dictionary' method described in 'relational networks'
 - Regresses to probability distributions in 3D space per joint (Not regressing multiple
   times to refine could be a weakness in this work)
 - Simple approach, uses only 2D positions ((lin->batch->relu->dropout x2)->rescon)x2
 - Fixed global space according to root joint (Hip is standard practice)

 - Exellent, and easy-to follow paper


Learning to Estimate 3D Human Pose and Shape from a Single Color Image
----------------------------------------------------------------------
https://arxiv.org/pdf/1805.04092.pdf

 - Rendering 3D meshes based on silhouette and predicted skeleton to further refine output
 - Using ConvNets
 - Estimating whole 3D mesh, not just skeleton bones. (maybe somewhat akin to DensePose?)
 - Making two networks, which produce 2D keypoints and silhouettes, which is then combined
   by a third network that produces the poses.
   

3D Human Pose Estimation Using Convolutional Neural Networks with 2D Pose Information
-------------------------------------------------------------------------------------
https://arxiv.org/pdf/1608.03075.pdf


3D Human Pose Estimation from Monocular Images with Deep Convolutional Neural Network
-------------------------------------------------------------------------------------
http://visal.cs.cityu.edu.hk/static/pubs/conf/accv14-3dposecnn.pdf


Image-based Synthesis for Deep 3D Human Pose Estimation
-------------------------------------------------------
https://arxiv.org/pdf/1802.04216.pdf

 - clustering data into a large number of pose classes
 - point about 3d datasets not available outside controlled evnironments with markerless
   (CMU Panopric Dataset, MARCOnI Dataset) or marker-based (HumanEva, Human 3.6M, Berkeley
   MHAD) tracking. -> overfitting to marker-suits
 - Synthesizing multiple views by 'copying' information for each joint from different
   samples. (focus on local photorealism than global realism)
 - CNN based approach!
 - Classifies to K pose classes.
 - (why not per limb, as in the synthesizing example, so more variation can be made?)
 

3D Human Pose Estimation in the Wild by Adversarial Learning
------------------------------------------------------------
https://arxiv.org/abs/1803.09722


Coarse-to-Fine Volumetric Prediction for Single-Image 3D Human Pose
-------------------------------------------------------------------
https://arxiv.org/abs/1611.07828


Latent structured models for human pose estimation
--------------------------------------------------
http://vision.imar.ro/human3.6m/ils_iccv11.pdf


3D Human Pose Estimation from 3D depth maps
===========================================

Accurate 3D Pose Estimation From a Single Depth Image
-----------------------------------------------------
https://www.inf.ethz.ch/personal/pomarc/pubs/YeICCV11.pdf

 - 


3D human pose estimation from depth maps using a deep combination of poses
--------------------------------------------------------------------------
https://arxiv.org/pdf/1807.05389.pdf


Estimation Human 3D Pose from Time-of-Flight Images Based on Geodesic Distances and
Optical Flow
-----------------------------------------------------------------------------------
http://far.in.tum.de/pub/schwarz2011fg/schwarz2011fg.pdf


3D Convolutional Neural Networks for Efficient and Robust Hand Pose Estimation from Single
Depth Images
------------------------------------------------------------------------------------------
https://ieeexplore.ieee.org/document/8100085


Robust 3D Hand Pose Estimation in Single Depth Images: from Single-View CNN to Multi-View
CNNs
-----------------------------------------------------------------------------------------
https://arxiv.org/abs/1606.07253


Home 3D Body Scans from Noisy Image and Range Data
--------------------------------------------------
http://files.is.tue.mpg.de/black/papers/KinectICCV2011.pdf


Real-Time Human Pose Recognition in Parts from Single Depth Images
------------------------------------------------------------------
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/BodyPartRecognition.pdf

 - uses no temporal infromation (so frame by frame)
 - does per pixel classification based on large varied dataset
 - (clothing, body shape and so on could screw up our experiment, because of small smaple
   size)
 - deep randomized decision forest classifier (per pixel)
 - using a mean-shift approach for proposing joint locations (weighted gaussian kernel)
 - surface of body detections, so a learned z parameter is used to push each proposal
 - approaces pose estimation as object recognition problem using intermedieate body part
   representations. 
 - learned occlusion handling
 - trains on synthetic datasets (this would be cool..)
 - also evaluates against real and synthetic datasets
 - avoid overfitting because of dataset size 
 - discards similar (~5cm) poses from the dataset
 - features are created by looking at nearby/offset pixels
 - simple operations lead to high speed (200 fps) but, could be low accuracy

 - btw, exellent explanation on descision trees/forests
 - users mostly +-120 degrees away from camera.
 - uses the original Kinect Structured Light sensor



2D Human Pose Estimation
========================

Stacked Hourglass Networks for Human Pose Estimation
----------------------------------------------------
https://arxiv.org/pdf/1603.06937.pdf

 - Regressing to 2D joint probability heatmaps


DeepPose: Human Pose Estimation via Deep Neural Networks
--------------------------------------------------------
https://arxiv.org/pdf/1312.4659.pdf

 - DNN regressors to find the 2D locations of anatomical landmarks (joints)
 - 7 layers convolutional network
 - Defines the pose from a normalized body pose vector, all joints are defined from the
   center of a bounding box around the body. (Translation by box center and scaling by box
   size)
 - Introduces the cascade of classifiers as seen in CPM eeeh not quite. This looks at a
   smaller and smaller part of the image to refine the location
 - fixed input (220x220) so, the network only learns pose properties at coarse
   scale. Could this be a good property where we can send in a laplacian pyramid of the
   image, and evaluate at the different levels, if that goes faster/we need a shallower
   network?
 - finds bounding boxes around each individual joint after initial step, and regresses/
   refines them iterativeley
 - This means that we, in each refined step work on the full image, meaning the subsequent
   pose regressors obtain high resoulution images, and can learn features for fine scales.

 - *very* thoroughly explains what is done and the implementation


DeepCut: Joint Subset Partition and Labeling for Multi Person Pose Estimation
-----------------------------------------------------------------------------
https://arxiv.org/pdf/1511.06645.pdf

 - 


Human Pose Estimation with Iterative Error Feedback
---------------------------------------------------
https://arxiv.org/pdf/1507.06550.pdf


Pictoral Structures for Object Recognition
------------------------------------------
http://www.cs.cornell.edu/~dph/papers/pictorial-structures.pdf


Strong Appearance and Expressive Spatial Models for Human Pose Estimation
-------------------------------------------------------------------------
https://www.is.mpg.de/uploads_file/attachment/attachment/148/pishchulin13iccv.pdf


Exploring the Spatial Hierarchy of Mixture Models for Human Pose Estimation
---------------------------------------------------------------------------
https://yuandong-tian.com/eccv_pose_est_camera_ready.pdf


Human Pose Estimation using Body Parts Dependent Joint Regressors
-----------------------------------------------------------------
https://www.cv-foundation.org/openaccess/content_cvpr_2013/papers/Dantone_Human_Pose_Estimation_2013_CVPR_paper.pdf


DensePose: Dense Human Pose Estimation In The Wild
--------------------------------------------------
https://arxiv.org/pdf/1802.00434.pdf


Using Linking Features in learning Non-parametric Part Models
-------------------------------------------------------------
http://www.wisdom.weizmann.ac.il/~leonidk/publications/papers/linking_features_eccv12.pdf


Multiple Tree Models for Occlusion and Spacial Contraints in Human Pose Estimation
----------------------------------------------------------------------------------
https://www.cs.sfu.ca/~mori/research/papers/wang_eccv08.pdf


Articulated Part-based Model for Joint Object Detection and Pose Estimation
---------------------------------------------------------------------------
http://vhosts.eecs.umich.edu/vision//papers/Sun_ICCV11_PID2005385.pdf


Panoptic Studio: A Massively Multiview System for Social Interaction Capture
----------------------------------------------------------------------------
https://arxiv.org/pdf/1612.03153.pdf


Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields
-------------------------------------------------------------------
https://arxiv.org/pdf/1611.08050.pdf

 - Introduces a set of 2D vector fields that encode the location and orientation of limbs
   in an image
 - Uses VGG-19 to produce feature maps whcih is input to the subsequent networks
 - The Part Affinity fields (2D vectors -- we could do this in 3D, no?)
 - Post processing using bipartite matching and line integrals over the PAFs to weight the
   different edges
 - Also decomposes the matching problem into smaller bipartite graph problems, so
   processing will be easier


Convolutional Pose Machines
---------------------------
https://arxiv.org/pdf/1602.00134.pdf

 - Focuses on long-range dependencies between variables in structured prediction tasks
 - Sequential conv archt that directly operate on belief maps from prev stages
 - replenishing gradients by intermediate supervision
 - completley diffrentieable, allwoing for end to end training of the network
 - with varying receptive field sizes it was found that the network encodes long range
   information relating the different anatomical landmarks
 - stride 8 preformed well
 - 

 - How is data preprocessing done?


Pose Machines: Articulated Pose Estimation via Inference Machines
-----------------------------------------------------------------
https://www.ri.cmu.edu/pub_files/2014/7/poseMachines.pdf


Efficient Object Localization Using Convolutional Networks
----------------------------------------------------------
https://cims.nyu.edu/~tompson/others/tompson_cvpr15.pdf
https://arxiv.org/pdf/1411.4280.pdf


2D Human Pose Estimation: New Benchmark and State of the Art Analysis
---------------------------------------------------------------------
https://ieeexplore.ieee.org/document/6909866





Human Activity Recognition
==========================

A Survey on Human Motion Analysis from Depth Data
-------------------------------------------------
http://files.is.tue.mpg.de/jgall/tutorials/slides/motionanalysis_DRAFT.pdf


Human Activity Recognition and Pattern Discovery
------------------------------------------------
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3023457/


A Survey on Human Activity Recognition using Wearable Sensors
-------------------------------------------------------------
https://ieeexplore.ieee.org/document/6365160


Human Activity Recognition on Smartphones Using a Multiclass Hardware-Friendly Support
Vector Machine
--------------------------------------------------------------------------------------
https://link.springer.com/chapter/10.1007/978-3-642-35395-6_30


Human activity recognition from 3D data: a review
-------------------------------------------------
https://www.sciencedirect.com/science/article/abs/pii/S0167865514001299


Tracking a Subset of Skeleton Joints: An Effective Approach towards Complex Human Activity
Recognition
------------------------------------------------------------------------------------------
https://www.hindawi.com/journals/jr/2017/7610417/


A Human Activity Recognition System Using Skeleton Data from RGBD Sensors
-------------------------------------------------------------------------
https://www.hindawi.com/journals/cin/2016/4351435/


Unstructured Human Activity Detection from RGBD Images
------------------------------------------------------
http://jaeyongsung.com/paper/unstructured_human_activity_learning.pdf
https://ieeexplore.ieee.org/abstract/document/6224591





On Convolutional Neural Networks
================================


Learning Message-Passing Inference Machines for Structured Prediction
---------------------------------------------------------------------
https://www.ri.cmu.edu/pub_files/2011/6/ross_cvpr_11.pdf


Very Deep Convolutional Networks for Large-Scale Image Recognition
------------------------------------------------------------------
https://arxiv.org/abs/1409.1556


ImageNet Classification with Deep Convolutional Neural Networks
---------------------------------------------------------------
https://dl.acm.org/citation.cfm?id=3065386

 - Dataset: 1.2M highres img. to 1000 different classes (ImageNet LSVRC-2010)
 - 5 conv layers, followed by max-pooling, three FC layers and a final 1000-way softmax
 - Uses dropout as regularization
 - Shows how fast ReLU's are
 - Introduces Local Response normalization (brightness normalization)
 - Error rates and overfitting are reduced by overlapp pooling (s=2,z=3)
 - Observed color agnosticity in one gpu vs the other, probably because of the split
   architecture.



Machine Learning Techniques
===========================

Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate
Shift
--------------------------------------------------------------------------------------
https://arxiv.org/pdf/1502.03167v3.pdf


3D Convolutional Neural Networks for Classification of Functional Connectomes
-----------------------------------------------------------------------------
https://arxiv.org/pdf/1806.04209.pdf


Understanding the difficulty of training deep feedforward neural networks
-------------------------------------------------------------------------
http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf


Deep Residual Learning for Image Recognition
--------------------------------------------
https://arxiv.org/pdf/1512.03385.pdf


Identity Mappings in Deep Residual Networks
-------------------------------------------
https://arxiv.org/pdf/1603.05027.pdf


Dropout: A Simple Way to Prevent Neural Networks from Overfitting
-----------------------------------------------------------------
http://jmlr.org/papers/volume15/srivastava14a.old/srivastava14a.pdf


Adam: A Method for Stochastic Optimization
------------------------------------------
https://arxiv.org/abs/1412.6980


Rectified Linear Units Improve Restricted Boltzmann Machines
------------------------------------------------------------
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.165.6419&rep=rep1&type=pdf


Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet
Classification (Kaiming initialization)
----------------------------------------------------------------------------
https://arxiv.org/abs/1502.01852


Computer Vision Papers/refrences
================================

BRIEF: Binary Robust Independent Elementary Features*
-----------------------------------------------------
https://www.cs.ubc.ca/~lowe/525/papers/calonder_eccv10.pdf




Other
=====

A simple neural network module for relational reasoning
-------------------------------------------------------
https://arxiv.org/abs/1706.01427


Understanding the Effective Receptive Field in Deep Convolutional Neural Networks
---------------------------------------------------------------------------------
https://arxiv.org/pdf/1701.04128.pdf




Notes
=====

Activation functions
--------------------

Often used, all nonlinear:
      f(x) = tanh(x)		(Tanh, saturating)     
      f(x) = (1 + e^(-x))^(-1)	(Sigmoid, saturating)  
      f(x) = max(0,x)		(Rectified Linear Unit, ReLU)
