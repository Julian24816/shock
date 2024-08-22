import functools
import random
import enum


class RollType(enum.IntEnum):
    SHOCK_OUT = 5
    SHOCK = 4
    TRIPLET = 3
    STRAIGHT = 2
    HIGHEST = 1


@functools.total_ordering
class Roll:
    def __init__(self, dice):
        assert len(dice) == 3, "there need to be three dice"
        assert all(1 <= d <= 6 for d in dice), "all dice need to be between 1 and 6"
        self.dice = dice
        self.dice.sort(reverse=True)

    def type(self) -> RollType:
        if self.dice[0] == self.dice[1] == self.dice[2] == 1:
            return RollType.SHOCK_OUT
        elif self.dice[1] == self.dice[2] == 1:
            return RollType.SHOCK
        elif self.dice[0] == self.dice[1] == self.dice[2]:
            return RollType.TRIPLET
        elif self.dice[0] == self.dice[1] + 1 == self.dice[2] + 2:
            return RollType.STRAIGHT
        else:
            return RollType.HIGHEST

    def reroll_keeping(self, first: bool, second: bool, third: bool):
        return Roll([
            self.dice[0] if first else random.randint(1, 6),
            self.dice[1] if second else random.randint(1, 6),
            self.dice[2] if third else random.randint(1, 6),
        ])

    def is_flipping_third_allowed(self):
        return self.dice[0] == self.dice[1] == 6

    def reroll_flipping_third(self):
        assert self.is_flipping_third_allowed(), "rerolling flipping third is only allowed when you have two sixes"
        return Roll([1, random.randint(1, 6), random.randint(1, 6)])

    @staticmethod
    def new_roll():
        return Roll([random.randint(1, 6) for _ in range(3)])

    def __eq__(self, other):
        return self.dice == other.dice

    def __lt__(self, other):
        return (self.type(), self.dice) < (other.type(), other.dice)

    def __str__(self):
        return f"{self.type().name}: {self.dice}"
