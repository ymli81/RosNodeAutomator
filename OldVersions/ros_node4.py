#!/usr/bin/python
#  Generate ROS node templates automatically
#

# replace the tags in a string (i.e. one line of source code)
def tagsub(s):
  global msg, sub, sub_object, pub, pub_name, publish_obj, srv_name, scl, callback, cb_arg
  global topic, msv, service, rws, pkd, email, name, license, pkg
  t = s.replace('$TPC$', topic)           # message topic name
  t = t.replace('$MSG$', msg)             # message name
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
  return t

# insert major sections into the template file
def sectsub(s):
  global imp_section, msg_cb_list, msg_names, srv_cb_list, srv_adv_list, msg_sub_list, msg_pub_list
  global msg_pst_list, srv_cli_inits, srv_cli_calls
  t = s.replace('$IMPs$', imp_section)     # python import section
  t = t.replace('$MCBs$', msg_cb_list)     # message callbacks
  t = t.replace('$MSLl$', msg_names)       # list of message files
  t = t.replace('$SCBs$', srv_cb_list)     # service callbacks
  t = t.replace('$SADs$', srv_adv_list)    # service advertisers
  t = t.replace('$SUBs$', msg_sub_list)    # message subscribers
  t = t.replace('$PUBs$', msg_pub_list)    # message publishers
  t = t.replace('$PBLs$', msg_pst_list)    # message publication statements
  t = t.replace('$SCIs$', srv_cli_inits)   # service client init statements
  t = t.replace('$SCCs$', srv_cli_calls)   # service client calls
  return t


print ('Welcome to ROS node generator  **3**')
print ('Please answer a few questions about your new node:')

global msg, sub, sub_object, pub, pub_name, publish_obj, srv_name, scl, callback, cb_arg
global topic, msv, service, rws, pkd, email, name, license, pkg
global imp_section, msg_cb_list, msg_names, srv_cb_list, srv_adv_list, msg_sub_list, msg_pub_list
global msg_pst_list, srv_cli_inits, srv_cli_calls
#  Set a bunch of variables from the parameter file
#Variables
#import param_node

with open('param_node.py') as pfile:
  initcode = pfile.readlines()
for line in initcode:
  exec (line)

###################################################################33
#  Query user for details

pkg = raw_input('Enter your new package name: ') or pkg
default = pkg + '_node'
node_name = raw_input('Enter your new node name: ['+ default + ']: ') or default
lang = raw_input('Enter your language: [Python or C++]: ') or lang

if lang[0]== 'C':
  lang = 'C++'
if lang[0]== 'P':
  lang = 'Python'

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
if lang == 'Python':
  imp_section = 'import rospy\n'
else:
  imp_section = ''' '''
srv_ptr_name = ''


###################################################################33
#  Generate the source code template files with template tag substitution

print ('type [%s], lang [%s]' % (type, lang))

if lang == 'C++':
#  with open(file_base + 'cpp_template.cpp') as file:
  with open('cpp_template.cpp') as file:
    filetemplate = file.readlines()
elif lang == 'Python':
#  with open(file_base + 'pyt2_template.py') as file:
  with open('pyt2_template.py') as file:
    filetemplate = file.readlines()
else:
  print ('Unknown Language, stopping.')
  exit(0)

# abstract the direction of communication to "incoming" or "outgoing"
def pubsub(prompt):
  d= raw_input(prompt) or 'Publisher'
  if d[0]== 'P':
    direction = 'outgoing'
  if d == 'Server':
    d = 'outgoing'
  if d[0]== 'A':
    d = 'outgoing'
  if d[0]== 'S':
    d = 'incoming'
  if d[0]== 'C':
    d = 'outgoing'
  if d[0]== 's':
    d = 'incoming'
  if d[0]== 'c':
    d = 'outgoing'
  return d

# Generate entries for template
msg_pst_list = ""
msg_pub_list = ""
msg_sub_list = ""
msg_cb_list = ""
srv_cb_list = ""
srv_adv_list = ""
srv_cli_inits = ""
srv_cli_calls = ""

#####  These are text elements for both languages
subscriber = {'Python' : 'rospy.Subscriber("$TPC$", $MSG$, $CLB$)\n',
              'C++'    : 'ros::Subscriber $SBO$ = nh.subscribe("$TPC$", 1000, $CLB$);\n',
              }

tmpstr =  '''  void $CLB$(const $PKG$::$MSG$ConstPtr& $MSG$) {
  ROS_INFO("$RNN$: I got message [%s] on topic '$TPC$'\\n", $MSG$->$MSV$);
  }
'''
callback = {'Python': '''def $CLB$($MSG$):
  rospy.loginfo(rosp.get_caller_id()+"I heard %s", $MSG$.$MSV$.c_str())\n\n''',
            'C++': tmpstr
  }

publisher =  {'Python': '$POB$  = rospy.Publisher("$TPC$_topic", $MSG$)\n$MSG$_obj = $MSG$()\n',
            'C++':  'ros::Publisher $POB$ = nh.advertise<$PKG$::$MSG$>("$TPC$", 1000);\n',
            }

pubcalls = {'Python' : '''$MSG$_obj.$MSV$ = "Message Text Here"\n$POB$.publish($MSG$_obj)\n''',
               'C++' : '''$POB$.publish("Message Text");\n'''}

imports =  {'Python': 'from $PKG$.msg import $MSG$\n',
            'C++': '#include <$PKG$/$MSG$.h>\n'
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

pub_num = 0
sub_num = 0
srv_num = 0
msg_names = ''
CMake_flag_msg_generation = 0
CMake_flag_includes = 0
while 1 :
   ##   Messages ##############################################################
  resp = raw_input('Do you want to add a message? (y for yes, n/CR for no) ') or -1
  if (resp == -1) or (resp[0]=='n') or (resp[0] == 'N'):
    break
  direction = pubsub('[P]ublish or [S]ubscribe?: ')
  # 'topic' should not be same as 'msg'
  msg = raw_input('What is your message [default: '+msg+']') or msg
  topic = msg+'_topic'
  topic = raw_input('What is your topic [default: '+topic+']') or topic

  # should open message file and read the variables!
  msg_names = msg_names + msg + '.msg\n'
  if direction == 'incoming':   # Subscriber
    cb_name = msg+'_cb'
    cb_name = raw_input('Name your message callback ['+cb_name+']') or cb_name
    clb = cb_name
    cb_arg = msg
    sub_num += 1
    msg_sub_list = msg_sub_list + tagsub(subscriber[lang])
    msg_cb_list = msg_cb_list + tagsub(callback[lang])
  else:                        # Publisher
    publish_obj = 'pub_obj'+str(pub_num)
    pub_num += 1
    msg_pub_list = msg_pub_list + tagsub(publisher[lang])
    msg_pst_list = msg_pst_list + tagsub(pubcalls[lang])

  imp_section = imp_section + tagsub(imports[lang])
  CMake_flag_msg_generation = 1
  if lang == 'C++':
    CMake_flag_includes = 1

while 1:
  ##   Services ##############################################################
  resp = raw_input('Do you want to add a service? (y for yes, CR for no) ') or -1
  if resp == -1:
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

# generate the output file
if lang == 'Python':
  filename = node_name +'.py'
else:
  filename = node_name +'.cpp'
out=""
for s in filetemplate:    # substitute all the sections
  out += sectsub(tagsub(s))

# output the output file
with open(filename, "w") as outfile:
 for line in out:
   outfile.write(line)

# output step-by-step for modifying CMakeLists.txt (should become automatic!)
if (CMake_flag_includes == 1) or (CMake_flag_msg_generation == 1):
  # generate and output instructions for modification of CMakeLists.txt
  with open('CMakeTemplate.txt', 'r') as cfile:
    cm_template = cfile.readlines()
  with open('CMakeHints.txt', 'w') as outfile:
    for line in cm_template:
      outfile.write(sectsub(tagsub(line)))

print ('All done. Thanks for using ros_node_gen.py')