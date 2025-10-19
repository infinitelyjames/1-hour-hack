import curses
import time
import random
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def color_intro():
    """
    Displays a rotating-color ASCII intro using colorama before curses starts.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]
    text = [
        "  ____       _ _ _     ____                        ",
        " |  _ \\ __ _| | | |   | __ )  __ _ ___  ___  ___  ",
        " | |_) / _` | | | |   |  _ \\ / _` / __|/ _ \\/ __| ",
        " |  __/ (_| | | | |   | |_) | (_| \\__ \\  __/\\__ \\ ",
        " |_|   \\__,_|_|_|_|   |____/ \\__,_|___/\\___||___/ "
    ]

    for i in range(24):  # Rotate for a few seconds
        os.system('cls' if os.name == 'nt' else 'clear')
        color = colors[i % len(colors)]
        print(color + Style.BRIGHT)
        for line in text:
            print(line.center(80))
        print("\n" + color + f" Loading game{'.' * (i % 4)}".center(80))
        time.sleep(0.2)

    # Countdown before game starts
    for i in range(3, 0, -1):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT)
        print("\n" * 5)
        print(f"{'Starting in ' + str(i) + '...':^80}")
        time.sleep(1)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    paddle_width = 10
    paddle_x = sw // 2 - paddle_width // 2
    paddle_y = sh - 2

    balls = [[sw // 2, sh // 2, random.choice([-1, 1]), -1]]
    score = 0
    game_over = False
    added_balls = 0

    while True:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(paddle_y, paddle_x, "=" * paddle_width)
        for ball in balls:
            stdscr.addstr(ball[1], ball[0], "O")
        stdscr.addstr(0, 2, f" Score: {score} ")
        stdscr.refresh()

        if game_over:
            msg = " GAME OVER! Press 'q' to quit. "
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('q'):
                break
            continue

        key = stdscr.getch()
        if key == curses.KEY_LEFT and paddle_x > 1:
            paddle_x -= 2
        elif key == curses.KEY_RIGHT and paddle_x < sw - paddle_width - 1:
            paddle_x += 2
        elif key == ord('q'):
            break

        for ball in balls:
            ball[0] += ball[2]
            ball[1] += ball[3]
            if ball[0] <= 1 or ball[0] >= sw - 2:
                ball[2] *= -1
            if ball[1] <= 1:
                ball[3] *= -1
            if ball[1] == paddle_y - 1 and paddle_x <= ball[0] <= paddle_x + paddle_width:
                ball[3] *= -1
                score += 1
            if ball[1] >= sh - 1:
                game_over = True

        if score // 10 > added_balls:
            balls.append([sw // 2, sh // 2, random.choice([-1, 1]), -1])
            added_balls += 1

        time.sleep(0.05)

if __name__ == "__main__":
    color_intro()  # Run fancy color intro first
    curses.wrapper(main)
