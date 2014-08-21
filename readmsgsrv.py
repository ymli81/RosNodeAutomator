#!/usr/bin/env python
import os, sys
import rospkg

class ros_files():
  def __init__(self, pkg):
    self.rospack = rospkg.RosPack()
    self.package_name = pkg
    self.package_path = ''
    self.message_list = []
    self.service_list = []
    self.action_list = []
    self.msv_list = []
    self.req_list = []
    self.res_list = []
    self.package_found = False
  
  def get_package_path(self):
    try:
      self.package_path = self.rospack.get_path(self.package_name)
      self.package_found = True
    except:
      self.package_found = False

  def set_package_path(self,path):
    self.package_path = path
    self.package_found = True

  def find_msgs(self):
    if self.package_found:
      msgdir = self.package_path+'/msg'
      if os.path.exists(msgdir): 
        try: 
          message_list = os.listdir(msgdir)
          for l in message_list:
            if '.msg' in l:
              self.message_list.append(l)
        except:
          print('fail to list the messages')
          return 0
        return 1
      else:
        print('cannot find message files in the package '+self.package_name)
        return 0
    else:
      print('ros package '+self.package_name+' does not exist !')
      return 0
  
  def list_msgs(self):
    if self.find_msgs():
      i = 0
      print('Find the following messages in the package '+self.package_name+':')
      for l in self.message_list:
        i +=1
        print(str(i)+': '+l)

  def find_srvs(self):
    if self.package_found:
      srvdir = self.package_path+'/srv'
      if os.path.exists(srvdir): 
        try: 
          service_list = os.listdir(srvdir)
          for l in service_list:
            if '.srv' in l:
              self.service_list.append(l)
        except:
          print('fail to list the services')
          return 0
        return 1
      else:
        print('cannot find service files in the package '+self.package_name)
        return 0
    else:
      print('ros package '+self.package_name+' does not exist !')
      return 0

  def list_srvs(self):
    if self.find_srvs():
      i = 0
      print('Find the following services in the package '+self.package_name+':')
      for l in self.service_list:
        i += 1
        print(str(i)+': '+l)

  def load_msg(self,msg):
    if self.find_msgs(): 
       if msg+'.msg' in self.message_list:
         with open(self.package_path+'/msg/'+ msg+'.msg', 'r') as msgfile:    
           tmp = msgfile.readlines()
         for l in tmp:
           if l.startswith('#'): print('this is a comment line')
           elif l.startswith('Header'): print('this is a header line')
           elif l.startswith('\n'): print('this is an empty line')
           else:
             tline = l.split(' ')
             ttype = tline[0]
             end = tline[len(tline)-1].find('\n')
             tvar = tline[len(tline)-1][0:end]
             self.msv_list.append([ttype, tvar])
    else:
      print('Unable to load the message with name '+msg)

  def load_srv(self,srv):
    if self.find_srvs(): 
       if srv+'.srv' in self.service_list:
         with open(self.package_path+'/srv/'+ srv+'.srv', 'r') as srvfile:    
           tmp = srvfile.readlines()
         res_flag = 0
         for l in tmp:
           if l.startswith('#'): print('this is a comment line')
           elif l.startswith('---'): res_flag = 1
           elif l.startswith('\n'): print('this is an empty line') 
           else:
             tline = l.split(' ')
             ttype = tline[0]
             end = tline[len(tline)-1].find('\n')
             tvar = tline[len(tline)-1][0:end]
             if res_flag ==0:
               self.req_list.append([ttype, tvar])
             else:
               self.res_list.append([ttype, tvar])
    else:
      print('Unable to load the sevice with name '+srv)


if __name__ == '__main__':
  a = ros_files('srvtest')
  a.get_package_path()
  a.load_msg('test')
  a.load_srv('custom')
  print(a.msv_list)
  print(a.req_list)



