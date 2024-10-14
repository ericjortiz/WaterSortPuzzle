from copy import copy
from enum import Enum
from typing import List, Tuple, Union

class Color(Enum):
    RED:     int = 0
    ORANGE:  int = 1
    YELLOW:  int = 2
    GRAY:    int = 3
    TEAL:    int = 4
    BLUE:    int = 5
    PINK:    int = 6
    BROWN:   int = 7
    PURPLE:  int = 8
    LIME:    int = 9
    EMERALD: int = 10
    OLIVE:   int = 11

class Tube:
    """ Class Tube represents a tube in a WaterSort level"""
    
    max_capacity = 4
    min_capacity = 1

    def __init__(self, colors: List[Color]=[], capacity: int = 4):
        """ Initializes a Tube for use in a WaterSort level

        This function accepts a list of colors and (optionally) a
        capacity and determines whether the tube is solved, the
        tube's remaining space, and the number of the same color
        on top of the tube to use in typical Tube operations. 

        This function throws an exception if the inputted capacity
        is not 4 (standard tube) or 1 (extra tube), or if the length 
        of the inputted list of colors is greater than the capacity

        Args:
            colors (List[Color]): the colors this tube holds
            capacity (int): the number of colors that this tube can hold

        Returns:
            None

        """
        if colors is None: # special case for copying an empty tube
            colors = []

        if capacity != self.min_capacity and capacity != self.max_capacity:
            raise Exception(
                "Cannot initialize Tube with capacity {0}".format(
                    capacity, 
                    self.max_capacity
                )
            )
        elif len(colors) > self.max_capacity:
            raise Exception(
                "Cannot initialize Tube with {0} colors > capacity {1}".format(
                    len(colors),
                    capacity
                )
            )
        self._colors = colors
        self._capacity = capacity

    def __len__(self) -> int:
        """ Returns the amount of water on the tube

        Args:
            None

        Returns:
            int: the amount of water on the tube

        """
        return len(self._colors)

    def __getitem__(self, indices):
        """ Returns the color(s) in the tube at position(s) indices

        Args:
            indices: int or slice

        Returns:
            Color or list of Colors

        """
        if len(self) == 0:
            return None
        return self._colors[indices]

    def __copy__(self):
        """ deep copy the Tube

        Args:
            None

        Returns:
            Tube: a deep copy of the tube
            
        """
        return Tube(self[:], self._capacity)

    def is_solved(self) -> bool:
        """ Determines whether the Tube is solved

        Args:
            None

        Returns:
            bool: whether the tube is solved
            
        """
        return len(self) == 0 or (len(self) == 4 and self.is_unicolor())
    def is_unicolor(self) -> bool:
        """ Determines whether the Tube is length 0 or entirely one color

        Args:
            None

        Returns:
            bool: whether the tube is unicolor
        """
        return len(self) > 0 and len(self) == self.num_same_color_on_top()

    def num_same_color_on_top(self):
        """ Returns the number of matching colors on top of the tube

        Args:
            None

        Returns:
            int: the number of matching colors on top of the tube

        """
        if len(self) == 0:
            return 0
        base_color, count = self[0], 1
        for color in self[1:]:
            if color != base_color:
                return count
            count = count + 1
        return count
    def peek(self) -> List[Color]:
        """ Returns the top matching colors on the tube without modifying it

        For example, if a tube has 2 emeralds on top of 2 reds, peek
        will return a list of 2 emeralds without modifying the tube

        Args:
            None

        Returns:
            List[Color]: the top matching colors on the tube

        """
        return self[:self.num_same_color_on_top()]

    def pop(self, num_to_move: int = None) -> List[Color]:
        """ Returns the top matching colors on the tube while modifying the tube

        For example, if a tube has 2 emeralds on top of 2 reds, pop
        will return a list of 2 emeralds and only contain 2 reds

        Args:
            None

        Returns:
            List[Color]: the top matching colors on the tube

        """
        if num_to_move is None:
            num_to_move = self.num_same_color_on_top()
        colors_on_top = self[:num_to_move]
        self._colors = self[num_to_move:]
        return colors_on_top

    def can_insert(self, colors: List[Color]) -> bool:
        """ Determines whether arg colors can be added onto the tube

        colors can be added when there is 1 unique color, the number
        of slots to fill is less than or equal to the remaining space
        on the tube, and the tube's top color matches the color to add

        Args:
            None

        Returns:
            bool: whether arg colors can be added onto the tube

        """
        if len(colors) == 0:
            return False
        elif len(self) > 0 and self[0] != colors[0]:
            return False
        for color in colors[1:]:
            if color != colors[0]:
                return False
        return len(colors) <= self._capacity - len(self)

    def insert(self, colors: List[Color]):
        """ Inserts colors onto the tube, if the insertion is valid

        An insertion is valid if there is exactly 1 unique color 
        added, the number of colors that will be added is less 
        than or equal to the remaining space on the tube, and the 
        tube's top color matches the unique color being added

        insert throws an exception if an insertion is invalid. can_insert
        should be used beforehand to ensure the requested insertion is valid
        
        Args:
            colors (List[Color]): the list of colors to add to the tube
        Returns:
            None

        """
        if not self.can_insert(colors):
            raise Exception(
                "{0} cannot be added onto Tube of {1} w/ capacity {2}".format(
                    colors,
                    self._colors,
                    self._capacity
                )
            )
        colors.extend(self._colors)
        self._colors = colors

class WaterSort:
    """ Class WaterSort represents a level of the WaterSort puzzle game. """

    def __init__(
        self, 
        tubes_of_ints: List[List[int]]=[[]], 
        extra_tube: bool = False,
    ):
        """ Initializes a level of the WaterSort game

        This function accepts a list of lists of type int, which
        represent the colors for the level, and (optionally) a
        boolean indicating whether an extra tube is being used.
        If arg extra_tube is True, the capacity of the final tube
        will be initialized to 1. Most levels will not require an
        extra tube, but some (rare) levels are unsolvable without one.
        Other tubes are initialized with the standard capacity of 4.

        Args:
            tubes_of_ints (List[List[int]]): the initial setup of the level
            extra_tube (bool): whether the last tube of ints is an extra tube

        Returns:
            None

        """
        self.tubes = []
        for i, tube in enumerate(tubes_of_ints):
            tube_of_colors = []
            for color_int in tube:
                tube_of_colors.append(Color(color_int))
            if i == len(tubes_of_ints) - 1 and extra_tube:
                self.tubes.append(Tube(tube_of_colors), 1)
            else:
                self.tubes.append(Tube(tube_of_colors))

    def solve(self) -> Union[List[str], str]:
        """ Finds a solution to the WaterSort level, if one exists

        This function uses a depth first search (DFS) retrieval to
        find a solution to the level. If no solution exists, solve will
        output "No solution found." In that case, an extra tube will
        likely be required to solve the level. Otherwise, there is
        probably a mistake in how the colors for the level are inputted.
        
        Args:
            None
        Returns:
            Union[List[str], str]: list of moves to make, or "No solution found"

        """
        solved, path = self.__solve_helper(self.tubes)
        if solved:
            return path
        return "No solution found"

    def __solve_helper(
        self,
        tubes: List[Tube],
        path:List[Tuple[int, int]] = [], 
    ) -> Tuple[bool, List[str]]:
        """ The internal helper function to solve the level.

        This function accepts a list of tubes and recursively explores
        possible paths until a solution is found. At which point, it will
        return a string representation of the path to the solution. 
        
        Args:
            tubes (List[Tube]): the state of the level at the current state
            path (List[Tuple[int, int]]): the path to the current state
        Returns:
            bool: whether a solution was found
            List[str]]: the path to the solution (if one was found), or []

        """
        if WaterSort.__is_solved(tubes):
            return True, path
        for idx1, idx2 in self.__get_possible_paths(tubes):
            tubes_cpy = [copy(tube) for tube in tubes]
            path_cpy = [p for p in path]

            path_cpy.append((idx1,idx2))
            tubes_cpy[idx2].insert(tubes_cpy[idx1].pop())

            solved, path_cpy = self.__solve_helper(tubes_cpy, path_cpy)
            if solved:
                return True, path_cpy
        return False, [[]]

    @staticmethod
    def __is_solved(tubes: List[Tube]) -> bool:
        """ Determines whether the list of tubes represents a solution

        This function returns True if each Tube in the list
        of provided tubes is solved, and False otherwise.
        
        Args:
            tubes (List[Tube]): the current state of the tubes
        Returns:
            bool: whether all tubes in the list are solved

        """
        for tube in tubes:
            if not tube.is_solved():
                return False
        return True

    def __get_possible_paths(self, tubes: List[Tube]) -> List[Tuple[int, int]]:
        """ Returns the possible paths based on the provided list of tubes

        This function accepts a list of tubes and returns possible paths
        that can be made from the given list. For example, if the only
        valid move is from tube 0 to tube 4, the function will return
        [(0, 4)]. To limit the solution space and avoid infinite loops,
        we don't consider moves from empty tubes anywhere, one tube to
        itself, or unicolor tubes anywhere. If there is more than one
        empty tube, we also only consider placing each tube onto exactly
        one of the empty tubes to avoid exploring the same path twice.
        
        Args:
            tubes (List[Tube]): the current state of the tubes
        Returns:
            List[Tuple[int, int]]: the possible paths that can be explored

        """
        possible_paths = []
        colors_in_unicolor_tubes = {}
        for tube in tubes:
            if tube.is_unicolor():
                colors_in_unicolor_tubes[tube[0]] = True
        for i, tube_i in enumerate(tubes):
            empty_tubes_considered_i = {}
            if len(tube_i) == 0: # don't move empty tubes
                continue
            elif tube_i.is_solved(): # don't move solved tubes
                continue
            for j, tube_j in enumerate(tubes):
                if i == j:
                    continue
                if tube_j.can_insert(tube_i.peek()):
                    if len(tube_j) == 0:
                        if tube_i[0] in colors_in_unicolor_tubes:
                            # don't move tube i onto empty tube j if there's
                            # another tube matching the color(s) on tube i
                            continue
                        elif tube_i[0] in empty_tubes_considered_i:
                            # consider moving tube i onto at most one empty tube
                            continue
                        empty_tubes_considered_i[tube_i[0]] = True
                    possible_paths.append((i, j))
        return possible_paths
