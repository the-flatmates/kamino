import random
from enum import Enum
from pathlib import Path

import numpy as np


class Space(Enum):
    RED = "🟥"
    BLUE = "🟦"
    WHITE = "⬜"
    BLACK = "⬛"

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"


class Game:
    HEIGHT = 5
    WIDTH = 5

    def __init__(self) -> None:
        """Game constructor"""
        self.word_list = []
        self.board = np.array([])
        self.key_card = np.array([])

        wl_path = Path(__file__).parent.parent / "data" / "word_list.txt"
        self.parse_word_list(wl_path)
        self.init_board()
        self.draw_key_card()

    def parse_word_list(self, path: Path) -> None:
        """Parse given path as word list.

        Args:
            path (Path): Path to word list file.
        """
        with open(path, "r") as f:
            for line in f.readlines():
                self.word_list.append(line.strip().lower())

    def init_board(self, method: str = "random") -> None:
        """Initialize game board with given method.

        Args:
            method (str, optional): Method for initializing game board.
                Defaults to "random".
        """
        if method == "random":
            self.board = np.array(
                random.sample(self.word_list, self.HEIGHT * self.WIDTH)
            ).reshape((self.HEIGHT, self.WIDTH))

    def draw_key_card(self) -> None:
        """Draw random key card"""

        key_card = []

        # Randomize what team goes first
        if random.randint(0, 1):
            key_card.extend([Space.RED] * 9)
            key_card.extend([Space.BLUE] * 8)
        else:
            key_card.extend([Space.RED] * 8)
            key_card.extend([Space.BLUE] * 9)

        key_card.extend([Space.WHITE] * 7)
        key_card.append(Space.BLACK)

        # Shuffle key card list
        np.random.shuffle(key_card)

        self.key_card = np.array(key_card).reshape((self.HEIGHT, self.WIDTH))

    def __str__(self) -> str:
        template = "| {0:^12s} | {1:^12s} | {2:^12s} | {3:^12s} | {4:^12s} |"
        repr = ""
        for row in range(len(self.board)):
            repr += template.format(*self.board[row]) + "\n"

        return repr

    def __repr__(self) -> str:
        template = "| {0:^12s} | {1:^12s} | {2:^12s} | {3:^12s} | {4:^12s} |"
        repr = ""
        for row in range(len(self.board)):
            repr += template.format(*self.board[row]) + "\n"

        return repr
