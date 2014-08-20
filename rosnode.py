import os, sys
#import rospkg
import text

class ros_node():
  def __init__(self,name = '',lang = 'C++',path = ''):
    self.node_name = name
    self.lang = lang
    self.node_path = path
    self.imp_section = ''
    self.msg_pub_list = ''
    self.msg_obj_list = ''
    self.msg_pst_list = ''
    self.msg_sub_list = ''
    self.msg_cb_list = ''
    self.srv_cb_list = ''
    self.srv_adv_list = ''
    self.srv_cli_inits = ''
    self.srv_cli_calls = ''
    self.pub_num = 0
    self.sub_num = 0
  
  def get_package_name(self):
    path = self.node_path.split('/')
    name = path[len(path)-1]
    return name

  def add_includes(self,pkgd,msg):
    header = '#include "'+pkgd+'/'+msg+'.h"'
    if not header in self.imp_section:
      text.pkgd = pkgd
      text.msg = msg
      self.imp_section = self.imp_section + text.tagsub(text.imports[self.lang])	

  def add_publisher(self,pkgd,msg,topic):
     self.pub_num +=1
     text.publisher_obj = msg+'_pub'+str(self.pub_num)
     text.msg_obj = msg +'_obj'+str(self.pub_num)
     text.pkgd = pkgd
     text.topic = topic
     text.msg = msg
     self.msg_pub_list = self.msg_pub_list + text.tagsub(text.publisher[self.lang])
     self.msg_pst_list = self.msg_pst_list + text.tagsub(text.pubcalls[self.lang]) 
     self.msg_obj_list = self.msg_obj_list + text.tagsub(text.msgs[self.lang])
     self.add_includes(pkgd,msg)
  
  def add_subscriber(self,pkgd,msg,topic,cb_name):
    self.sub_num +=1
    text.clb = cb_name
    text.cb_arg = msg
    text.pkgd = pkgd
    text.topic = topic
    text.msg = msg
    text.subscriber_obj= msg+'_sub'+str(self.sub_num)
    self.msg_sub_list = self.msg_sub_list + text.tagsub(text.subscriber[self.lang])
    self.msg_cb_list = self.msg_cb_list + text.tagsub(text.callback[self.lang])
    self.add_includes(pkgd,msg)
  
  def gen_node_source(self):
    print('start to generate the source file for node '+self.node_name+' in language '+self.lang)
    text.node_name = self.node_name
    text.imp_section = self.imp_section
    text.msg_pub_list = self.msg_pub_list
    text.msg_obj_list = self.msg_obj_list
    text.msg_pst_list = self.msg_pst_list 
    text.msg_sub_list = self.msg_sub_list
    text.msg_cb_list = self.msg_cb_list
    text.srv_cb_list = self.srv_cb_list 
    text.srv_adv_list = self.srv_adv_list 
    text.srv_cli_inits = self.srv_cli_inits 
    text.srv_cli_calls = self.srv_cli_calls
    text.pkg = self.get_package_name()
    if self.lang == 'C++':
      filename = self.node_name +'.cpp'
      with open('templates/cpp_template.cpp') as file:
        filetemplate = file.readlines()
    elif self.lang == 'Python':
      filename = self.node_name +'.py'
      with open('templates/pyt2_template.py') as file:
        filetemplate = file.readlines()
    else:
      print('Unknown languange')
    with open(self.node_path+'/'+filename, 'w') as outfile:
      for line in filetemplate:
        outfile.write(text.sectsub(text.tagsub(line)))
      

if __name__ == '__main__':

   a = ros_node('nn','C++','/Users/Danying/Dropbox/ROSworkspace/ros_node_generator/pc')
   a.add_publisher('std_msgs','String','chatter')
   a.gen_node_source()
   
