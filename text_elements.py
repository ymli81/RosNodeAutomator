#!/usr/bin/env python

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

