#!/usr/bin/env python
import os, sys
from readmsgsrv import ros_files

print ('Welcome to ROS node generator  **3**')
print ('Please answer a few questions about your new node:')

################### Function Definition ##########################################################
### func: replace the tags in a string (i.e. one line of source code)
def tagsub(s):
  global msg, sub, sub_object, pub, pub_name, publish_obj, srv_name, scl, callback, cb_arg
  global topic, msv, service, rws, pkd, email, name, license, pkg, pkgd, msg_obj, msg_var
  t = s.replace('$TPC$', topic)           # message topic name
  t = t.replace('$MSG$', msg)             # message name of the .msg
  t = t.replace('$POB$', publish_obj)     # publisher object
  t = t.replace('$SOB$', sub_object)      # subscriber object
  t = t.replace('$SRV$', srv)             # service name
  t = t.replace('$SNM$', srv_name)        # service name
  t = t.replace('$SPT$', srv_ptr_name)    # service name
  t = t.replace('$CLB$', clb)             # callback name
  t = t.replace('$CBA$', cb_arg)          # callback argument
  t = t.replace('$MSV$', msv)             # a variable in a message
  t = t.replace('$RWS$', rws)             # ros workspace path
  t = t.replace('$PKD$', pkd)             # ros package description text
  t = t.replace('$EML$', email)           # author email
  t = t.replace('$NAM$', name)            # author name
  t = t.replace('$LIC$', license)         # license statement (i.e. lgpl)
  t = t.replace('$PKG$', pkg)             # ros package name
  t = t.replace('$RNN$', node_name)       # ros node name
  t = t.replace('$PGD$', pkgd)            # ros dependency package name for certain message
  t = t.replace('$TYP$', var_type)        # message type in the .msg
  t = t.replace('$MOB$', msg_obj)         # message object in .cpp
  t = t.replace('$VAR$', msv)             # message variable in .msg
  return t

### func: insert major sections into the template file
def sectsub(s):
  global imp_section, msg_cb_list, msg_names, srv_cb_list, srv_adv_list, msg_sub_list, msg_pub_list,dependency_list,msg_obj_list
  global msg_pst_list, srv_cli_inits, srv_cli_calls, msg_gen, srv_gen, executable
  t = s.replace('$IMPs$', imp_section)     # python import section
  t = t.replace('$MCBs$', msg_cb_list)     # message callbacks
  #t = t.replace('$MSLl$', msg_names)       # list of message files
  t = t.replace('$SCBs$', srv_cb_list)     # service callbacks
  t = t.replace('$SADs$', srv_adv_list)    # service advertisers
  t = t.replace('$SUBs$', msg_sub_list)    # message subscribers
  t = t.replace('$PUBs$', msg_pub_list)    # message publishers
  t = t.replace('$PBLs$', msg_pst_list)    # message publication statements
  t = t.replace('$SCIs$', srv_cli_inits)   # service client init statements
  t = t.replace('$SCCs$', srv_cli_calls)   # service client calls
  t = t.replace('$DEPs$', dependency_list) # dependency list in manifest.xml
  t = t.replace('$MOBs$', msg_obj_list)    # message objects list if using publishers
  t = t.replace('$MSG_GEN$',msg_gen)       # msg flag in Cmakelist.txt
  t = t.replace('$SRV_GEN$',srv_gen)       # server flag in Cmakelist.txt
  t = t.replace('$EXE$',executable)               # executable in CMakelist.txt
  t = t.replace('$VARs$', msgs_var_list)   # message list in .msg
  return t


### func: abstract the direction of communication to "incoming" or "outgoing"
def pubsub(prompt):
  d= raw_input(prompt) or 'Publisher'
  if d[0]== 'P' or d[0]== 'p':
     d = 'outgoing'
  if d == 'Server':
     d = 'outgoing'
  if d[0]== 'A':
     d = 'outgoing'
  if d[0]== 'S' or d[0]== 's':
     d = 'incoming'
  if d[0]== 'C' or d[0]== 'c':
     d = 'outgoing'
  return d


### func: create .msg file
def gen_msg(path,msg_name):
  print('start to generate the .msg file')
  if not os.path.exists(path+'/'+'msg'): 
    os.makedirs(path+'/'+'msg')
  with open('msgTemplate.msg', 'r') as mfile:    
    m_template = mfile.readlines()
  with open(path+'/'+'msg''/'+msg_name+'.msg', 'w') as outfile: 
    for line in m_template:
			outfile.write(sectsub(tagsub(line)))


### func: create source file .cpp/.py
def gen_source(lang,node_name,path):
  print('start to generate the source code in language '+lang)
  if lang == 'C++':
    filename = node_name +'.cpp'
    with open('cpp_template.cpp') as file:
      filetemplate = file.readlines()
  elif lang == 'Python':
    filename = node_name +'.py'
    with open('pyt2_template.py') as file:
      filetemplate = file.readlines()
  else:
    print('unknown language')
    exit(0)
  out = ""
  for s in filetemplate:   
    out += sectsub(tagsub(s))
  with open(path+'/'+filename, 'w') as outfile:
    for line in out:
      outfile.write(line)


### func: create CMakeList.txt
def gen_cmake(path,msg_flag,srv_flag,node_name,lang):
  global msg_gen, srv_gen, executable
  print('start to generate CMakeList.txt')
  if (msg_flag == 1):
    msg_gen = "rosbuild_genmsg()"
  else:
    msg_gen = "#rosbuild_genmsg()"
  if (srv_flag == 1):
    srv_gen = "rosbuild_gensrv()"
  else:
    srv_gen = "#rosbuild_gensrv()"
  if lang == 'C++':
    executable = "rosbuild_add_executable("+node_name+' '+node_name+'.cpp)'
  else:
    executable = ""
  with open('CMakeListTemplate.txt', 'r') as cfile:
    cm_template = cfile.readlines()
  with open(path+'/'+'CMakeLists.txt', 'w') as outfile:       
    for line in cm_template:
      outfile.write(sectsub(tagsub(line)))


### func: create manifest.xml
def gen_manifest(path):
	print('start to generate manifest.xml')
	with open('manifestTemplate.xml', 'r') as mfile:    
		m_template = mfile.readlines()
	with open(path+'/'+'manifest.xml', 'w') as outfile: 
		for line in m_template:
			outfile.write(sectsub(tagsub(line)))


### func: create Makefile
def gen_mkfile(path):
	print('start to generate Makefile')
	with open('MakefileTemplate', 'r') as mfile:    
		m_template = mfile.readlines()
	with open(path+'/'+'Makefile', 'w') as outfile: 
		for line in m_template:
			outfile.write(sectsub(tagsub(line)))


########################### Variables Definition ##########################
global msg, sub, sub_object, pub, pub_name, publish_obj, srv_name, scl, callback, cb_arg
global topic, msv, service, rws, pkd, email, name, license, pkg
global imp_section, msg_cb_list, msg_names, srv_cb_list, srv_adv_list, msg_sub_list, msg_pub_list
global msg_pst_list, srv_cli_inits, srv_cli_calls


########################### Get System Setup #############################
with open('param_node.py') as pfile:
  initcode = pfile.readlines()
for line in initcode:
  exec (line)
print('got system parameters')


##########################################################################
#  Query user for details
print "------------------- Ros Node Builder ----------------------"
if ros_build_system == 'catkin':
  print "                     (catkin) "
else:
  print "                    (rosbuild)"
  
##  Package name ## 
pkg = raw_input('Enter your package name: ') or pkg
path = rws+pkg
# I think we should flag an error if package does not already exist
if not os.path.exists(path):
  print "This package path does not exist: "+path
  exit(0)
    #os.makedirs(path)

##  Language ## 
lang = raw_input('Enter your language: [Python or C++]: ') or lang
while 1 : 
  if lang[0]=='C' or lang[0]=='c':
     lang = 'C++'
     lang_suff = '.cpp'
     break
  elif lang[0]=='P' or lang[0]=='p':
       lang = 'Python'
       lang_suff = '.py'
       break
  else:
    lang = raw_input('Unknown Language, please re-enter the language type: [Python or C++]: ') or lang

##  Node name ## 
default = pkg + '_node'
node_name = raw_input('Enter your new node name: ['+ default + ']: ') or default
if os.path.exists(path+node_name+lang_suff):
  response = raw_input('node file '+path+node+lang_suff+' already exists.  Are you sure? (Y) ') or 'Y'
  if response != 'Y':
    print 'exiting, please try again'
    exit(0)
    
# initialize strings for output
sub = ''
sub_object  = ''
pub = ''
pub_name = ''
publish_obj = ''
topic = ''
srv_name = ''
service = ''
scl = ''
clb = ''
cb_arg = ''
pkgd = 'std_msgs'
msg_obj = ''
imp_section = ""
srv_ptr_name = ''

##################################################################
# TODO: Generate entries for template 
msg_pst_list = "" 
msg_pub_list = ""
msg_sub_list = ""
msg_cb_list = ""
srv_cb_list = ""
srv_adv_list = ""
srv_cli_inits = ""
srv_cli_calls = ""
dependency_list = ""
msg_obj_list = ""
msg_gen = ""
srv_gen = ""
executable = ""
msgs_var_list = ""

#####  These are text elements for both languages
subscriber = {'Python' : '$SOB$ = rospy.Subscriber("$TPC$", $MSG$, $CLB$)\n  ',
              'C++'    : 'ros::Subscriber $SOB$ = nh.subscribe("$TPC$", 1000, $CLB$);\n',
             }
tmpstr = '''void $CLB$(const $PGD$::$MSG$ConstPtr& $MSG$) {
 		        ROS_INFO("$RNN$: I got message on topic '$TPC$'");
  		    }\n
		      '''
callback = {'Python': '''def $CLB$($MSG$): rospy.loginfo("$RNN$: I got message on topic '$TPC$")\n''',
            'C++': tmpstr
  	       }
publisher =  {'Python': '$POB$  = rospy.Publisher("$TPC$",$MSG$)\n  ',
              'C++':  'ros::Publisher $POB$ = nh.advertise<$PGD$::$MSG$>("$TPC$", 1000);\n',
             }

pubcalls = {'Python' : '$POB$.publish($MOB$)\n    ',
            'C++' : '$POB$.publish($MOB$);\n  '}

imports =  {'Python': 'from $PGD$.msg import $MSG$\n',
            'C++':'#include "$PGD$/$MSG$.h"\n'
           }
advertisers = {'Python' : '''rospy.Service("$SNM$", $PKG$.srv.$SNM$, $CLB$)\n''',
               'C++' : '''ros::ServiceServer service = nh.advertiseService("$SNM$", $CLB$)\n '''}

tmpstr = '''  ros::service::waitForService("$SNM$", -1)
 			  ros::ServiceClient $SPT$ = nh.serviceClient<$PKG$::$SNM$>("$SNM$")
              $PKG$::$SNM$ $SPT$
              $SPT$.arg1 =
              $SPT$.arg2 =
'''
servinits  = {'Python' : '''rospy.wait_for_service("$SNM$")\n$SPT$ = rospy.ServiceProxy("$SNM$", $SNM$)\n''',
               'C++' : tmpstr}

servcalls  = {'Python' : '''result = $SPT$(<<service args>>)\n''',
               'C++' : '''result = $SPT$.call(<<service args>>)\n '''}

#text elements for message objects in .cpp file, TODO check python msgs
msgs = { 'Python':'$MOB$ = $MSG$()\n  ',
		     'C++': '$PGD$::$MSG$ $MOB$;\n'
	     }

#### text elements for manifest.xml  ###
depend = '<depend package="$PGD$"/>\n  '

#### text elements for .msg file ######
msv_list = '$TYP$       $VAR$\n'


pub_num = 0
sub_num = 0
srv_num = 0
CMake_flag_msg_generation = 0
CMake_flag_includes = 0
msg = 'String'
var_type = 'int32'
var_num = 0
msv = ''

######## Messages ##############################################################
while 1:
  resp = raw_input('Do you want to add a message? (y for yes, n/CR for no) ') or -1
  if (resp == -1) or (resp[0]=='n') or (resp[0] == 'N '):
    break
  direction = pubsub('[P]ublish or [S]ubscribe?: ')
  pkgd = raw_input('What is your dependent package [default: '+pkgd+']') or pkgd

  a = ros_files(pkgd)
  a.find_msgs()
  if pkg != pkgd:
    dependency_list = dependency_list + tagsub(depend)

  msg = raw_input('What is your message [default: '+msg+']') or msg
  topic = msg+'_topic'
  topic = raw_input('What is your topic [default: '+topic+']') or topic

  # Subscriber
  if direction == 'incoming':  
    sub_num += 1
    cb_name = msg+'_cb'
    cb_name = raw_input('Name your message callback ['+cb_name+']') or cb_name
    clb = cb_name
    cb_arg = msg
    sub_object = msg+'_sub'+str(sub_num)
    msg_sub_list = msg_sub_list + tagsub(subscriber[lang])
    msg_cb_list = msg_cb_list + tagsub(callback[lang])
  # Publisher 
  else:           
    pub_num += 1
    publish_obj = msg+'_pub'+str(pub_num)
    substr = msg + '.msg'
    #match = [s for s in a.message_list if substr in s]
    if not any(substr in s for s in a.message_list) and pkg==pkgd:
      print('You are going to create a custom message with name '+msg+'...')
      CMake_flag_msg_generation = 1
      while 1:
        res = raw_input('Do you want to add a variable into your message file? (y for yes, n/CR for no) ') or -1
        if (res == -1) or (res[0]=='n') or (res[0] == 'N'):
          break
        else:
          var_num += 1
          var_type = raw_input('What is the type of your message variable '+str(var_num)+', [default: '+var_type+']') or var_type
          msv = 'my_message_var'+ str(var_num)
          msgs_var_list = msgs_var_list + tagsub(msv_list)
      gen_msg(path,msg)
      msgs_var_list = ""
      
    msg_obj = msg + '_obj' +str(pub_num)
    msg_pub_list = msg_pub_list + tagsub(publisher[lang])
    msg_pst_list = msg_pst_list + tagsub(pubcalls[lang]) 
    msg_obj_list = msg_obj_list + tagsub(msgs[lang]) 
		
  imp_section = imp_section + tagsub(imports[lang])	


'''
while 1:
  ##   Services ##############################################################
  resp = raw_input('Do you want to add a service? (y for yes, n/CR for no) ') or -1
  if (resp == -1) or (resp[0]=='n') or (resp[0] == 'N'):
    break
  direction = pubsub('[S]erver or [C]lient?: ');
  # 'topic' same as 'msg'
  service = pkg+'_service'
  srv_name = 'srv_'+str(srv_num)+"_cb"
  srv_name = raw_input('What is your service name? [default: '+service+']') or service
  # should open message file and read the variables!
  srv_ptr_name = tagsub('$SNM$_srv'+str(srv_num))
  if direction == 'incoming':
    cb_name = 'my_service_callback'
    cb_arg = srv_name  #############   ************   CHECK ME ..
    clb = raw_input('Name your service callback ['+cb_name+']') or cb_name
    srv_adv_list = srv_adv_list + tagsub(advertisers[lang])
    srv_cb_list  = srv_cb_list  + tagsub(callback[lang])
  else:  # outgoing service
    srv_cli_inits = srv_cli_inits + tagsub(servinits[lang])
    srv_cli_calls = srv_cli_calls + tagsub(servcalls[lang])
  srv_num += 1
  CMake_flag_msg_generation = 1
  if lang == 'C++':
    CMake_flag_includes = 1
# end of services
'''

############### generate the source file #########################################
gen_source(lang,node_name,path)

############### modify the package manifest.xml ###################################
gen_manifest(path)

############### modify the CMakeList.txt ##########################################
gen_cmake(path,CMake_flag_msg_generation,0, node_name, lang)

############### copy the Makefile #################################################
gen_mkfile(path)


print ('All done. Thanks for using ros_node_gen.py')

