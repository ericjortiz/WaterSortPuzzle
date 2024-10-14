# Water Sort Puzzle

## Overview
This project was created to solve levels of the game [Water Sort Puzzle](https://apps.apple.com/us/app/water-sort-puzzle/id1514542157) after I reached level 3145 and tried (in vain) to solve the level on my own. As it turns out, level 3145 is unsolvable without watching an ad to add an extra tube.

## Features
The solver is quite simple. It takes a game state (`List[List[int]]`) as input and outputs the path (`List[Tuple[int, int]]`, e.g. `(1, 12),(2,13),...]`) to the first solution it finds using a [depth first search (DFS)](https://en.wikipedia.org/wiki/Depth-first_search) traversal. 

If a particular level is unsolvable without adding an extra tube, the solver may be slow to finish as it will explore every possible path with only limited deduplication of paths. Perhaps I should have written the solver in a more performant language than Python or added more deduplication to determine there is no solution more quickly. But lists showing unsolvable levels currently exist (e.g. [this](https://www.reddit.com/r/watersortpuzzle/comments/t3ncuv/the_14_levels_that_require_extra_tubes/) one), so it might not be worth the effort to do so. That being said, when a solution does exists, the solver finds a path nearly instantly. What's nearly instantly? ¯\\\_(ツ)\_/¯ <<1 second surely, but I haven't gotten around to measuring it since I've only needed to use this solver to solve a couple of levels.

As I hinted at above, in its current incarnation, the solver is not optimized to find the *shortest* solution, but rather the *first* one it finds. Maybe at some point I will modify the solver to use some other traversal algorithm, but for my use cases DFS works just fine.

Since some levels are unsolvable without adding an extra tube, the solver supports using an extra tube. Set input parameter `extra_tube` to `True` and add an extra empty tube (`[]`) to use the functionality.

A `Color` Enum exists to match ints to Colors, but as long as the numbers associated with each inputted Color are consistent, the solver will work just fine.

Naturally, the solver only works for levels in which all colors are known. That is, it cannot solve levels where colors are unknown unless the user first maps out what all the unknown colors actually are.

## How to Use
Most of these steps are probably redundant for those familiar with cloning repositories and running code in python, but I'll be intentionally verbose in case anyone less familiar comes across this repository.

1. Open your terminal (should be pretty standard for those experienced
2. Clone the repository (how ever you prefer) wherever it's convenient to get the `watersort.py` file, e.g.
```
$ cd ~/Downloads
$ git clone git@github.com:ericjortiz/WaterSortPuzzle.git
```
3. Navigate into the cloned repository
```
$ cd WaterSortPuzzle
```
4. Open an interactive Python shell, e.g.
```
$ python3 -i
```
5. Import the file and set up the level you wish to solve, e.g.
```
$ from watersort import *
$ level = WaterSort([
    [5, 0, 3, 2], [8, 2, 6, 9], [9, 10, 7, 3],
    [2, 1, 10, 6], [0, 10, 6, 7], [0, 0, 9, 9],
    [4, 1, 4, 4], [7, 2, 9, 8], [10, 9, 8, 1],
    [5, 3, 8, 9], [1, 5, 5, 7],[4, 3, 9, 6],[],[],
])
```
6. Solve the level
```
$ level.solve()
```
