// This file is generated using ros node template, feel free to edit
// Please finish the TODO part 
// $RNN$.cpp
/*
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
-------------------------------- */
#include <ros/ros.h>


// if messages or services used
$IMPs$


/////////////////// Message Callbacks
$MCBs$

/////////////////// Service Callbacks
$SCBs$

int main(int argc, char** argv) {
ROS_INFO("Hello world!");
ROS_INFO("Started template C++ node: $RNN$.");
// init and setup the node
ros::init(argc, argv, "$RNN$");
ros::NodeHandle nh;

//////////////  Message Subscribers & Publishers
$SUBs$
$PUBs$

//////////////  Service Advertisers & Initializers
$SADs$
$SCIs$

////////////// Message Objects
$MOBs$
$MSVs$
////////////// Service objects
$SROs$
$SVVs$


while(ros::ok()) {
  // message publish calls
  $PBLs$
  // service calls
  $SCCs$
  
  ROS_INFO("$RNN$: main loop");
  ros::spinOnce();   // yield to ROS
  ros::Duration(2.0).sleep();
  }

return 0;
}
