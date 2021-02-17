# Data Loader
The data loader is responsible for loading training data in batches. It provides batches of ground truth and input data for the networks. 

There is no guarantee that a deep network will learn what is a probable pose. Therefore a separate network that we feed with gt and random pose compositions will learn to distinguish what is a probable pose.

### Train in tandem?
If the networks are trained in tandem, This dataloader becomes simpler, as it only needs to provide GT and training data for the one network.


## File formats
The program takes a base 


### Classes

#### DataLoader
The data 



# File formats
ksynctables:
kinect
  color
    kinectnode0
	  index []
	  univ_time []

  depth
    kinectnode0
	  index []
	  univ_time []
	  
synctables:
vga
  index [] # 11999
  univ_time []

hd
  index [] # 14591
  univ_time []
		  
