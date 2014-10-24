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
import rospkg

class ros_files():
  def __init__(self, pkg):
    self.rospack = rospkg.RosPack()
    self.package_name = pkg
    self.package_path = ''
    self.msg_path = ''
    self.srv_path = ''
    self.message_list = []
    self.service_list = []
    self.action_list = []
    self.msv_list = []
    self.req_list = []
    self.res_list = []
    self.package_found = False

  def get_package_path(self):
    try:
      print 'getting path for package: ['+self.package_name+']'
      self.package_path = self.rospack.get_path(self.package_name)
      print 'Found package path: '+self.package_path
      self.msg_path = self.package_path + '/msg/'
      self.srv_path = self.package_path + '/srv/'
      self.package_found = True
    except Exception as exc:
      name_of_exception = type(exc).__name__
      print 'Could not "rospack.get_path" of package: '+self.package_name
      print 'Ros exception: '+name_of_exception
      self.package_found = False
      self.msg_path = "<<error!>>"

  def set_package_path(self,path):
    self.package_path = path
    self.package_found = True

  def find_msgs(self):
    if self.package_found:
      if os.path.exists(self.msg_path):
        try:
          message_list = os.listdir(self.msg_path)
          for l in message_list:
            if '.msg' in l:
              self.message_list.append(l)
        except:
          print('fail to list the messages')
          return 0
        return 1
      else:
        print('cannot find message files in the package '+self.msg_path)
        return 0
    else:
      print('ros package '+self.package_name+' does not exist !')
      return 0

  def list_msgs(self):
    if self.find_msgs():
      i = 0
      print('Found the following messages in the package '+self.msg_path+':')
      for l in self.message_list:
        i +=1
        print(str(i)+': '+l)

  def find_srvs(self):
    if self.package_found:
      if os.path.exists(self.srv_path):
        try:
          service_list = os.listdir(self.srv_path)
          for l in service_list:
            if '.srv' in l:
              self.service_list.append(l)
        except:
          print('fail to list the services')
          return 0
        return 1
      else:
        print('cannot find service files in the package '+self.srv_path)
        return 0
    else:
      print('ros package '+self.package_name+' does not exist !')
      return 0

  def list_srvs(self):
    if self.find_srvs():
      i = 0
      print('Found the following services in the package '+self.srv_path+':')
      for l in self.service_list:
        i += 1
        print(str(i)+': '+l)

  def load_msg(self,msg):
    if self.find_msgs():
       if msg+'.msg' in self.message_list:
	 msg_filename = self.package_path+'/msg/'+ msg+'.msg'
         with open(msg_filename, 'r') as msgfile:
	   print 'Scanning message file: '+msg_filename
           tmp = msgfile.readlines()
         for l in tmp:
           if l.startswith('#'): x = 0 #print('found a comment line')
           elif l.startswith('Header'): x=0 #print('found is a header line')
           elif l.startswith('\n'): x= 0 #print('found an empty line')
           else:
             tline = l.split(' ')
             ttype = tline[0]
             end = tline[len(tline)-1].find('\n')
             tvar = tline[len(tline)-1][0:end]
             self.msv_list.append([ttype, tvar])
             print('found a message variable: '+tvar+' in type '+ttype)
    else:
      print('Unable to load the message with name '+msg)

  def load_srv(self,srv):
    if self.find_srvs():
       if srv+'.srv' in self.service_list:
         srv_filename = self.package_path+'/srv/'+ srv+'.srv'
         with open(srv_filename, 'r') as srvfile:
           print 'Scanning service file: '+srv_filename
           tmp = srvfile.readlines()
         res_flag = 0
         for l in tmp:
           if l.startswith('#'):  #print('this is a comment line')
             x = 0 # dummy line
           elif l.startswith('---'):
             res_flag = 1
           elif l.startswith('\n'):   #print('this is an empty line')
             x = 0 # dummy line
           else:
             tline = l.split(' ')
             ttype = tline[0]
             end = tline[len(tline)-1].find('\n')
             tvar = tline[len(tline)-1][0:end]
             if res_flag ==0:
               self.req_list.append([ttype, tvar])
               print('found a request variable: '+tvar+' in type '+ttype)
             else:
               self.res_list.append([ttype, tvar])
               print('found a response variable: '+tvar+' in type '+ttype)
    else:
      print('Unable to load the sevice with name '+srv)


if __name__ == '__main__':
  a = ros_files('srvtest')
  a.get_package_path()
  a.load_msg('test')
  a.load_srv('custom')
  print(a.msv_list)
  print(a.req_list)



