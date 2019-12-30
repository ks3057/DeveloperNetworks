# Developer Networks

### OBJECTIVE
To construct a developer network of a Github project and identify influential developers in the network via social network analysis.

### USAGE
There are two files:
1. gitFunctions.py can be run as:
usage: gitFunctions.py [-h] RepositoryPath
**positional arguments:**
  RepositoryPath  complete local path of eclipse che repository
**optional arguments:**
  -h, --help      show this help message and exit
Eg:
 >>python3 gitFunctions.py /path-to-app-repo/che

This will create “filemap.csv” which will be used to run next python file.
It takes about 6 minutes for the execution. (This step can also be skipped if you do not have a clone of the repository on your local machine, as the filemap.csv is provided along with the python files)
2. NetworkxMap.py can be run as:
usage: NetworkxMap.py [-h] filename
**positional arguments:**
filename: The complete path of the file containing: file and committer mapping
**optional arguments:**
  -h, --help  show this help message and exit
Eg:
>>python3 NetworkxMap.py filemap.csv

### EXPERIMENT PART 1: THE DATASET
The Eclipse CHE (Java) Github project is used as the basis for constructing the network.
1. Each committer (unique email ID) is a node.
2. An edge between two committers means that they have both committed at least one file
in common.
3. Edges are undirected and unweighted.
For iterating through each commit, a simple wrapper over GitHub API is used, PyDriller. This provides a method (traverse_commits) to iterate through each commit, which makes extraction of committer name and committer file simpler. A csv file is constructed in this module, where the first column contains the files which have been committed to, and the second column contains committers that have committed to the file. Example:
CompoundIterator.java,mkuznyetsov@codenvy.com skabashnyuk@codenvy.com
This file is used to build the developer network.
Also commits are not always committed by the author. If you work on GitHub.com, you're the author, but GitHub (GitHub <noreply@github.com>) is the committer. So to prevent “noreply@github.com” appearing as the committer email, the author email is used in those cases.

### EXPERIMENT PART 2: CONSTRUCTING THE NETWORK
The developer network is constructed using NetworkX. Each unique committer email id is a node on the network. An edge between two committers if formed if they have both committed to at least one file in common. The graph is undirected and unweighted.

### EXPERIMENT PART 3: ANALYSING THE NETWORK
The network is analysed using three centrality measures:
**Degree Centrality:** The number of links incident upon a node. It is used as measure of a node’s degree of connectedness and hence also influence and/or popularity.
**Betweenness Centrality:** The number of shortest paths that pass through a node divided by all shortest paths in the network. Shows which nodes are more likely to be in communication paths between other nodes.
**Closeness Centrality:** The mean length of all shortest paths from a node to all other nodes in the network. It is a measure of reach, i.e. how long it will take to reach other nodes from a given starting node.

### RESULTS
There are three output files produced by running NetworkxMap.py.
1. developer_edges.txt: A text file where each line represent an edge in the graph in the format "email1:email2" indicating an edge from email1 to email2. ashumilo@redhat.com:okurinny@redhat.com
2. path_graph.pdf: A pdf file displaying a simple graph of the developer network.
![Screenshot 2019-12-30 at 3 46 14 AM](https://user-images.githubusercontent.com/42880317/71574585-5e6ffa00-2ab7-11ea-9bb0-6bbe36afb257.png)


