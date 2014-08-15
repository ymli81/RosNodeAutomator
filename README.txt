Steps to generate ros package/node test.py
1. edit para_node.py, modify the path to your workspace
2. start test.py and follow the instruction to create rospackage/node
3. after creating: run following commands
   roscd $PKG$
   make
   rosrun $PKG$ $RNN$


Features of current version:
1.Create a rospackage with given name and generate a list of files that are required for compile
2.Supports C++ and Python
3.Supports generic and custom msgs, for custom msgs, a msg/ folder will be generated
4.Any number of publishers and subscribers in one ros node
5.One rosnode has only one .cpp file or .py file
6.Supports multiple nodes of Python in one rospackage
