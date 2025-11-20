from typing import List, Tuple, Dict

class WolvesAndDens:
    EMPTY_SPACE = " "
    WOLF = "W"
    DEN = "D"

    def __init__(self, row_wolf_count: List[int], column_wolf_count: List[int], dens: List[Tuple[int, int]]) -> None:
        self.row_wolf_count = row_wolf_count
        self.column_wolf_count = column_wolf_count
        self.dens = dens
        self.wolves = len(self.dens)

        rows = len(self.row_wolf_count)
        cols = len(self.column_wolf_count)

        self.maze = []
        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append(self.EMPTY_SPACE)
            self.maze.append(row)

        for den in self.dens:
            den_row = den[0]
            den_col = den[1]
            self.maze[den_row][den_col] = self.DEN

    def find_spots(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        avail_spots = {}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for den in self.dens:
            ycord = den[0]
            xcord = den[1]
            avail_spots[den] = []

            for direction in directions:
                dy = direction[0]
                dx = direction[1]
                ny = ycord + dy
                nx = xcord + dx

                if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):
                    if self.maze[ny][nx] == self.EMPTY_SPACE:
                        avail_spots[den].append((ny, nx))

        return avail_spots

    def has_adjacent_wolf(self, row: int, col: int) -> bool:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            dy = direction[0]
            dx = direction[1]
            ny = row + dy
            nx = col + dx

            if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]):
                if self.maze[ny][nx] == self.WOLF:
                    return True

        return False

    def solve(self, index: int = 0) -> List[List[str]]:
        if index == len(self.dens):
            result_maze = []
            for row in self.maze:
                new_row = []
                for element in row:
                    new_row.append(element)
                result_maze.append(new_row)
            return result_maze

        rooms = self.find_spots()
        available_spots = rooms[self.dens[index]]

        for spot in available_spots:
            row = spot[0]
            col = spot[1]

            if (self.row_wolf_count[row] > 0 and self.column_wolf_count[col] > 0 and not self.has_adjacent_wolf(row, col)):
                self.maze[row][col] = self.WOLF
                self.row_wolf_count[row] -= 1
                self.column_wolf_count[col] -= 1

                result = self.solve(index + 1)
                if result:
                    return result

                self.maze[row][col] = self.EMPTY_SPACE
                self.row_wolf_count[row] += 1
                self.column_wolf_count[col] += 1

        return None
