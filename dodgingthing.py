import curses
import random
import time

def startGame():
    def main(stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        sh, sw = stdscr.getmaxyx()
        player_x = sw // 2
        player_y = sh - 2
        obstacles = []
        score = 0
        speed = 0.1
        spawn_timer = 0

        while True:
            stdscr.clear()
            stdscr.border()
            stdscr.addstr(player_y, player_x, "A")
            for ox, oy in obstacles:
                stdscr.addstr(oy, ox, "#")
            stdscr.addstr(0, 2, f"Score: {score}")
            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_LEFT and player_x > 1:
                player_x -= 1
            elif key == curses.KEY_RIGHT and player_x < sw - 2:
                player_x += 1
            elif key == ord("q"):
                break

            obstacles = [[ox, oy + 1] for ox, oy in obstacles if oy < sh - 1]

            new_obstacles = []
            for ox, oy in obstacles:
                if ox == player_x and oy == player_y:
                    stdscr.addstr(sh // 2, sw // 2 - 5, "GAME OVER", curses.A_BOLD)
                    stdscr.addstr(sh // 2 + 1, sw // 2 - 7, f"Final Score: {score}")
                    stdscr.refresh()
                    time.sleep(2)
                    return
                else:
                    new_obstacles.append([ox, oy])
            obstacles = new_obstacles

            spawn_timer += 1
            if spawn_timer % 5 == 0:
                obstacles.append([random.randint(1, sw - 2), 1])

            score += 1
            time.sleep(speed)

    curses.wrapper(main)
