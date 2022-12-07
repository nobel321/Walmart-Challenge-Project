# Walmart-Challenge-Project:
This is a prototype of a pathfinding algorithm to give a visual representation of an aspect of the pathfinding algorithms that our idea would include to return an *optimal* and *personalized* path through the Walmart store to find products.

## Implementation Details:
- Imports: pygame, math, queue (PriorityQueue)   
- Pathfinding Algorithm: *A-Star Pathfinding Algorithm* (https://en.wikipedia.org/wiki/A*_search_algorithm)  
- Comments on implementation are included in code

## Tips for navigating code:
`Line 1-4 >> a few details on function of program`
`Line 5-14 >> navigation details for navigating code`
`Line 16-18 >> imports`
`Line 20-22 >> window setup`
`Line 24-34 >> colours`
`Line 43-110 >> node class`
`Line 112-117 >> heuristic function`
`Line 125-167 >> algorithm`
`Line 210 >> number of rows/columns (change)`
`Line 209-260 >> main function`

## Usage Details:
1. clone repository (`git clone https://github.com/<repo-name>/.git`)
>*To run code...*
2. open IDE/terminal prompt
3. find directory where code is
4. run code using `python nav_algorithm.py` for Linux/Mac or `python .\nav_algorithm.py` for Windows
>*To use program...*
5. select a single *grid tile*/node to set the starting point of the algorithm
6. select another single *grid tile*/node to set the ending point of the algorithm
7. left-click on touch pad or mouse to place barrier nodes
8. right-click on touch pad or mouse to delete barrier nodes
9. enter to begin algorithm
10. ENJOY!

## Colour Key (Legend):
```diff
Orange (🟧) = starting point
Blue (🟦) = ending point
Red (🟥) = node check
Green (🟩) = node check open
Purple (🟪) = best path
Black (⬛) = barriers/closed nodes
White (⬜) = space/open nodes
```
