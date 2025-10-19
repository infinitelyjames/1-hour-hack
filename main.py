import curses
import time
import random
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# -----------------------------------
# COLORFUL LOADING INTRO
# -----------------------------------
def color_intro():
    os.system('cls' if os.name == 'nt' else 'clear')

    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.BLUE]
    text = [
        "  ____       _ _ _     ____                        ",
        " |  _ \\ __ _| | | |   | __ )  __ _ ___  ___  ___  ",
        " | |_) / _` | | | |   |  _ \\ / _` / __|/ _ \\/ __| ",
        " |  __/ (_| | | | |   | |_) | (_| \\__ \\  __/\\__ \\ ",
        " |_|   \\__,_|_|_|_|   |____/ \\__,_|___/\\___||___/ "
    ]

    for i in range(24):
        os.system('cls' if os.name == 'nt' else 'clear')
        color = colors[i % len(colors)]
        print(color + Style.BRIGHT)
        for line in text:
            print(line.center(80))
        print("\n" + color + f" Loading game{'.' * (i % 4)}".center(80))
        time.sleep(0.2)

    for i in range(3, 0, -1):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + Style.BRIGHT)
        print("\n" * 5)
        print(f"{'Starting in ' + str(i) + '...':^80}")
        time.sleep(1)


# -----------------------------------
# MAIN GAME
# -----------------------------------
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    # Initialize color pairs
    curses.start_color()
    curses.use_default_colors()

    # Create several color pairs (if supported)
    colors = [
        curses.COLOR_RED, curses.COLOR_YELLOW,
        curses.COLOR_GREEN, curses.COLOR_CYAN,
        curses.COLOR_MAGENTA, curses.COLOR_BLUE
    ]
    for i, c in enumerate(colors, start=1):
        curses.init_pair(i, c, -1)

    sh, sw = stdscr.getmaxyx()
    paddle_width = 10
    paddle_x = sw // 2 - paddle_width // 2
    paddle_y = sh - 2

    balls = [[sw // 2, sh // 2, random.choice([-1, 1]), -1]]
    score = 0
    game_over = False
    added_balls = 0
    color_index = 1  # Start with color pair 1

    while True:
        stdscr.clear()
        stdscr.border()

        # Draw paddle and balls with current color
        stdscr.attron(curses.color_pair(color_index))
        stdscr.addstr(paddle_y, paddle_x, "=" * paddle_width)
        for ball in balls:
            stdscr.addstr(ball[1], ball[0], "O")
        stdscr.attroff(curses.color_pair(color_index))

        # Draw score
        stdscr.attron(curses.color_pair(color_index))
        stdscr.addstr(0, 2, f" Score: {score} ")
        stdscr.attroff(curses.color_pair(color_index))
        stdscr.refresh()

        if game_over:
            msg = " GAME OVER! Press 'q' to quit. "
            stdscr.attron(curses.color_pair(color_index))
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.attroff(curses.color_pair(color_index))
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('q'):
                break
            continue

        # Player input
        key = stdscr.getch()
        if key == curses.KEY_LEFT and paddle_x > 1:
            paddle_x -= 2
        elif key == curses.KEY_RIGHT and paddle_x < sw - paddle_width - 1:
            paddle_x += 2
        elif key == ord('q'):
            break

        # Move each ball
        for ball in balls:
            ball[0] += ball[2]
            ball[1] += ball[3]

            # Bounce off walls
            if ball[0] <= 1 or ball[0] >= sw - 2:
                ball[2] *= -1
            if ball[1] <= 1:
                ball[3] *= -1

            # Paddle collision
            if ball[1] == paddle_y - 1 and paddle_x <= ball[0] <= paddle_x + paddle_width:
                ball[3] *= -1
                score += 1
                # Change color on every score
                color_index = (color_index % len(colors)) + 1

            # Lose condition
            if ball[1] >= sh - 1:
                game_over = True

        # Add new ball every 10 points
        if score // 10 > added_balls:
            balls.append([sw // 2, sh // 2, random.choice([-1, 1]), -1])
            added_balls += 1

        time.sleep(0.05)


# -----------------------------------
# RUN GAME
# -----------------------------------
if __name__ == "__main__":
    color_intro()  # Fancy color intro before curses
    curses.wrapper(main)
