import curses
import time
import random

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100 ms

    sh, sw = stdscr.getmaxyx()  # Screen height/width
    paddle_width = 10
    paddle_x = sw // 2 - paddle_width // 2
    paddle_y = sh - 2

    # List of balls; each ball is [x, y, dx, dy]
    balls = [[sw // 2, sh // 2, random.choice([-1, 1]), -1]]

    score = 0
    game_over = False
    added_balls = 0  # Track multiples of 10 to avoid duplicate additions

    while True:
        stdscr.clear()
        stdscr.border()

        # Draw paddle
        stdscr.addstr(paddle_y, paddle_x, "=" * paddle_width)

        # Draw balls
        for ball in balls:
            stdscr.addstr(ball[1], ball[0], "O")

        # Draw score
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

        # Input handling
        key = stdscr.getch()
        if key == curses.KEY_LEFT and paddle_x > 1:
            paddle_x -= 2
        elif key == curses.KEY_RIGHT and paddle_x < sw - paddle_width - 1:
            paddle_x += 2
        elif key == ord('q'):
            break

        # Move balls
        for ball in balls:
            ball[0] += ball[2]  # x
            ball[1] += ball[3]  # y

            # Bounce on walls
            if ball[0] <= 1 or ball[0] >= sw - 2:
                ball[2] *= -1
            if ball[1] <= 1:
                ball[3] *= -1

            # Bounce on paddle
            if ball[1] == paddle_y - 1 and paddle_x <= ball[0] <= paddle_x + paddle_width:
                ball[3] *= -1
                score += 1

            # Lose condition
            if ball[1] >= sh - 1:
                game_over = True

        # Add new ball at multiples of 5
        if score // 5 > added_balls:
            balls.append([sw // 2, sh // 2, random.choice([-1, 1]), -1])
            added_balls += 1

        time.sleep(0.05)

if __name__ == "__main__":
    curses.wrapper(main)
