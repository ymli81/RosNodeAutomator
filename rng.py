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

## Node name ##
node_name = pkg + '_node'
node_name = raw_input('Enter your new node name: ['+node_name+ ']: ') or node_name
while(rospkg.check_node_name(node_name)):
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
      direction = raw_input('Unknown message handle, [P]ublish or [S]ubscribe?:') or direction
  
  pkgd = 'std_msgs'
  pkgd = raw_input('Enter the package that contains your message, default package: [ '+pkgd+' ]') or pkgd
  a = ros_files(pkgd)
  a.find_msgs()
  msg = ''
  idx = 0
  if a.message_list:
     idx = raw_input('Enter the index of message you want to '+direction+': ')
     idx = int(idx)
  else:
    if direction == 'subscribe':   
      direction ='unknown'
   
  if direction == 'publish':
    if not idx > len(a.message_list) and a.message_list:
      msg = a.message_list[idx-1]
      end = msg.find('.msg')
      msg = msg[0:end]
      msg_flag = 0
    elif idx > len(a.message_list) and a.message_list:
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
  
  rospkg.add_dependency(pkgd)

## Services ##




####################### Generate basic files ###########################
rospkg.add_node(rosnd)
rospkg.update_manifest()
rospkg.update_cmake()


