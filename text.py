# text elements for ros node generator

### tag general
pkg = node_name = pkgd = ''
### tags message
topic = msg = publisher_obj = subscriber_obj = clb = cb_arg = var_type = msg_obj = msv = ''
### tags services
srv_name = srv = client_obj = server_obj = srv_obj = srv_var = val = arg = ''

### text_elments
# node file
node_name=imp_section = msg_cb_list = msg_sub_list = msg_pub_list = msg_pst_list = msg_obj_list  = msv_init_list = ''
srv_cb_list = srv_adv_list =srv_cli_inits=srv_cli_calls=srv_obj_list=srv_var_list= srv_init_list=''
# manifest
dependency_list = ''
# cmake
msg_gen = srv_gen = exe_list = ''
# .msg
msg_var_list = ''
#.srv
srv_var_list = ''

#####  These are text elements for both languages
subscriber = {'Python' : '$SOB$ = rospy.Subscriber("$TPC$", $MSG$, $CLB$)\n  ',
              'C++'    : 'ros::Subscriber $SOB$ = nh.subscribe("$TPC$", 1000, $CLB$);\n',
             }
msg_callback = {'Python': '''def $CLB$($MSG$): rospy.loginfo("$RNN$: I got message on topic '$TPC$")\n''',
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

imports_msg =  {'Python': 'from $PGD$.msg import $MSG$\n',
                'C++':'#include "$PGD$/$MSG$.h"\n'
               }

imports_srv =  {'Python': 'from $PGD$.srv import $SRV$\n',
                'C++': '#include "$PGD$/$SRV$.h"\n'
               }

advertiser = {'Python' : 'rospy.Service("$SNM$", $SRV$, $CLB$)\n  ',
               'C++' : 'ros::ServiceServer $SER$ = nh.advertiseService("$SNM$", $CLB$);\n'}

srv_callback = {'Python': 'def $CLB$(req): \n  rospy.loginfo("$RNN$: I got service request on name $SNM$, please finish the response.")\n  return True',
                'C++': '''bool $CLB$($PGD$::$SRV$::Request & req, $PGD$::$SRV$::Response & res) {
 		                        ROS_INFO("$RNN$: I got service request on name '$SNM$', please finish the response.");
  		                     return true;}\n
		                   '''
  	           }

clientinits  = {'Python' : '''rospy.wait_for_service("$SNM$")\n  $CLI$ = rospy.ServiceProxy("$SNM$", $SRV$)\n  ''',
               'C++' : 'ros::ServiceClient $CLI$ = nh.serviceClient<$PGD$::$SRV$>("$SNM$");\n'}

clientcalls  = {'Python' : 'try:\n      result = $CLI$($ARG$)\n      print(result)\n    except:print("Something wrong with client call $SNM$")',
               'C++' : '$CLI$.call($SRO$);\n'}

msgs = { 'Python':'$MOB$ = $MSG$()\n  ',
		     'C++': '$PGD$::$MSG$ $MOB$;\n'
	     }
srvs = { 'Python':'$SRO$ = $SRV$()\n  ',
		     'C++': '$PGD$::$SRV$ $SRO$;\n'
	     }

msgs_var_inits = {'Python': '$MOB$.$MSV$ = $VAL$\n  ',
                 'C++': '$MOB$.$MSV$ = $VAL$;\n'
                }
srvs_var_inits= {'Python': '$SRO$.$SVV$ = $VAL$\n  ',
                 'C++': '$SRO$.request.$SVV$ = $VAL$;\n'
                }


depend = '<depend package="$PGD$"/>\n  '
executable = 'rosbuild_add_executable($RNN$ $RNN$.cpp)\n'



# .msg .srv
msv_list = '$TYP$       $MSV$\n'
srv_list = '$TYP$       $MSV$\n'


def tagsub(s):
  #t = t.replace('$RWS$', rws)             # ros workspace path
  #t = t.replace('$PKD$', pkd)             # ros package description text
  #t = t.replace('$EML$', email)           # author email
  #t = t.replace('$NAM$', name)            # author name
  #t = t.replace('$LIC$', license)         # license statement (i.e. lgpl)
  t = s.replace('$PKG$', pkg)             # ros package name
  t = t.replace('$RNN$', node_name)       # ros node name
  t = t.replace('$PGD$', pkgd)            # ros dependency package name for certain message
  t = t.replace('$TPC$', topic)           # message topic name
  t = t.replace('$MSG$', msg)             # message name of the .msg
  t = t.replace('$POB$', publisher_obj)   # publisher object
  t = t.replace('$SOB$', subscriber_obj)  # subscriber object
  t = t.replace('$CLB$', clb)             # callback name
  #t = t.replace('$CBA$', cb_arg)          # callback argument
  t = t.replace('$MOB$', msg_obj)         # message object in node file
  t = t.replace('$TYP$', var_type)        # message type in the .msg
  t = t.replace('$MSV$', msv)              # message variable in .msg
  t = t.replace('$SRV$', srv)             # service name of .srv
  t = t.replace('$SNM$', srv_name)        # service name similar to topic
  t = t.replace('$CLI$',client_obj)       # client object
  t = t.replace('$SER$',server_obj)       # server object
  t = t.replace('$SRO$',srv_obj)          # service object
  t = t.replace('$SVV$',srv_var)          # service variable in .srv
  t = t.replace('$VAL$',val)              # value for service variable
  t = t.replace('$ARG$',arg)              # args for python client call
  #t = t.replace('$SPT$', srv_ptr_name)   # service name
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
  t = t.replace('$MSVs$', msv_init_list)    # message variables in .msg for init
  t = t.replace('$VARs$', msg_var_list)    # message variables in .msg for init
  t = t.replace('$SROs$', srv_obj_list)    # service objects list if using clients
  t = t.replace('$MSG_GEN$',msg_gen)       # msg flag in Cmakelist.txt
  t = t.replace('$SRV_GEN$',srv_gen)       # server flag in Cmakelist.txt
  t = t.replace('$EXE$',exe_list)          # executable in CMakelist.txt
  t = t.replace('$SVVs$',srv_init_list)     # request variable list in .srv for init
  t = t.replace('$SRVs$', srv_var_list)    # message variables in .srv for creating the .srv
  return t


