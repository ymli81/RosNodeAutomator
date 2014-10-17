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
#import rospkg
import text
from rosnode import ros_node

class ros_package():
  def __init__(self,name = '',rws = '',bs = ''):
    self.build_system = bs
    self.package_name = name
    self.rws = rws
    self.package_path = ''
    self.msg_path = ''
    self.srv_path = ''
    self.node_list = []   #node list from CMakelist.txt
    self.msg_list = []
    self.srv_list = []
    self.dependency_list= []
    self.msg_flag = 0
    self.srv_flag = 0
    self.license = ''
    self.email = ''
    self.new_msg =''
    self.new_srv =''

  def set_build_system(self, bs):
    self.build_system = bs

  def set_package_name(self,name):
    self.package_name = name

  def set_package_rws(self,rws):
    self.rws = rws
    #self.package_path = self.rws + 'src/' + self.package_name

  def set_package_path(self):
    if self.build_system == 'ros_build':
      self.package_path = self.rws+self.package_name # is this rosbuild style?
      self.msg_path = self.package_path + '/msg'
      self.srv_path = self.package_path + '/srv'
    elif self.build_system == 'catkin':
      self.package_path = self.rws+'src/'+self.package_name
      self.msg_path = self.package_path + '/msg'
      self.srv_path = self.package_path + '/srv'
    else:
      print('Unknown build environment. Please specify your build system in param_node.py')

# ros_build and catkin
  def create_package_folder(self):
    if not self.rws:
      print('Please set your workspace')
    else:
      self.set_package_path()
      if not os.path.exists(self.package_path):
        print('Package does not exist, creating a new package directory '+self.package_path)
        os.makedirs(self.package_path)
        self.gen_cmake()
        if self.build_system == 'ros_build':
          self.gen_mkfile()  #  'makefile' only needed for ros_build
          self.gen_manifest()
        else:
          self.gen_package_catkin()

# ros_build AND catkin
  def get_package_msgs(self):
    if os.path.exists(self.msg_path):
      try:
        message_list = os.listdir(self.msg_path)
        i = 0
        sub = '.msg'
        for l in message_list:
          if sub in l:
            i +=1
            self.msg_list.append(l)
      except:
        self.msg_list = []
    else:
        self.msg_list = []

# ros_build AND catkin
  def get_package_srvs(self):
    if os.path.exists(self.srv_path):
      try:
        service_list = os.listdir(self.srv_path)
        i = 0
        sub = '.srv'
        for l in srv_list:
          if sub in l:
            i +=1
            self.srv_list.append(l)
      except:
        self.srv_list = []
    else:
      self.srv_list = []

# ros_build AND catkin
  def get_dependency_list(self):
    try:
      if self.build_system == 'ros_build':
        with open(self.package_path+'/'+'manifest.xml', 'r') as outfile:
          for line in outfile:
            if line.startswith('  <depend package="'):
              line = line.split('"')
              if line[1]!='roscpp' and line[1]!='rospy' and not line[1] in self.dependency_list:
                self.dependency_list.append(line[1])
      else:
        with open(self.package_path+'/'+'package.xml', 'r') as outfile:
          for line in outfile:
            if line.startswith('  <build_depend>'):
              line = line.split('</')
              dependency = line[0][16:]
              if dependency!='roscpp' and dependency!='rospy' and dependency!='message_generation' and not dependency in self.dependency_list:
                self.dependency_list.append(dependency)
    except:
       self.dependency_list = []

# ros_build AND catkin
  def get_node_list(self):
    self.node_list = []
    try:
      with open(self.package_path+'/'+'CMakeLists.txt', 'r') as inputfile: # can't read an outfile!
        for line in inputfile:
          if line.startswith('rosbuild_add_executable('):
            line = line.split(' ')
            node_name = line[0][24:]
            self.node_list.append(node_name)
          elif line.startswith('add_executable('):
            line = line.split(' ')
            node_name = line[0][15:]
            self.node_list.append(node_name)
    except:
      print('excepted')
      self.node_list = []

# ros_build only
  def gen_mkfile(self):
    with open('templates/MakefileTemplate', 'r') as mfile:
      m_template = mfile.readlines()
    with open(self.package_path+'/'+'Makefile', 'w') as outfile:
      for line in m_template:
        outfile.write(line)
    print('Created package file '+self.package_path+'/Makefile')


# ros_build AND catkin
  def gen_cmake(self):
    if self.build_system == 'ros_build':
      with open('templates/CMakeListTemplate_rosbuild.txt', 'r') as cfile:
        cm_template = cfile.readlines()
    else:
      text.pkg = self.package_name
      with open('templates/CMakeListTemplate_catkin.txt', 'r') as cfile:
        cm_template = cfile.readlines()
    with open(self.package_path+'/'+'CMakeLists.txt', 'w') as outfile:
      for line in cm_template:
        outfile.write(text.sectsub(text.tagsub(line)))
    print('Created package file '+self.package_path+'/CMakeList.txt')

# ros_build AND catkin
  def update_cmake(self):
    print('start to update CMakeList.txt')
    if self.build_system == 'ros_build':
      self.update_cmake_rosbuild()
    elif self.build_system == 'catkin':
      self.update_cmake_catkin()
    else:
      print('Unknown build environment. Please specify your build system in param_node.py')

# ros_build only
  def update_cmake_rosbuild(self):
    text.exe_list = ''
    for i in self.node_list:
      text.node_name = i
      text.exe_list = text.exe_list + text.tagsub(text.executable_rosbuild)
    with open(self.package_path+'/'+'CMakeLists.txt', 'r') as cmfile:
      cmfile = cmfile.readlines()
    if (self.msg_flag == 1):
      text.msg_gen = 'rosbuild_genmsg()'
    else:
      if 'rosbuild_genmsg()\n' in cmfile:
        text.msg_gen = 'rosbuild_genmsg()'
      else:
        text.msg_gen = '#rosbuild_genmsg()'
    if (self.srv_flag == 1):
      text.srv_gen = 'rosbuild_gensrv()'
    else:
      if 'rosbuild_gensrv()\n' in cmfile:
        text.srv_gen = 'rosbuild_gensrv()'
      else:
        text.srv_gen = '#rosbuild_gensrv()'
    self.gen_cmake()

# catkin only
  def update_cmake_catkin(self):
    text.exe_list = ''
    text.catkin_dependency_list = ''
    for i in self.node_list:
      text.node_name = i
      text.exe_list = text.exe_list + text.tagsub(text.executable_catkin)
    text.msg_list, text.srv_list = self.process_cmake_catkin()
    if (self.msg_flag == 1) or (self.srv_flag == 1):
      text.msg_gen = 'generate_messages(DEPENDENCIES std_msgs)'
      if self.msg_flag == 1: 
        text.msg_list = text.msg_list + self.new_msg
        text.msg_add = text.tagsub(text.msg_add_file)
        self.new_msg = ''
      if self.srv_flag == 1:
        text.srv_list = text.srv_list + self.new_srv
        text.srv_add = text.tagsub(text.srv_add_file)
        self.new_Srv = ''
    else:
      text.msg_gen = ''
      text.msg_add = ''
      text.srv_add = ''
    for i in self.dependency_list:
      print(i)
      text.catkin_dependency_list = text.catkin_dependency_list + i +' '
    self.gen_cmake()

# catkin only
  def process_cmake_catkin(self):
    msg_file_list = ''
    srv_file_list = ''
    dep_pkg_list = ''
    with open(self.package_path+'/'+'CMakeLists.txt', 'r') as cmfile:
      cmfile = cmfile.readlines()
    for line in cmfile:
      if line.startswith('add_message_files'):
        self.msg_flag = 1
        line = line.split(' ')
        for tmp in line:
          if ".msg" in tmp:
            fileName = tmp[:tmp.find(".msg") + len(".msg")]
            msg_file_list = msg_file_list + fileName+ ' '
      elif line.startswith('add_service_files'):
        self.srv_flag = 1
        line = line.split(' ')
        for tmp in line:
          if ".srv" in tmp:
            fileName = tmp[:tmp.find(".srv") + len(".srv")]
            srv_file_list = srv_file_list + fileName+ ' '
      elif line.startswith('find_package('):
        line = line.split(' ')
        for tmp in line:
          if tmp and not tmp=='find_package(catkin' and not tmp=='REQUIRED' and not tmp=='COMPONENTS' and not tmp=='roscpp' and not tmp=='rospy' and not tmp == 'message_generation':
            fileName = tmp[:tmp.find(")")]
            dep_pkg_list = dep_pkg_list + fileName + ' '
    return msg_file_list,srv_file_list

 # ros_build only
  def gen_manifest(self):
    with open('templates/manifestTemplate.xml', 'r') as mfile:
      m_template = mfile.readlines()
    with open(self.package_path+'/'+'manifest.xml', 'w') as outfile:
      for line in m_template:
         outfile.write(text.sectsub(text.tagsub(line)))
    print('Created package file '+self.package_path+'/manifest.xml')

 # ros_build only
  def update_manifest(self):
    print('start to update manifest.xml')
    text.dependency_list = ''
    for i in self.dependency_list:
      if not i == self.package_name:
        text.pkgd = i
        text.dependency_list = text.dependency_list + text.tagsub(text.depend)
    with open('templates/manifestTemplate.xml', 'r') as mfile:
      m_template = mfile.readlines()
    with open(self.package_path+'/'+'manifest.xml', 'w') as outfile:
      for line in m_template:
         outfile.write(text.sectsub(text.tagsub(line)))

# catkin only
  def gen_package_catkin(self):
    text.pkg = self.package_name
    with open('templates/packageTemplate.xml', 'r') as mfile:
      m_template = mfile.readlines()
    with open(self.package_path+'/'+'package.xml', 'w') as outfile:
      for line in m_template:
         outfile.write(text.sectsub(text.tagsub(line)))
    print('Created package file '+self.package_path+'/package.xml')

# catkin only
  def update_package_catkin(self):
    print('start to update package.xml')
    text.dependency_list = ''
    for i in self.dependency_list:
      if not i == self.package_name:
        text.pkgd = i
        text.dependency_list = text.dependency_list + text.tagsub(text.depend_pkg_catkin)
    with open('templates/packageTemplate.xml', 'r') as mfile:
      m_template = mfile.readlines()
    with open(self.package_path+'/'+'package.xml', 'w') as outfile:
      for line in m_template:
         outfile.write(text.sectsub(text.tagsub(line)))

# ros_build AND catkin
  def update_xmlfile(self):
    if self.build_system == 'ros_build':
      self.update_manifest()
    else:
      self.update_package_catkin()
  

# ros_build AND catkin
  def gen_msg(self,msg_name):
    if not os.path.exists(self.msg_path):
      os.makedirs(self.msg_path)
    self.msg_list = os.listdir(self.msg_path)
    while self.check_msg_name(msg_name):
      msg_name = raw_input('Message file exists already, please use another name: ') or msg_name
    print('Generating '+msg_name+'.msg file')
    with open('templates/msgTemplate.msg', 'r') as mfile:
      m_template = mfile.readlines()
    with open(self.msg_path+'/'+msg_name+'.msg', 'w') as outfile:
      for line in m_template:
        outfile.write(text.sectsub(text.tagsub(line)))
    self.new_msg = msg_name+'.msg'

# ros_build AND catkin
  def gen_srv(self,srv_name):
    if not os.path.exists(self.srv_path):
      os.makedirs(self.srv_path)
    self.srv_list = os.listdir(self.srv_path)
    while self.check_srv_name(srv_name):
      srv_name = raw_input('Service file exists already, please use another name: ') or srv_name
    print('Generating the '+srv_name+'.srv file')
    with open('templates/srvTemplate.srv', 'r') as sfile:
      s_template = sfile.readlines()
    with open(self.srv_path+'/'+srv_name+'.srv', 'w') as outfile:
      for line in s_template:
	outfile.write(text.sectsub(text.tagsub(line)))
    self.new_srv = srv_name+'.srv'

#  ros_build and catkin
  def add_node(self,node):
    if node.lang == 'C++':
      self.add_node_list(node.node_name)
    elif node.lang == 'Python':
      print('')
    else:
      print('Unknown languange')
    node.gen_node_source()

# ros_build only
  def add_dependency(self,dependency):
    self.get_dependency_list()
    if not dependency in self.dependency_list and not dependency==self.package_name:
      self.dependency_list.append(dependency)

# ros_build AND catkin
  def add_node_list(self,node_name):
    self.get_node_list()
    if not node_name in self.node_list:
      self.node_list.append(node_name)
    else:
      print('Node name exist already, please use another name')

# ros_build AND catkin
  def check_node_name(self,node_name):
    self.get_node_list()
    if not node_name in self.node_list:
      return 0
    else:
      return 1

# ros_build AND catkin
  def check_msg_name(self, msg_name):
     self.get_package_msgs()
     if msg_name+'.msg' in self.msg_list:
       return 1
     else:
       return 0

# ros_build AND catkin
  def check_srv_name(self, srv_name):
     self.get_package_srvs()
     if srv_name+'.srv' in self.srv_list:
       return 1
     else:
       return 0

# ros_build AND catkin
  def edit_custom_msg(self):
    text.msg_var_list = ''
    var_num = 0
    text.var_type = 'int32'
    while 1:
      res = raw_input('Do you want to add a variable into your message file? (y for yes, n/CR for no) ') or -1
      if (res == -1) or (res[0]=='n') or (res[0] == 'N'):
        print('Do not forget to edit the .msg file before compile')
        break
      else:
        var_num += 1
        text.msv = 'my_message_var'+ str(var_num)
        print 'New message variable: '+text.msv
        text.var_type = raw_input('New message variable type? [default: '+text.var_type+']') or text.var_type
        text.msg_var_list = text.msg_var_list + text.tagsub(text.msv_list_element)

# ros_build AND catkin
  def edit_custom_srv(self):
    text.srv_var_list = ''
    var_num = 0
    text.var_type = 'int32'
    while 1:
      res = raw_input('Do you want to add a variable into your srv file? (y for yes, n/CR for no) ') or -1
      if (res == -1) or (res[0]=='n') or (res[0] == 'N'):
        print('Do not forget to edit the .srv file before compile')
        break
      else:
        while 1:
          text.var_type = raw_input('Enter the type of request variable '+str(var_num+1)+', [default: '+text.var_type+'], (n for stop)') or text.var_type
          if (req[0]=='n') or (req[0] == 'N'):
            break
          else:
            var_num += 1
            text.msv = 'my_request_var'+ str(var_num)
            text.srv_var_list = text.srv_var_list + text.tagsub(text.srv_list_element)

        text.srv_var_list = text.srv_var_list + '---\n'
        var_num = 0
        print '---'
        while 1:
          req = raw_input('Enter the type of response variable '+str(var_num+1)+', [default: '+text.var_type+'], (n for stop)') or text.var_type
          if (req[0]=='n') or (req[0] == 'N'):
            break
          else:
            var_num += 1
            text.msv = 'my_response_var'+ str(var_num)
            text.srv_var_list = text.srv_var_list + text.tagsub(text.srv_list_element)
      break


if __name__ == '__main__':
  # create a test package:  name = "pc" ros workspace = "/Users ... "
   a = ros_package('beginner_tutorials','/home/danying/ROSWorkspace/ros_node_generator')
   a.set_build_system('catkin')
   print(a.package_path)
   a.get_dependency_list()
   a.get_node_list()
   print(a.dependency_list)
   a.update_cmake_catkin()

   #a.edit_custom_msg()
   #a.gen_msg('lol')

