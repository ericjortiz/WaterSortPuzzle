from enum import Enum
from typing import List, Tuple
import numpy as np

class Color(Enum):
	RED = 0
	ORANGE = 1
	YELLOW = 2
	GRAY = 3
	TEAL = 4
	BLUE = 5
	PINK = 6
	BROWN = 7
	PURPLE = 8
	LIME = 9
	EMERALD = 10
	OLIVE = 11

class WaterSort:
	tubes = [[]]
	def __init__(self, tubes: List[List[Color]]=[[]]):
		self.tubes = tubes
	def solve(self) -> List[str]:
		return self.__solve_helper(self.tubes, [])[2]
	def __solve_helper(self, tubes:List[List[Color]], path:List[Tuple[int, int]]) -> Tuple[bool, List[List[Color]], List[str]]:
		if self.__is_solved(tubes):
			return True, tubes, path
		last_move = None if len(path) == 0 else path[len(path) - 1]
		possible_paths = self.__get_possible_paths(tubes, last_move)
		for idx1, idx2 in possible_paths:
			tubes_cpy = [tube[:] for tube in tubes]
			path_cpy = [p for p in path]
			path_cpy.append((idx1,idx2))
			num_to_move = min(self.__space_remaining_on_tube(tubes[idx2], idx2), self.__num_same_color_on_top(tubes[idx1]))
			colors_to_move = tubes_cpy[idx1][:num_to_move]
			tubes_cpy[idx1] = tubes_cpy[idx1][num_to_move:]
			for color in colors_to_move:
				tubes_cpy[idx2].insert(0, color)
			solved, tubes_cpy, path_cpy = self.__solve_helper(tubes_cpy, path_cpy)
			if solved:
				return True, tubes_cpy, path_cpy
			#return self.__solve_helper(tubes_cpy, path_cpy)
		return False, [[]], [[]]
	def __is_solved(self, tubes: List[List[Color]]) -> bool:
		for tube in tubes:
			if not self.__is_tube_solved(tube):
				return False
		return True
	def __is_tube_solved(self, tube: List[Color]) -> bool:
		if len(tube) == 0:
			return True
		# tubes under length 4 aren't solved
		elif len(tube) < 4:
			return False
		base_color = tube[0]
		for color in tube[1:]:
			if color != base_color:
				return False
		return True
	def __get_possible_paths(self, tubes: List[List[Color]], last_move: Tuple[int,int]=None) -> List[Tuple[int, int]]:
		possible_paths = []
		colors_moved_on_empty_tube = {}
		for i in np.arange(len(tubes)):
			# can't move nothing
			if len(tubes[i]) == 0:
				continue
			# don't move solved tubes
			elif self.__is_tube_solved(tubes[i]):
				continue
			for j in np.arange(len(tubes)):
				num_same_on_top_i = self.__num_same_color_on_top(tubes[i])
				space_remaining_on_j = self.__space_remaining_on_tube(tubes[j], j)
				# can't move to the same location
				if i == j:
					continue
				# can't move on top of a full tube
				elif len(tubes[j]) == 4:
					continue
				# don't move unicolor tube on top of an empty tube
				elif self.__is_unicolor_tube(tubes[i]) and len(tubes[j]) == 0:
					continue
				# don't move back and forth
				elif last_move is not None and last_move[1] == i and last_move[0] == j:
					continue
				# move to an empty tube only if we haven't already added a path to move the same color to an empty tube
				elif len(tubes[j]) == 0 and tubes[i][0] not in colors_moved_on_empty_tube:
					possible_paths.append((i, j))
					colors_moved_on_empty_tube[tubes[i][0]] = True
				elif len(tubes[j]) == 0:
					continue
				# only move onto non-empty tube j if there is enough space for all colors
				elif tubes[i][0] == tubes[j][0] and space_remaining_on_j >= num_same_on_top_i:
					possible_paths.append((i, j))
		return possible_paths
	def __is_unicolor_tube(self, tube: List[Color]) -> bool:
		return len(tube) == self.__num_same_color_on_top(tube)
	def __num_same_color_on_top(self, tube: List[Color]) -> int:
		if len(tube) == 0:
			return 0
		count = 1
		base_color = tube[0]
		for color in tube[1:]:
			if color != base_color:
				return count
			count = count + 1
		return count
	def __space_remaining_on_tube(self, tube: List[Color], index = 0) -> int:
		if index == 14:
			return 1 - len(tube)
		return 4 - len(tube)
