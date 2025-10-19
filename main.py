import curses
import time
import random

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Don't block on getch()
    stdscr.timeout(100)  # Refresh every 100 ms

    sh, sw = stdscr.getmaxyx()  # Screen height/width
    paddle_width = 10
    paddle_x = sw // 2 - paddle_width // 2
    paddle_y = sh - 2

    ball_x = sw // 2
    ball_y = sh // 2
    ball_dx = random.choice([-1, 1])
    ball_dy = -1

    score = 0
    game_over = False

    while True:
        stdscr.clear()

        # Draw borders
        stdscr.border()

        # Draw paddle
        stdscr.addstr(paddle_y, paddle_x, "=" * paddle_width)

        # Draw ball
        stdscr.addstr(ball_y, ball_x, "O")

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

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Bounce on walls
        if ball_x <= 1 or ball_x >= sw - 2:
            ball_dx *= -1
        if ball_y <= 1:
            ball_dy *= -1

        # Bounce on paddle
        if ball_y == paddle_y - 1 and paddle_x <= ball_x <= paddle_x + paddle_width:
            ball_dy *= -1
            score += 1

        # Lose condition
        if ball_y >= sh - 1:
            game_over = True

        time.sleep(0.05)


if __name__ == "__main__":
    curses.wrapper(main)
