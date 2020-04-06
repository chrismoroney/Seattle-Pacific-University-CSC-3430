# Creating Community Small Groups

Files included in respository:
- `group1.txt` a file with 16 names
- `group2.txt` a file with 29 names
- `group3.txt` a file with 34 names
- `community_smallgroups.py` file with source of assigning groups per week, using a graph as keeping track of visitations
- `node.py` file that defines a Node in this project
- `requirements.txt` requirements file 
- `smallgroups.txt` output text file that shows the group assignments
- `smallgroups1.txt` example of project run with group1.txt 
- `smallgroups2.txt` example of project run with group2.txt
- `smallgroups3.txt` example of project run with group3.txt 
- `group1Screenshot.png` screenshot of program run with group 1 in groups of 5
- `group2Screenshot.png` screenshot of program run with group 2 in groups of 7
- `group3Screenshot.png` screenshot of program run with group 3 in groups of 8
- `SmallGroups-Graph.pdf` assignment details

# Creating Community Small Groups
A work by Katie Honsinger and Christopher Moroney

## Introduction
In the Christian community, outreach and fellowship are very important parts of showing the love of Jesus Christ. Thus, many churches and communities create small groups in order to share and study the gospel as well as to provide brother/sisterhood in the church community. Part of this fellowship involves meeting many different people. However, it can be difficult for people to meet new people in a community, and it also can be difficult for church leaders to assign groups on a weekly basis while encouraging outreach and meeting new people. This is exactly what out project aims to solve.

## Description	

Using a directed graph, we can define a relationship between a set of people as a person visiting another's house. The nodes of this graph would be the people, and the directed edges indicate who has visited whose house. In order to establish a set of hosts, we switch up the hosts each week in order for every person to be able to eventually visit everyone's houses. We also use various queues to assign people to fill into various houses if they already have visited all of the hosts, or if all of the groups are filled up and there are leftover people. 

This project is a program written in Python that will take in a list of names from a text file (or comma-separated values file) and will assign small groups with hosts for every week, given an inputted group size. The program will take as few weeks as possible for every person to host everyone else, as well as to visit everyone else's home. Married couples will stay together every week (noted as a ',' in the text file for each couple; eg "Mark, Mary" on a single line denotes a couple). The project utilizes a graph in order to track where individuals/couples have visited, so the names from the text file represent nodes, and the directed edge represents whose house they have visited (ie A --> B means A has hosted B). 
	
We also used a queue to maintain the rotation of hosts, as well as queues to assist in filling in groups for people that either need to visit a different host or just to fill up a group for the week. We, Katie and Christopher, believe that our program runs in O(n^2) time with our implementation. The reason why we say that is because we have N nodes, and the graph eventually runs with an empty number of edges to eventually becoming completely dense in the graph. Since we use the graph as a "progress checker" in order to know when to stop and which nodes still need to visit hosts, we know that the number of directed edges is going to be N * (N - 1). Thus, at the very end of the program, when we check the number of edges is going to be N * (N - 1) total edges, we will have approximately N^2 edges, which means that our run time complexity is O(n^2). 

## Requirements
- The program is written in Python
- You will need to be running Python 3 in order to use this program
- We recommend running the program from the command line, but an IDE can also be used to run the program or customize it
- The IDE we used for this project is PyCharm CE. A link to download PyCharm CE is here: 
     - https://www.jetbrains.com/pycharm/download/#section=mac
     - Any type of IDE should be fine, as long as it runs Python 3 and the other two requirements below are installed (also, see the requirements.txt file in this repository)
- pip is needed in order to download other software packages. Instructions to download pip are here: 
     - https://pip.pypa.io/en/stable/installing/ 
     - NOTE: If you have already downloaded Python 2 >=2.7.9 or Python 3 >=3.4 from python.org, you only need to upgrade pip
- Networkx, a third-party library, contains methods and functions for graph implementation. Instructions for downloading can be found here: 
     - https://networkx.github.io/documentation/stable/install.html

## User Manual
[Link to YouTube video here](https://youtu.be/LdWwhwINwyc)

1) Be sure to install pip and the python package networkx onto your computer. The links are found in the requirements section.
    - PyCharm CE is not required, but you need to be running Python 3. For the sake of the user manual, we recommend using Pycharm CE or, even better, the command line.
    
2) Be sure that you are running pip3. Even if pip is already installed onto your machine, double check that it is the Python 3 version. Without this, the correct version of networkx may not install. 

3) After downloading pip, download 3rd-party package networkx. Networkx is a Python package for graphs; the program cannot run without it.

4) Clone this respository, and be able to access the "community_smallgroups.py" and "node.py" files. 

5) Write a plaintext file with the people who will be in your smallgroups. Each name should be on a separate line, except couples will be on a single line separated with a comma. The formatting of this file is crucial; reference group1.txt, group2.txt, or group3.txt for examples. The program will prompt you to input your plaintext file; you can either put this file in the community_smallgroups directory and type in the filename as is, or you can specify the filepath to the file with your people from community_smallgroups. 

6) If you are going to run the program from the command line:
- Navigate to the community_smallgroups directory, which should contain both community_smallgroups.py and node.py
- Your text file with your people also needs to be in this directory, or you can specify the filepath from this directory as detailed in step 5
- From community_smallgroups directory, type "Python community_smallgroups.py" (or Python3 community_smallgroups.py, if that's how you need to run Python3) and follow the prompts. 

7) If you are going to run the program from PyCharm:
-Open PyCharm, and select the folder where the cloned (or downloaded) respository is located. Right-click and select "open with PyCharm." This will open the entire project. 
     - Do not just open up the "community_smallgroups.py" file inside of the respository folder. The program will not be able to run because you need the additional project files and python classes. 
- On PyCharm, click "Run" tab at the top, and then select "edit configuration" when the prompt comes up.
- Select a Python3 interpreter for the "Python Interpretter" option. If you have no interpreter, follow the instructions here to configure one. Click apply, and then run.

8) The program should be running at this point. If not, double check that you have downloaded and upgraded pip, as well as networkx, and redo steps 1-7.

9) The program will prompt you to enter a plaintext file. You can use any of the included "group" text files, or make your own as shown in step 5. If you type a file that doesn't exist, the program will ask you for a new filename. If the file exists but the program can't open it, the program inform you and then end. 

10) The next prompt will be for the group size. Only values greater than 2 (or 1 if your file contains no couples) and less than half the total number of people will produce a sensible result. Any people who don't fit evenly into a group will be added as overflow.
	- If the group size is such that the result of "total people // group size", (which is integer division) is less than the remainder of ( total people // group size ), every group will be bigger than the specified group size. In other words, for best results pick a number slightly above a number that the number of people is divisible by, rather than a number slightly smaller than a number that the total number of people is divisible by. EG if the total number of people is 29 and you pick a group size of 6, the program will create 4 groups because 29//6 is 4. However, there will be 5 leftover people from this assignment and so every group will have 6 people and one will have 7. 
	- If these guidelines are followed, no group shouldn't vary more than +/-1 person from the specified group size. However, sometimes in order to not separate couples, the groups will vary more than this.
	- The program will run as long as the number is an integer

12) The output  will be located in the "smallgroups.txt" file in the respository folder that you downloaded.      
	- Please rename smallgroups.txt to something else, or it will be overwritten the next time you run the program
	
## Reflection
The way that we mimimized number of weeks was essentially to prioritize the people that haven’t visited a host. At the beginning, nobody has visited anyone, so everyone is a “priority” for being placed into a group. However, as we have more and more visitations and iterations, people eventually will see that they have either visited all of the current hosts, or that they only need to visit the groups that are full. Those people (or nodes for the graph) are placed in an auxiliary queue, and will be placed into their groups once the other people have been assigned. For instance, if there are 4 hosts, and Node “Christopher” has visited all 4 hosts, the program will place “Christopher” into a queue, and wait for all other names to be assigned to groups before placing Christopher into a group. This will allow for different nodes to either “fill in” groups or to visit new houses without having to repeat as many times. 

The hosts are chosen by inserting all of the nodes into a list, and then creating a given number of queue such that the same layer of each queue represents all the hosts for one week. For instance, if there are 28 people and we want groups of 7 people, we are telling the program to provide 4 queues of hosts. The program will start by taking the first name from each queue. The queues are created so that each week, the hosts will effectively "shift" by one name to the right, which means that in this instance a person will host for 4 consecutive weeks and then have a break. When we empty the queues, we simply re-generate them. We can re-generate the queues, taking one host from each for every week, as long as we need to to finish the smallgroup assignments.  

The time complexity allowing each person to visit everyone else’s house is O(n^2). The reason for this is because if we use a graph to resemble people as nodes, and directed edges as people visiting another’s home, we will need to achieve a fully connected graph in order for every person to reach everyone else’s home. The exact number of edges is actually going to be (N) * (N - 1) where N is the number of nodes. This is due to the fact that the graph is directed. If the graph was undirected, then we could say that the amount of edges we need to add to the graph is only N * (N - 1) / 2. 

We believe that our algorithm is not the perfect O(n^2), but is pretty close to this. The reason why we say that is because the number of edges required for every person to reach everyone else’s house is N * (N - 1), but sometimes, people will visit other hosts multiple times. Thus, we do not add the same number of edges to the graph for every single iteration. Sometimes, in extreme cases, we may only add one edge to the graph to indicate a person has visited another’s house, but in other cases every single node will add an edge to the graph. Still, all in all, our algorithm will still achieve O(n^2). 

One of the biggest difficulties in this particular problem is coming up with an algorithm that will assign groups with the married couples. The married couples really screw up some of the group proportioning at times, and it is very difficult to deal with sometimes. Thus, sometimes there is an assignment or groups where one group may have more names than others. Being able to account for this was difficult, so what we did was we redefined the Node class specifically just for married couples. What we did was when we read in from the text file that names were on the same line and separated by a comma, they were considered married, but also counted as two people. One of the variables we used was to account for the total number of people in a group, and so when we assigned groups, we would add two people to the group instead of just one. 

