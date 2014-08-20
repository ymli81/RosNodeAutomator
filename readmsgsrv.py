#!/usr/bin/env python
import os, sys
import rospkg
import re

class ros_files():
  def __init__(self, pkg):
    self.rospack = rospkg.RosPack()
    self.package_name = pkg
    self.package_path = {}
    self.message_list = []
    self.service_list = []
    self.action_list = []
    self.msgvars = {}
    self.srvvars = {}
    self.package_found = False
  
  def get_package_path(self):
    try:
      self.package_path = self.rospack.get_path(self.package_name)
      self.package_found = True
    except:
      print('cannot find the ros package named '+self.package_name)
      self.package_found = False

  def find_msgs(self):
    self.get_package_path()
    if self.package_found:
      msgdir = self.package_path+'/msg'
      if os.path.exists(msgdir): 
        try: 
          message_list = os.listdir(msgdir)
          print('Find the following messages in the package '+self.package_name+':')
          i = 0;
          sub = '.msg'
          for l in message_list:
            if sub in l:
              i +=1
              self.message_list.append(l)
              print(str(i)+': '+l)
        except:
          print('fail to list the messages')
      else:
        print('cannot find message files in the package '+self.package_name)
      

  def find_srvs(self):
    self.get_package_path()
    servicedir = self.package_path+'/srv'
    if os.path.exists(msgdir): 
      try: 
        self.service_list = os.listdir(servicedir)
      except:
        print('fail to list the service')
    else:
      print('cannot find service files in the package '+self.package_name)

'''
  def load_msgs(self):
    comment_re = re.compile('^[ ]*#')
    pound_re   = re.compile('#')
    divider_re = re.compile('---')
    # load all messages in the package
    for fname in self.message_list:
      tlist = []
      fn = self.path+'/msg/'+fname
      print "Opening: "+fn
      with open(fn, 'r') as msgfile:    
         tmp = msgfile.readlines()
      for l in tmp:
				if (comment_re.match(l) == None):
	  		if (pound_re.search(l) != None):
	   		 #print "I saw an inline comment"
	    	[l, l1] = string.split(l,'#',1)
	  		#print "tmp string: "+l
	  		[ttype, tvar] = string.split(l)
	  		tlist.append( [ttype, tvar])
	 			#print tlist
        self.msgvars[fname] = tlist	
      #print fname+" contains: "
      #for l in self.msgvars[fname]:
        #print l[0] + ' | '+l[1]
      #print ' '
'''
'''    
  def load(self):
    comment_re = re.compile('^[ ]*#')
    pound_re   = re.compile('#')
    divider_re = re.compile('---')
    # load all messages in the package
    for fname in self.message_list:
      tlist = []
      fn = self.path+'/msg/'+fname
      print "Opening: "+fn
      with open(fn, 'r') as msgfile:    
         tmp = msgfile.readlines()
      for l in tmp:
				if (comment_re.match(l) == None):
	  		if (pound_re.search(l) != None):
	   		 #print "I saw an inline comment"
	    	[l, l1] = string.split(l,'#',1)
	  		#print "tmp string: "+l
	  		[ttype, tvar] = string.split(l)
	  		tlist.append( [ttype, tvar])
	 			#print tlist
        self.msgvars[fname] = tlist	
      #print fname+" contains: "
      #for l in self.msgvars[fname]:
        #print l[0] + ' | '+l[1]
      #print ' '
    
    # load all services in the package
    for fname in self.service_list:
      srv_req_list = []
      srv_res_list = []
      req_or_res = 0  # collecting req or result vars?
      fn = self.path+'/srv/'+fname
      print "Opening: "+fn
      with open(fn, 'r') as srvfile:    
         tmp = srvfile.readlines()
      for l in tmp:
	      if (comment_re.match(l) == None):
	      if (pound_re.search(l) != None):
	      #print "I saw an inline comment"
	      [l, l1] = string.split(l,'#',1)
	      print "tmp string: "+l
	      if (divider_re.search(l) != None):
	        req_or_res = 1
	      else:
  	      [ttype, tvar] = string.split(l)
	      if req_or_res == 0:
  	      srv_req_list.append( [ttype, tvar])
  	    else:
	        srv_res_list.append( [ttype, tvar])
	  #print tlist
        self.srvvars[fname] = [srv_req_list, srv_res_list]	
        print fname+" contains: "
        for l in self.srvvars[fname]:
          print l
        print ' '
 '''   
if __name__ == '__main__':
  a = ros_files('std_msgs')
  a.find_msgs()
