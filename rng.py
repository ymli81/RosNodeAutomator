#!/usr/bin/env python
import os, sys
from readmsgsrv import ros_files
from rospackage import ros_package
from rosnode import ros_node

print ('Welcome to ROS node generator  *****')
print ('Please answer a few questions about your new node:')

########################### Get System Setup #############################
with open('param_node.py') as pfile:
  initcode = pfile.readlines()
for line in initcode:
  exec (line)

####################### Query user for details ###########################
##  Package name ## 
pkg = raw_input('Enter your package name: ') or pkg
rospkg = ros_package(pkg,rws)
rospkg.create_package_folder()
rospkg.set_build_system = ros_build_system

## Node name ##
node_name = pkg + '_node'
node_name = raw_input('Enter your new node name: ['+node_name+ ']: ') or node_name
while rospkg.check_node_name(node_name):
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

rosnd = ros_node(node_name,lang,rospkg.package_path)

## Messages ##
while 1:
  resp = raw_input('Do you want to add a message? (y for yes, n/CR for no) ') or -1
  if (resp == -1) or (resp[0]=='n') or (resp[0] == 'N '):
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
  
  pkgd = pkg 
  pkgresp = raw_input('Enter the package that contains your message ['+pkgd+']') or pkgd
  a = ros_files(pkgresp)
  a.get_package_path()
  
  if not a.package_found and pkgd==pkgresp:      #  can you comment this????
    a.set_package_path(rospkg.package_path)
  a.list_msgs()
  msg = ''
  idx = 0
  if a.message_list:
     idx = raw_input('Enter the index of message you want to '+direction+': ')
     idx = int(idx)   #  careful: a python 'feature' is that entering a decimal ('2.0') will break this!
  else:
    if direction == 'subscribe':  
      print('You cannot subscribe to nonexisting message') 
      direction ='unknown'
   
  if direction == 'publish':
    if not idx > len(a.message_list) and idx >0 and a.message_list:
      msg = a.message_list[idx-1]
      end = msg.find('.msg')
      msg = msg[0:end]
      msg_flag = 0
    elif (idx > len(a.message_list) or idx == 0) and a.message_list:
      msg = raw_input('Unknown message, creating a custom message in package '+ pkg+'. Name your message: ')
      pkgd = pkg
      rospkg.msg_flag = 1
      msg_flag = 1
    else:
      msg = raw_input('Empty message list, creating a custom message in package '+ pkg+'. Name your message: ')
      pkgd = pkg
      rospkg.msg_flag = 1
      msg_flag = 1
   
    topic = msg+'_topic'
    topic = raw_input('Enter the topic of your message: default ['+topic+']') or topic
    if msg_flag:
      rospkg.edit_custom_msg()
      rospkg.gen_msg(msg)
    rosnd.add_publisher(pkgd,msg,topic)

  elif direction == 'subscribe':
    while idx > len(a.message_list):
      idx = raw_input('Unknown message, please re-enter the index of message you want to '+direction) or idx
      idx = int(idx)
    msg = a.message_list[idx-1]
    end = msg.find('.msg')
    msg = msg[0:end]
    topic = msg+'_topic'
    topic = raw_input('Enter the topic of your message: default ['+topic+']') or topic
    cb_name =  msg+'CB'
    cb_name = raw_input('Enter the name of your message callback function: default ['+cb_name+']') or cb_name
    rosnd.add_subscriber(pkgd,msg,topic,cb_name)
  
  rospkg.add_dependency(pkgresp)    

## Services ##
while 1:
  resp = raw_input('Do you want to add a service? (y for yes, n/CR for no) ') or -1
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
  
  pkgd = raw_input('Enter the package that contains your service, default package: [ '+pkg+' ]') or pkg
  a = ros_files(pkgd)
  a.get_package_path()
  if not a.package_found and pkg==pkgd:
    a.set_package_path(rospkg.package_path)
  a.list_srvs()
  srv = ''
  idx = 0
  if a.service_list:
     idx = raw_input('Enter the index of service type you want to use: ')
     idx = int(idx)
  else:
     if direction == 'server': 
       print('You cannot use a nonexisting service type')
       direction = 'unknown'
   
  if direction == 'client':
    if not idx > len(a.service_list) and idx>0 and a.service_list :
      srv = a.service_list[idx-1]
      end = srv.find('.srv')
      srv = srv[0:end]
      srv_flag = 0
    elif (idx > len(a.service_list) or idx == 0) and a.service_list:
      srv = raw_input('Unknown service type, creating a custom service type in package '+ pkg+'. Name your service type: ')
      pkgd = pkg
      rospkg.srv_flag = 1
      srv_flag = 1
    else:
      srv = raw_input('Empty service list, creating a custom service type in package '+ pkg+'. Name your service type: ')
      pkgd = pkg
      rospkg.srv_flag = 1
      srv_flag = 1
    srv_name = srv+'_name'
    srv_name = raw_input('Enter the name of your service: default ['+srv_name+']') or srv_name
    if srv_flag:
      rospkg.edit_custom_srv()
      rospkg.gen_srv(srv)
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
    rosnd.add_server(pkgd,srv,srv_name,cb_name)
  
  rospkg.add_dependency(pkgd)


####################### Generate basic files ###########################
rospkg.add_node(rosnd)
rospkg.update_manifest()
rospkg.update_cmake()


