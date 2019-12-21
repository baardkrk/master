Robotic Operating System
========================

The Robotic Operating System (ROS) is basically a program that interconnects different
programs with separate functions, through the ROS core. It allows us to have a unified way
of sending data between the different programs (also called ROS nodes). The ROS keeps
track of timing between the nodes, and how everything is connected together.

Sensors
-------
A robot usually consists of different sensors and actuators. In ROS we like to create one
node for one type of sensor. In a way, the node will be like a driver for that sensor in
ROS (although that analogy isn't perfect, we still need the actual driver for the
hardware, and the node can be written to directly interface with the user.)

We have some standard sensor information formats we use in ROS. These are nicely collected
in the `sensor_msgs` (sensor messages) package, which includes:

| - BatteryState     	     | - Joy     		      | - PointCloud
| - CameraInfo		     | - JoyFeedback	      	      | - PointCloud2
| - ChannelFloat32	     | - JoyFeedbackArray	      | - PointField
| - CompressedImage	     | - LaserEcho	      	      | - Range
| - FluidPressure	     | - LaserScan	     	      | - RegionOfInterest
| - Illuminance		     | - MagneticField	      	      | - RelativeHumidity
| - Image		     | - MultiDOFJointState   	      | - Temprature
| - Imu			     | - MultiEchoLaserScan 	      | - TimeReference
| - JointState		     | - NavSatFix	      	      

More information on each message type can be found by following the link to the (*API
reference*)[1].

In ROS we also have something called *services*. Services can set certain variables on a
node. The messages define a format in which we transmit information. This is stored in the
`.msg` files.




[1]: http://docs.ros.org/melodic/api/sensor_msgs/html/index-msg.html

