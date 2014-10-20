#!/usr/bin/env python
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
import os, sys
from readmsgsrv import ros_files
from rospackage import ros_package
from rosnode import ros_node
import rospkg

print ('Welcome to ROS Node Automator  *****')
print ('Please answer a few questions about your new node:')

########################### Get System Setup #############################
with open('param_node.py') as pfile:
  initcode = pfile.readlines()
for line in initcode:
  exec (line)


######################## Check ROS workspace #########################

if not os.path.exists(rws):
  print ('  Apparently your ROS workspace '+rws+' does not exist yet.')
  print ('       ... Please create it or check your param_node.py file')
  exit(0)
  
  
####################### Query user for details ###########################
##  Package name ##
pkg = raw_input('Enter your package name: default [' + pkg +']:') or pkg
my_rospkg = ros_package(pkg,rws,ros_build_system)
my_rospkg.create_package_folder()


## test for proper ROS environment setting of the package using rospkg library ##
try:
  print 'Testing ros core setup.'
  ros_root = rospkg.get_ros_root() 
  rp = rospkg.RosPack() 
  path = rp.get_path(pkg)
  print 'Your package path is: '+ path
  print 'Ros system working properly!'
except Exception as exc:
  name_of_exception = type(exc).__name__
  print 'Could not "rospack.get_path" of package: '+pkg
  print '  in ROS workspace: '+rws
  print 'Ros exception: '+name_of_exception
  print '\n\nPlease check your ROS environment'
  print ' 1) Is roscore running?'
  print ' 2) did you already create and initialize your package (catkin_create_pkg or roscreate-pkg)'
  print ' 3) in your Ros-workspace: catkin_make ';
  print ' 4) in your RNA dir, source <RosWs>/devel/setup.bash'
  print ''
  print 'Test your ros setup:'
  tmpstr = pkg[:3]
  print ' >rosrun '+tmpstr+'<tab> '
  print ' should autocomplete to '
  print ' >rosrun '+pkg
  exit(0)


## Node name ##
node_name = pkg + '_node'
node_name = raw_input('Enter your new node name: ['+node_name+ ']: ') or node_name
while my_rospkg.check_node_name(node_name):
  node_name = raw_input('ROS node ['+node_name+'] exists in package '+pkg+', enter another name:') or node_name

## Language ##
lang = raw_input('Enter your language: [Python or C++]: ') or lang
while 1 :
  if lang[0]=='C' or lang[0]=='c':
    lang = 'C++'
    break
  elif lang[0]=='P' or lang[0]=='p':
    lang = 'Python'
    break
  else:
    lang = raw_input('Unknown Language, please re-enter the language type: [Python or C++]: ') or lang

rosnd = ros_node(node_name,lang,my_rospkg.package_path)


########################################################################################
#
#                           Get and process the Messages
rep = ''
while 1:  
  resp = raw_input('Do you want to add a'+rep+' message? (y for yes, n/CR for no): ') or -1
  rep = 'nother'
  if (resp == -1) or (resp[0]=='n') or (resp[0] == 'N'):
    break
  direction = raw_input('[P]ublish or [S]ubscribe?: ')
  while 1 :
    if direction[0]=='P' or direction[0]=='p':
      direction = 'publish'
      break
    elif direction[0]=='S' or direction[0]=='s':
      direction = 'subscribe'
      break
    else:
      direction = raw_input('Unknown message direction, enter [P]ublish or [S]ubscribe?:') or direction

# get dependent package from input
  pkgd = pkg
  pkgd = raw_input('Enter the package that contains your message ['+pkgd+']: ') or pkgd

  # get the files for the desired package
  a = ros_files(pkgd)
  a.get_package_path()

#if the dependent package does not exist or the dependency is same as the user package --> create/use a custom .msg file in user package
  if not a.package_found and pkgd==pkg:     
    a.set_package_path(my_rospkg.package_path)
  a.list_msgs()
  msg = ''
  idx = 0
  if a.message_list:  # we have found messages
     idx = raw_input('Select message by number: ')
     idx = int(idx)   #  careful: a python 'feature' is that entering a decimal ('2.0') will break this!
  else:   # no messages found
    idx = 0
    if direction == 'subscribe':
      print('You cannot subscribe to nonexisting message')
      direction ='unknown'

  # now we have some message
  if direction == 'publish':
    if (not idx > len(a.message_list)) and (idx >0) and (a.message_list): # we have a valid message selection
      msg = a.message_list[idx-1]
      end = msg.find('.msg')
      msg = msg[0:end]
      custom_msg_flag = 0
      my_rospkg.msg_flag = 1
    else:
      msg = raw_input('Empty or unknown message list, creating a custom message in package '+ pkg+'. Name your message: ')
      pkgd = pkg
      my_rospkg.msg_flag = 1
      custom_msg_flag = 1

   #############################################################
   #
   #     Get and process the topic for each publisher message
    topic = msg+'_topic'
    topic = raw_input('Enter the topic of your message ['+topic+']: ') or topic
    if custom_msg_flag:
      my_rospkg.edit_custom_msg()
      my_rospkg.gen_msg(msg)
    rosnd.add_publisher(pkgd,msg,topic)

  elif direction == 'subscribe':
    while idx > len(a.message_list):
      idx = raw_input('Unknown message, please re-enter the index of message you want to '+direction) or idx
      idx = int(idx)
    msg = a.message_list[idx-1]
    end = msg.find('.msg')
    msg = msg[0:end]

   #############################################################
   #
   #     Get and process the topic for each subscriber message
    topic = msg+'_topic'
    topic = raw_input('Enter the topic of your message ['+topic+']: ') or topic
    cb_name =  topic+'_cb'
    cb_name = raw_input('Enter the name of your message callback function: default ['+cb_name+']') or cb_name
    rosnd.add_subscriber(pkgd,msg,topic,cb_name)

  # this might be a dependency on own package (check?)
  my_rospkg.add_dependency(pkgd)



########################################################################################
#
#                           Get and process the Services
rep = ''
while 1:
  resp = raw_input('Do you want to add a'+rep+' service? (y for yes, n/CR for no) ') or -1
  rep = 'nother'
  if (resp == -1) or (resp[0]=='n') or (resp[0] == 'N '):
    break
  direction = raw_input('[C]lient or [S]erver?: ')
  while 1 :
    if direction[0]=='C' or direction[0]=='c':
      direction = 'client'
      break
    elif direction[0]=='S' or direction[0]=='s':
      direction = 'server'
      break
    else:
      direction = raw_input('Unknown service handle, [C]lient or [S]erver?: ') or direction

  pkgd = pkg
  pkgd = raw_input('Enter the package that contains your service, default package: [ '+pkgd+' ]') or pkgd
  a = ros_files(pkgd)
  a.get_package_path()

#if the dependent package does not exist or the dependency is same as the user package --> create/use a custom .srv file in user package
  if not a.package_found and pkg==pkgd:
    a.set_package_path(my_rospkg.package_path)
  a.list_srvs()
  srv = ''
  idx = 0
  if a.service_list:
     idx = raw_input('Select service by number: ')
     idx = int(idx)  #  careful: a python 'feature' is that entering a decimal ('2.0') will break this!
  else:
     if direction == 'server':
       print('Sorry- I cant yet work with a nonexisting service type')
       print('Please manually create your service file in '+my_rospkg.package_path+'/srv ')
       print(' ... then restart rna.py')
       exit(0)

  if direction == 'client':
    if not idx > len(a.service_list) and idx>0 and a.service_list :  # we found existing service file
      srv = a.service_list[idx-1]
      end = srv.find('.srv')
      srv = srv[0:end]
      my_rospkg.srv_list.append(srv + '.srv ')   # can this cause CMakeLists to come out right?
      custom_srv_flag = 0
    elif (idx > len(a.service_list) or idx == 0) and a.service_list:
      srv = raw_input('Unknown service type, creating a custom service type in package '+ pkg+'. Name your service file: ')
      pkgd = pkg
      my_rospkg.srv_flag = 1
      custom_srv_flag = 1
    else:
      srv = raw_input('Empty service list, creating a custom service type in package '+ pkg+'. Name your service file: ')
      pkgd = pkg
      my_rospkg.srv_flag = 1
      custom_srv_flag = 1
    srv_name = srv+'_service'
    srv_name = raw_input('Enter the name of your service: default ['+srv_name+']') or srv_name
    if custom_srv_flag:
      my_rospkg.edit_custom_srv()
      my_rospkg.gen_srv(srv)
    rosnd.add_client(pkgd,srv,srv_name)

  elif direction == 'server':
    while idx > len(a.service_list):
      idx = raw_input('Unknown service type, please re-enter the index of service you want to use: ') or idx
      idx = int(idx)
    srv = a.service_list[idx-1]
    end = srv.find('.srv')
    srv = srv[0:end]
    srv_name = srv+'_name'
    srv_name = raw_input('Enter the name of your service: default ['+srv_name+']') or srv_name
    cb_name =  srv +'CB'
    cb_name = raw_input('Enter the name of your message callback function: default ['+cb_name+']') or cb_name
    my_rospkg.srv_flag = 1  # this is supposed to get CMakeLists.txt right for services
    rosnd.add_server(pkgd,srv,srv_name,cb_name)

  my_rospkg.add_dependency(pkgd)


####################### Generate basic files ###########################
my_rospkg.add_node(rosnd)
my_rospkg.update_xmlfile()
my_rospkg.update_cmake()



