# Food Webs with Graphs

## Problem: Food Webs

### Solution #1: 
<p>Use Dijkstra's Algorithm to find the shortest path from a given prey to a target predator (could be the next one could be the apex predator).</p>

### Solution #2: 
<p>Use Floyd-Warshall's Algorithm to look at one animal in a food web and figure out how long it would take to get to every other animal. This can tell us which animals in a given food web are the most "popular" meaning they are consumed a lot.</p>

### Solution #3: 
<p>Use my own algorithm and the output from Solution #2 to pick out the most common animal. This is useful for figuring out what species of animals is the MOST common in a given ecosystem. In most ecosystems, there tend to be many more prey than predators. Using this algorithm, if we find that a predator is very "popular" it might show that a certain species is overpopulated.</p>

## [Medium Blog Post]()