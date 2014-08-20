#!/usr/bin/env python
import os, sys
#import rospkg
import text
from rosnode import ros_node

class ros_package():
  def __init__(self,name = '',rws = ''):
    self.package_name = name
    self.rws = rws
    self.package_path = rws+'/'+name
    self.msg_path = self.package_path + '/msg'
    self.srv_path = self.package_path + '/srv'
    self.node_list = []   #node list from CMakelist.txt
    self.msg_list = []
    self.srv_list = []
    self.dependency_list= []
    self.msg_flag = 0
    self.srv_flag = 0
    self.license = ''
    self.email = ''

  def set_package_name(self,name):
    self.package_name = name
    self.package_path = self.rws + '/' + self.package_name
  
  def set_package_rws(self,rws):
    self.rws = rws
    self.package_path = self.rws + '/' + self.package_name

  def create_package_folder(self):
    if not self.rws:
      print('Please set your workspace')
    else:
      if not os.path.exists(self.package_path):
        print('Package does not exist, creating a new package with name '+self.package_name)
        os.makedirs(self.package_path)
    self.gen_mkfile()

  def get_package_msgs(self):
    ## do stuff
    return self.msg_list

  def get_package_srvs(self):
    ## do stuff
    return self.srv_list

  def get_dependency_list(self):
    try:
      with open(self.package_path+'/'+'manifest.xml', 'r') as outfile:
        for line in outfile:
          if line.startswith('  <depend package="'):
            line = line.split('"')
            if line[1]!='roscpp' and line[1]!='rospy' and not line[1] in self.dependency_list:
              self.dependency_list.append(line[1])
    except:
       self.dependency_list = []

  def get_node_list(self):
    self.node_list = []
    try:
      with open(self.package_path+'/'+'CMakeLists.txt', 'r') as outfile:
        for line in outfile:
          if line.startswith('rosbuild_add_executable('):
            line = line.split(' ')
            node_name = line[0][24:]
            self.node_list.append(node_name)
    except:
      self.node_list = []

  def gen_mkfile(self):
	  print('start to generate Makefile')
	  with open('templates/MakefileTemplate', 'r') as mfile:    
		  m_template = mfile.readlines()
	  with open(self.package_path+'/'+'Makefile', 'w') as outfile: 
		  for line in m_template:
			  outfile.write(line)

  def gen_cmake(self):
    with open('templates/CMakeListTemplate.txt', 'r') as cfile:
      cm_template = cfile.readlines()
    with open(self.package_path+'/'+'CMakeLists.txt', 'w') as outfile:       
      for line in cm_template:
        outfile.write(text.sectsub(text.tagsub(line)))

  def update_cmake(self):
    print('start to update CMakeList.txt')
    text.exe_list = ''
    for i in self.node_list:
      text.node_name = i
      text.exe_list = text.exe_list + text.tagsub(text.executable)
    if not os.path.isfile(self.package_path+'/'+'CMakeLists.txt'):
      if (self.msg_flag == 1):
        text.msg_gen = 'rosbuild_genmsg()'
      else:
        text.msg_gen = '#rosbuild_genmsg()'
      if (self.srv_flag == 1):
        text.srv_gen = 'rosbuild_gensrv()'
      else:
        text.srv_gen = '#rosbuild_gensrv()'
      self.gen_cmake()
    else:
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

  def gen_msg(self,msg_name):
    print('start to generate the '+msg_name+'.msg file')
    #if flag == 0:
       #text.msgs_var_list = ''
    if not os.path.exists(self.package_path+'/'+'msg'): 
      os.makedirs(self.package_path+'/'+'msg')
    self.msg_list = os.listdir(self.package_path+'/'+'msg')
    if not msg_name+'.msg' in self.msg_list:
      with open('templates/msgTemplate.msg', 'r') as mfile:    
        m_template = mfile.readlines()
      with open(self.package_path+'/'+'msg''/'+msg_name+'.msg', 'w') as outfile: 
        for line in m_template:
	      outfile.write(text.sectsub(text.tagsub(line)))
    else:
      print('Message file exists already, please use another name')

  def add_node(self,node):
    if node.lang == 'C++':
      self.add_node_list(node.node_name)
    elif node.lang == 'Python':
      print('')
    else:
      print('Unknown languange')
    node.gen_node_source()
    
  def add_dependency(self,dependency):
    self.get_dependency_list()
    if not dependency in self.dependency_list:
      self.dependency_list.append(dependency)
  
  def add_node_list(self,node_name):
    self.get_node_list()
    if not node_name in self.node_list:
      self.node_list.append(node_name)
    else:
      print('Node name exist already, please use another name')

  def check_node_name(self,node_name):
    self.get_node_list()
    if not node_name in self.node_list:
      return 0
    else:
      return 1

  def edit_custom_msg(self):
    text.msgs_var_list = ''
    var_num = 0
    text.var_type = 'int32'
    while 1:
      res = raw_input('Do you want to add a variable into your message file? (y for yes, n/CR for no) ') or -1
      if (res == -1) or (res[0]=='n') or (res[0] == 'N'):
        break
      else:
        var_num += 1
        text.var_type = raw_input('What is the type of your message variable '+str(var_num)+', [default: '+text.var_type+']') or text.var_type
        text.msv = 'my_message_var'+ str(var_num)
        text.msgs_var_list = text.msgs_var_list + text.tagsub(text.msv_list)
        

if __name__ == '__main__':
   a = ros_package('pc','/Users/Danying/Dropbox/ROSworkspace/ros_node_generator')
   #a.get_node_list()
   #print(a.node_list)
   a.edit_custom_msg()
   a.gen_msg('lol')
   


