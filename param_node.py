# ros node generator parameter file

#  Start by reading and editing this file.   When done, save this and run:
#  > rng.py

# select your build system
#ros_build_system = 'catkin'
ros_build_system = 'rosbuild'

# path to your ROS workspace
#rws = '/home/danying/ROSWorkspace/ros_node_generator/'
#rws = '/home/blake/Projects/Ros2/RosNodeGen/'
rws = '/home/blake/Projects/Ros_node2/RosNodeGen/'
# name of ROS package
pkg = 'my_test_package'
# package text description
pkd = 'A first package for testing the ros node generator'

#########   Personalization
# username  and email for the package.xml file
name = 'FIRSTNAME LASTNAME'
email = 'USER@SYSTEM.COM'
license = '(C) 20XX, All Rights Reserved'

#defaults
lang = 'Python'
direction = 'incoming'

###   MESSAGES

# First, enter name of custom message files you have in ~/package/msg/
# name of .msg file (describing your message)
msg = ''
msg_flag = 0
srv_flag = 0
# name of one of the variables defined in the message (ideally a string)
# if you have more than one variable (such as from multiple .msg files),
# you will need to add those manually

### Services
# name of  .srv file for your service (found in ~/package/srv/)
srv = 'custom_srv'

# location of template files
#file_base = '/home/blake/Dropbox/Ros_node2/'
#file_base = "C:Userslake\Dropbox\Ros_node2"


