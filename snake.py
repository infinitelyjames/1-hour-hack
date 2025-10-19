import curses
import random
import time
from colorama import init, Fore, Style

init(autoreset=True)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]
    for x in range(box[0][1], box[1][1]):
        stdscr.addstr(box[0][0], x, "#")
        stdscr.addstr(box[1][0]-1, x, "#")
    for y in range(box[0][0], box[1][0]):
        stdscr.addstr(y, box[0][1], "#")
        stdscr.addstr(y, box[1][1]-1, "#")
    snake = [[sh//2, sw//2 + i] for i in range(3)]
    direction = curses.KEY_LEFT
    food = [random.randint(box[0][0]+1, box[1][0]-2), random.randint(box[0][1]+1, box[1][1]-2)]
    score = 0
    while True:
        stdscr.clear()
        for x in range(box[0][1], box[1][1]):
            stdscr.addstr(box[0][0], x, "#")
            stdscr.addstr(box[1][0]-1, x, "#")
        for y in range(box[0][0], box[1][0]):
            stdscr.addstr(y, box[0][1], "#")
            stdscr.addstr(y, box[1][1]-1, "#")
        stdscr.addstr(food[0], food[1], "🍎")
        for i, segment in enumerate(snake):
            stdscr.addstr(segment[0], segment[1], "O" if i==0 else "o")
        stdscr.addstr(box[0][0]-1, box[0][1], f" Score: {score} ")
        stdscr.refresh()
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if (direction == curses.KEY_UP and key != curses.KEY_DOWN) or \
               (direction == curses.KEY_DOWN and key != curses.KEY_UP) or \
               (direction == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
               (direction == curses.KEY_RIGHT and key != curses.KEY_LEFT):
                direction = key
        head = snake[0].copy()
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1
        snake.insert(0, head)
        if head[0] in [box[0][0], box[1][0]-1] or head[1] in [box[0][1], box[1][1]-1] or head in snake[1:]:
            stdscr.addstr(sh//2, sw//2 - 5, Fore.RED + "GAME OVER")
            stdscr.addstr(sh//2+1, sw//2 - 7, f"Final Score: {score}")
            stdscr.refresh()
            time.sleep(2)
            break
        if head == food:
            score += 1
            while True:
                food = [random.randint(box[0][0]+1, box[1][0]-2), random.randint(box[0][1]+1, box[1][1]-2)]
                if food not in snake:
                    break
        else:
            snake.pop()
        time.sleep(0.1)

def startGame():
    curses.wrapper(main)
