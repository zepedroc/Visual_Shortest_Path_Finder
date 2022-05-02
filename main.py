import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "0", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", "X", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]]


def printMaze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*3, 'X', RED)
            else:
                # j*3 to visually spread the columns
                stdscr.addstr(i, j*3, value, BLUE)


def findStart(maze, startSymbol):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == startSymbol:
                return i, j


def findPath(maze, stdscr):
    start = '0'
    end = 'X'
    startPos = findStart(maze, start)

    # Queue -> First Element to get in is the first to come out
    q = queue.Queue()
    q.put((startPos, [startPos]))

    visited = set()

    while not q.empty():
        currentPos, path = q.get()
        row, col = currentPos

        # Re-draw the screen
        stdscr.clear()
        printMaze(maze, stdscr, path)
        time.sleep(0.1)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row, col)

        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze[r][c] == '#':  # obstacle
                continue

            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)


def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:  # add UP neighbor
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # add DOWN neighbor
        neighbors.append((row + 1, col))
    if col > 0:  # add LEFT neighbor
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # add RIGHT neighbor
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    findPath(maze, stdscr)

    stdscr.getch()  # wait user input to exit program


wrapper(main)
