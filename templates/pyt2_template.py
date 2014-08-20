#!/usr/bin/env python
"""nav.py, A minimal ROS node in Python.
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


############# Message Object for Publish ####################
### TODO: Assign values to the message objs
  $MOBs$

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

