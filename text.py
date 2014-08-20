
### tags mes
topic = msg = publisher_obj = subscriber_obj = clb = cb_arg = msv = pkg = node_name = pkgd = var_type = msg_obj = msv = ''
### text_elments
# node file
node_name=imp_section = msg_cb_list = msg_sub_list = msg_pub_list = msg_pst_list = msg_obj_list  = msgs_var_list = ''
srv_cb_list = srv_adv_list =srv_cli_inits=srv_cli_calls=''
# manifest
dependency_list = ''
# cmake
msg_gen = srv_gen = exe_list = ''


#####  These are text elements for both languages
subscriber = {'Python' : '$SOB$ = rospy.Subscriber("$TPC$", $MSG$, $CLB$)\n  ',
              'C++'    : 'ros::Subscriber $SOB$ = nh.subscribe("$TPC$", 1000, $CLB$);\n',
             }
callback = {'Python': '''def $CLB$($MSG$): rospy.loginfo("$RNN$: I got message on topic '$TPC$")\n''',
            'C++':  '''void $CLB$(const $PGD$::$MSG$ConstPtr& $MSG$) {
 		                   ROS_INFO("$RNN$: I got message on topic '$TPC$'");
  		                  }\n
		                '''
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

msgs = { 'Python':'$MOB$ = $MSG$()\n  ',
		 'C++': '$PGD$::$MSG$ $MOB$;\n'
	    }

depend = '<depend package="$PGD$"/>\n  '
executable = 'rosbuild_add_executable($RNN$ $RNN$.cpp)\n'


msv_list = '$TYP$       $VAR$\n'


def tagsub(s):
  t = s.replace('$TPC$', topic)           # message topic name
  t = t.replace('$MSG$', msg)             # message name of the .msg
  t = t.replace('$POB$', publisher_obj)     # publisher object
  t = t.replace('$SOB$', subscriber_obj)   # subscriber object
  #t = t.replace('$SRV$', srv)             # service name
  #t = t.replace('$SNM$', srv_name)        # service name
  #t = t.replace('$SPT$', srv_ptr_name)    # service name
  t = t.replace('$CLB$', clb)             # callback name
  t = t.replace('$CBA$', cb_arg)          # callback argument
  t = t.replace('$MSV$', msv)             # a variable in a message
  #t = t.replace('$RWS$', rws)             # ros workspace path
  #t = t.replace('$PKD$', pkd)             # ros package description text
  #t = t.replace('$EML$', email)           # author email
  #t = t.replace('$NAM$', name)            # author name
  #t = t.replace('$LIC$', license)         # license statement (i.e. lgpl)
  t = t.replace('$PKG$', pkg)             # ros package name
  t = t.replace('$RNN$', node_name)       # ros node name
  t = t.replace('$PGD$', pkgd)            # ros dependency package name for certain message
  t = t.replace('$TYP$', var_type)        # message type in the .msg
  t = t.replace('$MOB$', msg_obj)         # message object in .cpp
  t = t.replace('$VAR$', msv)             # message variable in .msg
  return t

### func: insert major sections into the template file
def sectsub(s):
  t = s.replace('$IMPs$', imp_section)     # python import section
  t = t.replace('$MCBs$', msg_cb_list)     # message callbacks
  t = t.replace('$SCBs$', srv_cb_list)     # service server callbacks
  t = t.replace('$SADs$', srv_adv_list)    # service server advertisers
  t = t.replace('$SUBs$', msg_sub_list)    # message subscribers
  t = t.replace('$PUBs$', msg_pub_list)    # message publishers
  t = t.replace('$PBLs$', msg_pst_list)    # message publication statements
  t = t.replace('$SCIs$', srv_cli_inits)   # service client init statements
  t = t.replace('$SCCs$', srv_cli_calls)   # service client calls
  t = t.replace('$DEPs$', dependency_list) # dependency list in manifest.xml
  t = t.replace('$MOBs$', msg_obj_list)    # message objects list if using publishers
  t = t.replace('$MSG_GEN$',msg_gen)       # msg flag in Cmakelist.txt
  t = t.replace('$SRV_GEN$',srv_gen)       # server flag in Cmakelist.txt
  t = t.replace('$EXE$',exe_list)          # executable in CMakelist.txt
  t = t.replace('$VARs$', msgs_var_list)   # message list in .msg
  return t


