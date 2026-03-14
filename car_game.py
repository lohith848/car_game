import random
import time
import os
import msvcrt

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_game(player_lane, player_row, enemies, score, speed, frame, explosion=False):
    print("\033[2J\033[H", end="")

    print("=" * 50)
    print(f"  CAR RACING    Score: {score:4d}  Frame: {frame}")
    print(f"  Speed: {speed:.1f}x")
    print("=" * 50)

    road_height = 15

    for row in range(road_height):

        line = ""

        for col in range(3):

            has_enemy = False

            for ey, elane in enemies:
                if ey == row and elane == col:
                    has_enemy = True
                    break

            is_player = (row == player_row and col == player_lane)

            if explosion and is_player:
                line += "  * *  "
            elif is_player:
                line += "  [X]  "
            elif has_enemy:
                line += "  [V]  "
            else:
                line += "   .   "

        print(f"|{line}|")

    print("=" * 50)
    print("Controls: W=Up S=Down A=Left D=Right Q=Restart E=Exit")


def explosion_animation(player_lane, player_row, enemies, score, speed, frame):
    for _ in range(5):
        draw_game(player_lane, player_row, enemies, score, speed, frame, True)
        time.sleep(0.08)


def run_game():

    road_height = 15

    player_lane = 1
    player_row = road_height - 1

    enemies = []

    score = 0
    speed = 1.0
    frame = 0

    while True:

        frame += 1

        if msvcrt.kbhit():

            key = msvcrt.getch().decode("utf-8").lower()

            if key == 'a' and player_lane > 0:
                player_lane -= 1

            elif key == 'd' and player_lane < 2:
                player_lane += 1

            elif key == 'w' and player_row > 0:
                player_row -= 1

            elif key == 's' and player_row < road_height - 1:
                player_row += 1

            elif key == 'e':
                return "exit"

        draw_game(player_lane, player_row, enemies, score, speed, frame)

        new_enemies = []

        for row, lane in enemies:

            if row < road_height - 1:
                new_enemies.append((row + 1, lane))
            else:
                score += 10

        enemies = new_enemies

        # slower spawning
        if random.random() < 0.12:

            lanes = [0,1,2]

            # avoid blocking all lanes
            occupied_top = {lane for r,lane in enemies if r < 3}

            free_lanes = [l for l in lanes if l not in occupied_top]

            if free_lanes:
                lane = random.choice(free_lanes)
                enemies.append((0, lane))

        # collision
        for row, lane in enemies:
            if row == player_row and lane == player_lane:
                explosion_animation(player_lane, player_row, enemies, score, speed, frame)
                return "restart"

        # slower speed increase
        speed = 1.0 + (score / 300)

        time.sleep(0.20 / speed)


def main():

    while True:

        result = run_game()

        clear_screen()

        if result == "exit":
            print("Thanks for playing!")
            break

        print("=" * 50)
        print("           GAME OVER!")
        print("Press Q to Restart or E to Exit")
        print("=" * 50)

        while True:

            if msvcrt.kbhit():
                key = msvcrt.getch().decode("utf-8").lower()

                if key == "q":
                    break
                elif key == "e":
                    return


if __name__ == "__main__":
    main()