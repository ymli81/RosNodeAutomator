#!/usr/bin/env python
import os, sys
import string
import re

class ros_files():
  def __init__(self, pkg, ws_path):
    self.path = ws_path
    self.package_name = pkg
    self.message_list = []
    self.service_list = []
    self.action_list = []
    self.msgvars = {}
    self.srvvars = {}
    
  def find(self):
    msgdir = self.path+'/msg/'
    servicedir = self.path+'/srv'
    try: 
      self.message_list = os.listdir(msgdir)
    except:
      x=5   # dummy statement
    try:
      self.service_list = os.listdir(servicedir)
    except:
      x=5   # dummy statement
    
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
    
      
  
a = ros_files('pkgn', '/home/blake/Projects/generator')
a.find()
for l in a.message_list:
  print "File name: "+l

a.load()
  
exit(1)

  #if (msa_selection != '.msg') and (msa_selection != '.srv'): 
    #print "Illegal msa_selction (file type)"
    #exit(0)
  #else:
    #filename = 
    #try:
      #f = open()
    #except IOError:
      #print 'Oh dear.'