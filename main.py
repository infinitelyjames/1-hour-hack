import curses
import os
import sys

def game_selection(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()
    options = ["Bouncy Ball Game", "Snake Game", "Space Shooter", "Quit"]
    selected = 0

    while True:
        stdscr.clear()
        stdscr.addstr(2, sw//2 - 12, "🎮 SELECT A GAME 🎮")
        for i, option in enumerate(options):
            if i == selected:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(sh//2 - len(options)//2 + i, sw//2 - len(option)//2, f"> {option} <")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(sh//2 - len(options)//2 + i, sw//2 - len(option)//2, option)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(options) - 1:
            selected += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return options[selected]

def launch_bouncy_ball():
    import bouncyball
    bouncyball.startGame()

def launch_snake():
    import snake
    snake.startGame()

def launch_space_shooter():
    import spaceshooter
    spaceshooter.startGame()

if __name__ == "__main__":
    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    choice = curses.wrapper(game_selection)
    curses.endwin()
    os.system('cls' if os.name == 'nt' else 'clear')
    if choice == "Bouncy Ball Game":
        launch_bouncy_ball()
    elif choice == "Snake Game":
        launch_snake()
    elif choice == "Space Shooter":
        launch_space_shooter()
    else:
        print("Goodbye! Thanks for playing!")
        sys.exit()
