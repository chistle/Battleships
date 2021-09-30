import copy
import random


class GameBoard(object):

    def __init__(self, battleships, width, height):
        self.battleships = battleships
        self.shots = []
        self.width = width
        self.height = height

    # * Update battleship with any hits
    # * Save the fact that the shot was a hit or a miss
    def take_shot(self, shot_location):
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:
                is_hit = True
                b.hits[idx] = True
                break

        self.shots.append(Shot(shot_location, is_hit))

    def is_game_over(self):
        return all([b.is_destroyed() for b in self.battleships])

        for b in self.battleships:
            if not b.is_destroyed():
                return False
        return True


class Shot(object):
    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit


class Battleship(object):

    @staticmethod
    def build(head, length, direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i)
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "W":
                el = (head[0] - i, head[1])
            elif direction == "E":
                el = (head[0] + i, head[1])

            body.append(el)

        return Battleship(body)

    def __init__(self, body):
        self.body = body
        # [False, False, False, False]
        self.hits = [False] * len(body)

    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None

    def is_destroyed(self):
        return all(self.hits)


class Player(object):

    def __init__(self, name, shot_f):
        self.name = name
        self.shot_f = shot_f


def render(game_board, show_battleships=False):
    header = "+" + "-" * game_board.width + "+"
    print(header)
    # Construct empty board
    board = []
    for _ in range(game_board.width):
        board.append([None for _ in range(game_board.height)])
    if show_battleships:
        # Add the battleships to the board
        for b in game_board.battleships:
            for x, y in b.body:
                board[x][y] = "O"

    # Add the shots to the board
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            ch = "X"
        else:
            ch = "."
        board[x][y] = ch

    for y in range(game_board.height):
        row = []
        for x in range(game_board.width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(header)


def get_random_ai_shot(game_board):
    x = random.randint(0, game_board.width - 1)
    y = random.randint(0, game_board.height - 1)
    return (x, y)


def get_human_shot(game_board):
    inp = input("Where do you want to shoot?\n")
    # TODO: deal with invalid input
    xstr, ystr = inp.split(",")
    x = int(xstr)
    y = int(ystr)

    return (x, y)


if __name__ == "__main__":
    battleships = [
        Battleship.build((1, 1), 2, "N"),
        # Battleship.build((5, 8), 5, "N"),
        # Battleship.build((2, 3), 4, "E")
    ]

    game_boards = [
        GameBoard(battleships, 10, 10),
        GameBoard(copy.deepcopy(battleships), 10, 10)
    ]

    players = [
        Player("Kiryl", get_human_shot),
        Player("AI", get_random_ai_shot)
    ]

    offencive_idx = 0

    while True:
        # Defensive player is the non-offensive one
        defensive_idx = (offencive_idx + 1) % 2

        defensive_board = game_boards[defensive_idx]
        offensive_player = players[offencive_idx]

        print("%s YOUR TURN!" % offensive_player.name)
        shot_location = offensive_player.shot_f(defensive_board)

        defensive_board.take_shot(shot_location)
        render(defensive_board)

        if defensive_board.is_game_over():
            print("%s WINS!" % offensive_player.name)
            break

        # Offensive player becomes the previous defensive one
        offencive_idx = defensive_idx
