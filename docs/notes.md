Convolutional Neural networks
==========================
In a fully connected layer every neuron in layer $n$ is connected to
every neuron in the next layer, $n + 1$. This means that if we have
$i$ neurons in layer $n$ and $j$ neurons in layer $n + 1$ we will have
a total $i j$ number of weights between the layers!

However, in convolutional neural networks we have a filter between the
layers. The size of layer $n + 1$ is then decided by how large the
layer $n$ is, and the size of 


Lets think about CNNs in depth images. How many layers do we need to
preform an understanding of the image? How small should the details we
look at be?
In a depth image, the error at a distance will be based on the sensor,
so we might not be interested in details that are quite small. 

The challenge is that it is not a direct classification problem. We
want the network to produce an output vector which contains a variable
number of peoples joint positions in 3d coordinates irt. the camera.

we could turn it into a classification problem, by defining a cone of
caring, where we have a finite number of voxels that either contains a
joint, or don't.

In the open pose project we have a finite map that contains the
probabilities for a joint to be in coordinate (x,y). We could do the
same in the depth map, where we take the depth value at that position,
and say it is the z-value in the post processing of the results.

However, we would also like to use this information about the
connected joints, to infer the position of occluded joints, so we can
get a complete skeleton.

CNNs in 3D
-----------
In 2D we can look for features that rely on differing contrast between regions. For
example, we can detect an edge where there is a sudden change between light and
dark. Combining this, we can find larger structures, such as lines, blobs, or regions. All
of these are 3D features.

However, when we get a 3D depth image as input, we don't always have as clearly defined
contrast between objects. We can therefore imagine that we need features such as smooth
planes, cylinders, boxes, spheres, rough surfaces (a keyboard for example). 

This is why we think it is better to train a network from scratch, instead of using
transferlearning from a network that has been trained on 2D images. - The desired features
are fundamentally different.


On intermediate pose evaluation
-----------------------------------
After some number of stages of joint predictions in the network, we try to evaluate the
pose in and of itself. To do this, we feed it the ground truth pose, as well as the
predicted skeleton.

Human Pose Estimation
-----------------------
Traditionally, this problem has been approached in one of two ways. One is top-down,
meaning we first try to find an instance of a human being in the scene, then we try to
find the pose for each person we find in this first pass. We could for example first look
for faces using *Haar Cascades* and then for each face we find, go looking for evidence as
to where the rest of the joints are. However, using this technique, the time spent
processing will increase proportionally to the number of faces found in the image.

Another way is to use a bottom-up approach. Here, we try to find all joints/landmarks
first, *then* we match them up to create skeletons. This 


LINKS
=========
- [ ] https://medium.com/@iamvarman/how-to-calculate-the-number-of-parameters-in-the-cnn-5bd55364d7ca
      
- [ ] https://en.wikipedia.org/wiki/Cross-correlation
      
- [ ] https://victorzhou.com/blog/intro-to-cnns-part-1/
      
- [ ] https://towardsdatascience.com/training-a-convolutional-neural-network-from-scratch-2235c2a25754
      
- [ ] https://www.youtube.com/watch?v=AQirPKrAyDg
      
- [ ] https://datascience.stackexchange.com/questions/18341/how-are-weights-represented-in-a-convolution-neural-network
      


- [ ] https://github.com/deepmind/Temporal-3D-Pose-Kinetics
      
- [ ] https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf
      
- [ ] https://heartbeat.fritz.ai/a-2019-guide-to-human-pose-estimation-c10b79b64b73
      Top-down: low-to-high resolutions. Starts by localizing individual people using a
      bounding-box object detection. Then we estimate the pose of each individual person.
	  Bottom-up: high-to-low resolutions. Localizing identity-free semantic instances and
      then grouping them into person instances.
- [ ] https://www.tandfonline.com/doi/full/10.1080/09298215.2020.1711778
      
- [ ] https://www.analyticsvidhya.com/blog/2019/10/building-image-classification-models-cnn-pytorch/
	  
- [ ] https://towardsdatascience.com/step-by-step-vgg16-implementation-in-keras-for-beginners-a833c686ae6c
- [ ] https://www.domos.no/news-updates/running-machine-learning-with-low-resource-understanding-the-process
      
- [ ] https://medium.com/@youebned/notes-on-training-vgg16-7ae99689fd5
      
- [ ] https://arxiv.org/pdf/1905.04266.pdf
      
- [ ] https://arxiv.org/abs/1910.13911
      
- [ ] https://arxiv.org/pdf/1910.13911.pdf
      
- [ ] https://www.quora.com/What-is-the-VGG-19-neural-network
      
- [ ] https://ieeexplore.ieee.org/document/8593383
      
- [ ] https://forums.fast.ai/t/vgg16-extract-4096-feature-vector/5513
      
- [ ] https://arxiv.org/pdf/1605.07678.pdf
      
- [ ] https://pytorch.org/tutorials/beginner/nlp/pytorch_tutorial.html
      
- [ ] https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
      
- [ ] https://discuss.pytorch.org/t/check-gradient-flow-in-network/15063
      
- [ ] https://discuss.pytorch.org/t/how-to-check-for-vanishing-exploding-gradients/9019
      
- [ ] https://machinelearningmastery.com/how-to-fix-vanishing-gradients-using-the-rectified-linear-activation-function/
      
- [ ] https://algorithmia.com/blog/convolutional-neural-nets-in-pytorch
      
- [ ] https://arxiv.org/abs/1803.08225
      
- [ ] https://arxiv.org/pdf/1907.06922.pdf
      
- [ ] https://www.mn.uio.no/ifi/english/research/groups/robin/studies/how-to-write-master-thesis-torresen.pdf
      

- [ ] https://www.oslo.kommune.no/getfile.php/13139280-1466695241/Tjenester%20og%20tilbud/Politikk%20og%20administrasjon/Statistikk/Oslohelsa_kortversjon.pdf
      
