# ros node generator parameter file
"""--------------------------------
(C) 2014, Biorobotics Lab, Department of Electrical Engineering, University of Washington
This file is part of RNA - The Ros Node Automator.

    RNA - The Ros Node Automator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RNA - The Ros Node Automator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with RNA - The Ros Node Automator.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------
"""
#  Start by reading and editing this file.   When done, save this and run:
#  > rng.py

# select your build system
#ros_build_system = 'catkin'
ros_build_system = 'ros_build'

# path to your ROS workspace
rws = '/home/danying/ROSWorkspace/ros_node_generator/'
#rws = '/home/blake/Projects/Ros2/RosNodeGen/'
#rws = '/home/blake/Projects/Ros_node2/RosNodeGen/'
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


