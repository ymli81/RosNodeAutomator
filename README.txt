
BH: Sat 8/16:
   *  copied "test.py" to "rng.py"  (let's call it rng for "Ros Node Generator" until somebody thinks
             of a really good name for the project).
   *  created a folder for old versions (not strictly nesc. in github but danying made some big refactors so
             I'm just keeping my old version handy for reference).
             
Can somebody edit this file and check / correct the task assignments we agreed on?  
(from my memory):
   Blake:    catkin specific outputs for modifying CMakeLists.txt
             add a flag for catkin/rosbuild selection
             continue drafting the ICRA paper and assign writing sections
             
   Danying:  rosbuild specific outputs
             integrate bh_readmsgsrv.py through an import statement and handle the 
                3 message/service cases
                
   Yangming: learn system and get up to speed. 
   
   Mohammad: testing C++ node outputs. 

------------------------
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
