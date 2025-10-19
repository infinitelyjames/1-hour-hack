import curses
import time
import random
import os
from colorama import init, Fore, Style
import platform
import threading

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
    curses.start_color()
    curses.use_default_colors()

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
    powerups = []  # list of [x, y, type]
    score = 0
    game_over = False
    added_balls = 0
    color_index = 1
    speed = 0.05

    # Power-up effects
    double_points = False
    slow_motion = False
    widen_timer = 0
    effect_timer = 0

    while True:
        stdscr.clear()
        stdscr.border()

        # Draw paddle and balls
        stdscr.attron(curses.color_pair(color_index))
        stdscr.addstr(paddle_y, paddle_x, "=" * paddle_width)
        for ball in balls:
            stdscr.addstr(ball[1], ball[0], "O")
        stdscr.attroff(curses.color_pair(color_index))

        # Draw power-ups
        for px, py, ptype in powerups:
            stdscr.addstr(py, px, ptype)

        # Draw score and active effects
        stdscr.attron(curses.color_pair(color_index))
        stdscr.addstr(0, 2, f" Score: {score} ")
        if double_points:
            stdscr.addstr(0, 20, "⭐ 2X POINTS ⭐")
        if slow_motion:
            stdscr.addstr(0, 40, "🐢 SLOW MOTION 🐢")
        stdscr.attroff(curses.color_pair(color_index))
        stdscr.refresh()

        # Input
        key = stdscr.getch()
        if key == curses.KEY_LEFT and paddle_x > 1:
            paddle_x -= 2
        elif key == curses.KEY_RIGHT and paddle_x < sw - paddle_width - 1:
            paddle_x += 2
        elif key == ord('q'):
            break

        # Move balls
        for ball in balls:
            ball[0] += ball[2]
            ball[1] += ball[3]

            if ball[0] <= 1 or ball[0] >= sw - 2:
                ball[2] *= -1
            if ball[1] <= 1:
                ball[3] *= -1

            # Paddle bounce
            if ball[1] == paddle_y - 1 and paddle_x <= ball[0] <= paddle_x + paddle_width:
                ball[3] *= -1
                points = 2 if double_points else 1
                score += points
                color_index = (color_index % len(colors)) + 1

                # Randomly drop a power-up
                if random.random() < 0.3:
                    ptype = random.choice(["W", "S", "D"])
                    powerups.append([ball[0], 1, ptype])

            # Lose condition
            if ball[1] >= sh - 1:
                game_over = True
                game_over_animation()
                return

        # Move power-ups
        for p in powerups[:]:
            p[1] += 1
            if p[1] >= paddle_y:
                if paddle_x <= p[0] <= paddle_x + paddle_width:
                    # Apply power-up effect
                    if p[2] == "W":
                        paddle_width = min(paddle_width + 4, sw - 4)
                        widen_timer = time.time()
                    elif p[2] == "S":
                        slow_motion = True
                        effect_timer = time.time()
                        speed = 0.1
                    elif p[2] == "D":
                        double_points = True
                        effect_timer = time.time()
                    powerups.remove(p)
                elif p[1] > paddle_y:
                    powerups.remove(p)

        # Power-up effect expiration
        if double_points and time.time() - effect_timer > 10:
            double_points = False
        if slow_motion and time.time() - effect_timer > 5:
            slow_motion = False
            speed = 0.05
        if widen_timer and time.time() - widen_timer > 8:
            paddle_width = max(10, paddle_width - 4)
            widen_timer = 0

        # Add ball every 10 points
        if score // 10 > added_balls:
            balls.append([sw // 2, sh // 2, random.choice([-1, 1]), -1])
            added_balls += 1

        time.sleep(speed)


# -----------------------------------
# GAME OVER SCREEN
# -----------------------------------
def game_over_animation():
    import time
    import os
    from colorama import Fore, Style
    import random

    def play_tune():
        try:
            if platform.system() == "Windows":
                import winsound
                notes = [(440, 200), (660, 200), (330, 300), (550, 300), (440, 400)]
                for freq, dur in notes:
                    winsound.Beep(freq, dur)
                    time.sleep(0.05)
            else:
                for _ in range(5):
                    print("\a", end="", flush=True)
                    time.sleep(0.2)
        except Exception:
            pass

    messages = ["Y O U   L O S T", "HAHAHAHAHAHA!", "BETTER LUCK NEXT TIME!"]
    colors = [Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN, Fore.GREEN]
    os.system('cls' if os.name == 'nt' else 'clear')

    thread = threading.Thread(target=play_tune)
    for i in range(15):
        os.system('cls' if os.name == 'nt' else 'clear')
        color = random.choice(colors)
        print(Style.BRIGHT + color)
        print("\n" * 5)
        for msg in messages:
            print(msg.center(80))
        print("\n" * 3)
        print(color + "💀 HAHA 💀".center(80))
        time.sleep(0.2)
        if i == 0:
            thread.start()
    thread.join()


# -----------------------------------
# RUN GAME
# -----------------------------------
if __name__ == "__main__":
    color_intro()
    curses.wrapper(main)
