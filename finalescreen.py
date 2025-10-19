import curses
import random
import time

def finale_screen(score):
    def main(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(False)
        curses.start_color()
        curses.use_default_colors()
        colors = [curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_YELLOW,
                  curses.COLOR_BLUE, curses.COLOR_MAGENTA, curses.COLOR_CYAN, curses.COLOR_WHITE]
        for i, color in enumerate(colors, start=1):
            curses.init_pair(i, color, -1)
        sh, sw = stdscr.getmaxyx()

        messages = [
            "🎉 CONGRATULATIONS! 🎉",
            f"YOUR FINAL SCORE: {score}",
            "YOU ARE AWESOME!",
            "THANKS FOR PLAYING!"
        ]

        confetti_chars = ["*", "+", "x", "o", "@", "#", "%"]

        for frame in range(30):
            stdscr.clear()
            for y in range(sh):
                for x in range(sw):
                    if random.random() < 0.02:
                        char = random.choice(confetti_chars)
                        color = random.randint(1, len(colors))
                        stdscr.addstr(y, x, char, curses.color_pair(color) | curses.A_BOLD)
            for i, msg in enumerate(messages):
                color = random.randint(1, len(colors))
                stdscr.addstr(sh//2 - len(messages)//2 + i, sw//2 - len(msg)//2, msg, curses.color_pair(color) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.1)

        stdscr.addstr(sh-2, sw//2 - 15, "Press any key to return to the menu...")
        stdscr.getch()

    curses.wrapper(main)
