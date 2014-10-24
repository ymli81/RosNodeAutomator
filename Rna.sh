#!/bin/bash 
#   RNA wrapper function for environment init 

##################################################################
##  please edit these according to your setup:

# Ros workspace (already initialized)
rws=/home/blake/Projects/RosNodeAutomator/Ros_ws 

# location you have installed RNA
rnahome=/home/blake/Projects/RosNodeAutomator/RosNodeAutomator
##################################################################

#  Do not edit below this line
#####--------------------------------------------------------------
echo "RNA: refreshing your ROS environment.  This may take a minute."
#  Now we set up Ros
cd $rws
# these dirs may contain old binaries and confusing stuff for RNA
rm -rf devel build
#  now we rebuild them and the binaries
catkin_make > /dev/null 
#  now we setup environment and path variables
source ./devel/setup.bash
#  back to RNA's directory
cd $rnahome
#  OK - let's go
./rna.py $rws

