// This file is generated using ros node template, feel free to edit
// Please finish the TODO part 
// $RNN$.cpp

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

////////////// Message Object for Publish
$MOBs$

////////////// TODO: Assign values to the message objs



while(ros::ok()) {
  $PBLs$
  $SCCs$
  
  ROS_INFO("$RNN$: main loop");
  ros::spinOnce();   // yield to ROS
  ros::Duration(2.0).sleep();
  }

return 0;
}
