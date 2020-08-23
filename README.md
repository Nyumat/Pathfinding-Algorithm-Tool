<p align="center">A* Pathfinding Visualization Tool [WIP]</p>

<b><p align="center">Made by @Nyumat</p></b>

## What the Tool is...
 
 This tool is an interactive, easy to use visualization of the popular A* search algorithm. 
 
 The tool uses the GUI and Keyboard Key access that comes with pygame and creates a plan where "nodes" are to be placed which are essentially points on a grid that, when the program is ran executes the algorithm and displays a optimal  path to the other node. 
 
 This tool is written in Python with the GUI/Alogrithm being developed entirely using the pygame module. 
 
 ## Features 
 
 *Disclaimer: Some of these features aren't completely implemented yet.* 
 
 - Unlimited placeable nodes
 - Colorful GUI
 - Grid Canvas
 - Barriers
 - One click execution usng pygame
 
 ## The Algorithm

__*The A\* Search Algorithm is a path search and graph traversal algorithm.* It is really efficent, and has simple, easy to understand implementation for newbies__

The algorithm works by traversing the lowest-cost tree from the starting "node" to the target node. Because we're working with a grid and can only move in 4 directions, the **Manhattan Distance Heursitic** is the method I used for computing and visualizing the algorithm. 

*It looks like this*

![MDH](mdh.png)

As you can see, the path that the search took was only within the constrains of non-diagonal grid movement. The search's goal is to find paths that are combination of straight line movements. 

Calculating the movement cost that it would take to go from the beginning node to the end node was done by obtaining the sum of absolute values of differences in the first node's x and y coordinates and the ending node's x and y coordinates.

**If we wanted to visualize the calculation with psuedocode it would look like this**

```
movement_cost = abs (current_node.x – goal.x) + abs (current_node.y – goal.y) 
```
Once we're able to compute that cost and evaluate the neighbors of the initially place node, for each neighbor we select the path with the lowest f cost and continue this until we get to the ending node.

*And that's how the algorithm works.*

## Other Random Stuff

For the technical nerds,
>The only drawback of the A* algorithm versus any of the other greedy algorithms is the memory hit. 

>This is pretty true for pretty much all BFS algo's but the bar is so low that it should be able to be executed on current machines.

- This was also my first real DS&A side project, but nonetheless I've learned so much and know I still have a ton to learn.

## License

[MIT License](LICENSE.txt)
