import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    sh, sw = stdscr.getmaxyx()
    player_x = sw // 2
    player_y = sh - 2
    bullets = []
    enemies = []
    score = 0
    spawn_timer = 0
    speed = 0.1

    while True:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(player_y, player_x, "^", curses.color_pair(1))
        for bx, by in bullets:
            stdscr.addstr(by, bx, "|")
        for ex, ey in enemies:
            stdscr.addstr(ey, ex, "V", curses.color_pair(2))
        stdscr.addstr(0, 2, f"Score: {score}")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_LEFT and player_x > 1:
            player_x -= 1
        elif key == curses.KEY_RIGHT and player_x < sw - 2:
            player_x += 1
        elif key == ord(" "):
            bullets.append([player_x, player_y - 1])
        elif key == ord("q"):
            break

        bullets = [[bx, by - 1] for bx, by in bullets if by > 1]
        enemies = [[ex, ey + 1] for ex, ey in enemies if ey < sh - 1]

        new_enemies = []
        for ex, ey in enemies:
            hit = False
            for b in bullets:
                if b[0] == ex and b[1] == ey:
                    bullets.remove(b)
                    score += 1
                    hit = True
                    break
            if not hit:
                new_enemies.append([ex, ey])
        enemies = new_enemies

        spawn_timer += 1
        if spawn_timer % 10 == 0:
            enemies.append([random.randint(1, sw - 2), 1])

        for ex, ey in enemies:
            if ey == player_y and ex == player_x:
                stdscr.addstr(sh // 2, sw // 2 - 5, "GAME OVER", curses.A_BOLD)
                stdscr.addstr(sh // 2 + 1, sw // 2 - 7, f"Final Score: {score}")
                stdscr.refresh()
                time.sleep(2)
                return

        time.sleep(speed)

def startGame():
    curses.wrapper(main)
