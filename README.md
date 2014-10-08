RNA - The Ros Node Automator
--------------------------------
(C) 2014, Biorobotics Lab, Department of Electrical Engineering, University of Washington
This file is part of RNA - The Ros Node Automator.

    RNA - The Ros Node Automator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RNA - The Ros Node Automator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with RNA - The Ros Node Automator.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------
 
RNA helps you build the skeleton of a new ROS node quickly from scratch.  You answer questions to specify the package, language, and ROS messages and services of your node, and RNA autogenerates source code and build files.  RNA works by customizing several template files which have included tags.  RNA populates the relevant tags with your answers to its questions.  Of course you have to add in your application logic.
 
File Description
- rng.py. Start this file to generate your ros node.
- param_node.py: defines system environment, used by rng.py. You can place useful defaults in here. Do please check this before starting.
- All template files are moved to folder /templates.
- rospackage.py: defines class ros_package. dealing with package common files, such as CMakelist.txt, manifest.xml msg and srv files.
- rosnode.py: defines class ros_node. dealing with rosnode related files: source file. defines a set of operations to the rosnode when adding publisher/subscriber, client/server to the node.
- readmsgsrv.py: defines class ros_files, dealing with msg and srv. read, load and initialize msg and srv to source file.
- text.py: defines texts and functions for generating the files.

How to Use:
- Use ROS commands to set up your ROS workspace and your package (catkin_init_workspace and catkin_create_package - or equivalent rosbuild commands)
- edit param_node.py to set up your ROS workspace and select your build system.  You can set other variables as convenient.
- Run rng.py and follow the instruction to generate the node.
- the program checks the name of rosnodes in the given package, a new node name is asked if the given node name is found.
- To generate the custom msg/srv: enter any index number that is not showing in the msg/srv list or if the msg/srv is empty
- For editing the custom msg/srv: answer the questions when enter that step or you can choose to edit that later.
- names of custom msg/srv will be checked before generating to prevent duplicate names.
- After finishing: roscd into the package, and build . the package should be able to compile w/o error.
- You can customize the templates for site-specific features or requirements.

RNA Features:
- ros_build and catkin environments
- python or C++ output
- create a rospackage
- add any number of ros nodes to an existing ros package
- add any number of publishers/subscribers to the new ros node
- add any number of service servers/clients to the new ros node
- automatically load and initialize msg/srv variables
- steps for creating custom msg
- steps for creating custom srv
- robust to user input: dealing with random inputs
- auto generation/update CMakelist.txt
- auto generation/update manifest.xml

