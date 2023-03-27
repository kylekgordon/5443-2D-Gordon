# from game import SpaceRocks
from game import *


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("need player name")
        sys.exit()
    player = sys.argv[1]

    if player == 'player-1':
        otherPlayer = 'player-2'
    else:
        otherPlayer = 'player-1'

    space_rocks = SpaceRocks()
    space_rocks.main_loop()
    space_rocks.main(player, otherPlayer)