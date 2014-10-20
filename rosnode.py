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
import text
from readmsgsrv import ros_files

class ros_node:
  def __init__(self,name = '',lang = 'C++',path = ''):
    self.package = ''
    self.node_name = name
    self.lang = lang
    self.package_path = path
    self.imp_section = ''
    self.msg_pub_list = ''
    self.msg_obj_list = ''
    self.msg_pst_list = ''
    self.msg_sub_list = ''
    self.msg_cb_list = ''
    self.msv_init_list = ''
    self.srv_cb_list = ''
    self.srv_adv_list = ''
    self.srv_cli_inits = ''
    self.srv_cli_calls = ''
    self.srv_obj_list = ''
    self.srv_init_list = ''
    self.pub_num = 0
    self.sub_num = 0
    self.cli_num = 0
    self.ser_num = 0
  
  def get_package_name(self):
    path = self.package_path.split('/')
    name = path[len(path)-1]
    self.package = name
    return name

  def add_includes_for_msg(self,pkgd,msg):
    if self.lang =='C++':
      header = '#include "'+pkgd+'/'+msg+'.h"'
      if not header in self.imp_section:
        text.pkgd = pkgd
        text.msg = msg
        self.imp_section = self.imp_section + text.tagsub(text.imports_msg[self.lang])
    else:
      header = 'from '+pkgd+'.msg '+'import '+msg
      if not header in self.imp_section:
        text.pkgd = pkgd
        text.msg = msg
        self.imp_section = self.imp_section + text.tagsub(text.imports_msg[self.lang])

  def add_includes_for_srv(self,pkgd,srv):
    if self.lang =='C++':
      header = '#include "'+pkgd+'/'+srv+'.h"'
      if not header in self.imp_section:
        text.pkgd = pkgd
        text.srv = srv
        self.imp_section = self.imp_section + text.tagsub(text.imports_srv[self.lang])
    else:
      header = 'from '+pkgd+'.srv '+'import '+srv
      if not header in self.imp_section:
        text.pkgd = pkgd
        text.srv = srv
        self.imp_section = self.imp_section + text.tagsub(text.imports_srv[self.lang])


  def add_publisher(self,pkgd,msg,topic):
     self.pub_num +=1
     text.node_name = self.node_name
     text.pkgd = pkgd
     text.topic = topic
     text.msg = msg
     text.publisher_obj = msg+'_pub'+str(self.pub_num)
     text.msg_obj = msg +'_obj'+str(self.pub_num)
     self.assign_values_msg(pkgd,msg)
     self.msg_pub_list = self.msg_pub_list + text.tagsub(text.publisher[self.lang])
     self.msg_pst_list = self.msg_pst_list + text.tagsub(text.pubcalls[self.lang]) 
     self.msg_obj_list = self.msg_obj_list + text.tagsub(text.msgs[self.lang])
     self.add_includes_for_msg(pkgd,msg)
  
  def add_subscriber(self,pkgd,msg,topic,cb_name):
    self.sub_num +=1
    text.node_name = self.node_name
    text.clb = cb_name
    text.pkgd = pkgd
    text.topic = topic
    text.msg = msg
    text.subscriber_obj= msg+'_sub'+str(self.sub_num)
    self.msg_sub_list = self.msg_sub_list + text.tagsub(text.subscriber[self.lang])
    self.msg_cb_list = self.msg_cb_list + text.tagsub(text.msg_callback[self.lang])
    self.add_includes_for_msg(pkgd,msg)

  def add_client(self,pkgd,srv,srv_name):
    self.cli_num +=1
    text.node_name = self.node_name
    text.pkgd = pkgd
    text.srv_name = srv_name
    text.srv = srv
    text.client_obj = srv+'_cli'+str(self.cli_num)
    text.srv_obj = srv +'_obj'+str(self.cli_num)
    self.assign_values_srv(pkgd,srv)
    self.srv_cli_inits = self.srv_cli_inits + text.tagsub(text.clientinits[self.lang])
    self.srv_cli_calls = self.srv_cli_calls + text.tagsub(text.clientcalls[self.lang]) 
    self.srv_obj_list = self.srv_obj_list + text.tagsub(text.srvs[self.lang])
    self.add_includes_for_srv(pkgd,srv)

  def add_server(self,pkgd,srv,srv_name,cb_name):
    self.ser_num +=1
    text.node_name = self.node_name
    text.clb = cb_name
    text.pkgd = pkgd
    text.srv_name = srv_name
    text.srv = srv
    text.server_obj= srv+'_ser'+str(self.ser_num)
    self.srv_adv_list = self.srv_adv_list + text.tagsub(text.advertiser[self.lang])
    self.srv_cb_list = self.srv_cb_list + text.tagsub(text.srv_callback[self.lang])
    self.add_includes_for_srv(pkgd,srv)

  def assign_values_srv(self,pkgd,srv):
    a = ros_files(pkgd)
    a.get_package_path()
    if not a.package_found and self.get_package_name==pkgd:
      a.set_package_path(self.package_path)
    a.load_srv(srv)
    if a.req_list:
      req_list = a.req_list
      text.srv_var = ''
      text.arg = ''
      for l in req_list:
        text.srv_var = l[1]
        if l == req_list[0]:
          text.arg = text.srv_obj+'.'+l[1]
        else:
          text.arg = text.arg +', '+text.srv_obj+'.'+l[1]
        if l[0].startswith('int') or l[0].startswith('float'):
          text.val = '0'
        elif l[0].startswith('string'):
          text.val = '"please change this"'
        elif l[0].startswith('bool'):
          text.val = False
        else:
          print('Please initiate the variables manually !')
        self.srv_init_list = self.srv_init_list + text.tagsub(text.srvs_var_inits[self.lang])

  def assign_values_msg(self,pkgd,msg):
    a = ros_files(pkgd)
    a.get_package_path()
    if not a.package_found and self.get_package_name==pkgd:
      a.set_package_path(self.package_path)
    a.load_msg(msg)
    if a.msv_list:
      msv_list = a.msv_list
      text.msv = ''
      for l in msv_list:
        text.msv = l[1]
        if l[0].startswith('int') or l[0].startswith('float') or l[0].startswith('double'):
          text.val = '0'
        elif l[0].startswith('string'):
          text.val = '"please change this"'
        elif l[0].startswith('bool'):
          text.val = False
        else:
          print('Please initiate the variables manually !')
        self.msv_init_list = self.msv_init_list + text.tagsub(text.msgs_var_inits[self.lang])


  def gen_node_source(self):
    print('start to generate the source file for node '+self.node_name+' in language '+self.lang)
    text.node_name = self.node_name
    text.imp_section = self.imp_section
    text.msg_pub_list = self.msg_pub_list
    text.msg_obj_list = self.msg_obj_list
    text.msg_pst_list = self.msg_pst_list 
    text.msg_sub_list = self.msg_sub_list
    text.msg_cb_list = self.msg_cb_list
    text.msv_init_list = self.msv_init_list
    text.srv_cb_list = self.srv_cb_list 
    text.srv_adv_list = self.srv_adv_list 
    text.srv_cli_inits = self.srv_cli_inits 
    text.srv_cli_calls = self.srv_cli_calls
    text.srv_obj_list = self.srv_obj_list
    text.srv_init_list = self.srv_init_list
    text.pkg = self.get_package_name()
    if self.lang == 'C++':
      if not os.path.exists(self.package_path+'/src/'):
        os.mkdir(self.package_path+'/src/')
      codefilename = self.package_path+'/src/'+self.node_name +'.cpp'
      with open('templates/cpp_template.cpp') as file:
        filetemplate = file.readlines()
    elif self.lang == 'Python':
      if not os.path.exists(self.package_path+'/scripts/'):  # make scripts directory if not there
        os.mkdir(self.package_path+'/scripts/')
      codefilename = self.package_path+'/scripts/'+self.node_name +'.py'
      with open('templates/pyt2_template.py') as file:
        filetemplate = file.readlines()
    else:
      print('Unknown languange')
    with open(codefilename, 'w') as outfile:
      for line in filetemplate:
        outfile.write(text.sectsub(text.tagsub(line)))
      os.chmod(codefilename, 0755)  # make it executable
      

if __name__ == '__main__':

   rws = '/home/blake/Projects/Ros2/RosNodeGen/'

   #a = ros_node('cc','Python','/home/danying/ROSWorkspace/ros_node_generator/srvtest')
   a = ros_node('cc','Python',rws+'srvtest')
   #a.add_publisher('pc','test','pusfsd')
   #a.add_client('srvtest','custom','lunch')
   #a.add_client('srvtest','custom','dinner')
   #a.add_server('srvtest','custom','dinner','dinnercallback')
   #a.add_server('srvtest','custom','lunch','lunchcallback')
   #a.gen_node_source()
   
