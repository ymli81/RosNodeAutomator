File Description
- param_node.py: defines system environment, used by rng.py. Do please check this before starting.
- rng.py. Start this file to generate the ros nodes.
- All template files are moved to folder templates.
- rospackage.py: defines class ros_package. dealing with package common files, such cmakelist.txt, manefest.xml msg and srv files.
- rosnode.py: defines class ros_node. dealing with rosnode related file: source file. defines a set of operations to the rosnode when adding publisher/subscriber, client/server to the node.
- readmsgsrv.py: defines class ros_files, dealing with msg and srv. read, load and initialize msg and srv to source file.
- text.py: defines texts and functions for generating the files.

How to Use:
- Set up your ROS workspace and your package (catkin_init_workspace and catkin_create_package - or equivalent rosbuild commands)
- edit param_node.py to set up your ROS workspace and select your build system.  You can set other variables as convenient.
- Run rng.py and follow the instruction to generate the node.
- the program checks the name of rosnodes in the given package, a new node name is asked if the given node name is found.
- To generate the custom msg/srv: enter any index number that is not showing in the msg/srv list or if the msg/srv is empty
- For editing the custom msg/srv: answer the questions when enter that step or you can choose to edit that later.
- names of custom msg/srv will be checked before generating to prevent duplicate names.
- After finishing: roscd into the package, and build . the package should be able to compile w/o error.
- You can customize the templates for site-specific features or requirements.

RosNodeGen
Features:
- ros_build environment
- create a rospackage
- add any number of ros nodes to an existing ros package
- add any number of publishers/subscribers to a ros node
- service intergation
- automatically load and initialize msg/srv variables
- steps for creating custom msg
- steps for creating custom srv
- robust to user input: dealing with random inputs
- python and C++
- auto generation/update CMakelist.txt
- auto generation/update manifest.xml
