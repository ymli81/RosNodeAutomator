#!/usr/bin/env python
"""nav.py, A minimal ROS node in Python.
--------------------------------
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
### This file is generated using ros node template, feel free to edit
### Please finish the TODO part
#  Ros imports
import rospy
import roslib; roslib.load_manifest('$PKG$')

## message import format:
##from MY_PACKAGE_NAME.msg import MY_MESSAGE_NAME
#from   $PKG$.msg import  $MSG$

$IMPs$

##############################################################
##   Message Callbacks
$MCBs$

##############################################################
##  Service Callbacks
$SCBs$

##############################################################
# Main Program Code
# This is run once when the node is brought up (roslaunch or rosrun)
if __name__ == '__main__':
  print "Hello world"
# get the node started first so that logging works from the get-go
  rospy.init_node("$RNN$")
  rospy.loginfo("Started template python node: $RNN$.")
##############################################################
##  Service Advertisers
  $SADs$

##############################################################
##  Message Subscribers
  $SUBs$

##############################################################
##  Message Publishers
  $PUBs$

##############################################################
##  Service Client Inits
  $SCIs$


############# Message Object for Publisher ####################
  $MOBs$
  $MSVs$
############# Service Object for client ####################
  $SROs$
  $SVVs$
##############################################################
##  Main loop start
  while not rospy.is_shutdown():
##############################################################
##  Message Publications
    $PBLs$
##############################################################
##  Service Client Calls
    $SCCs$
    
    rospy.loginfo("$RNN$: main loop")
    rospy.sleep(2)
###############################################################
#
# end of main wile loop

