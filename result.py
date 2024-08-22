import functools

from roll import Roll, RollType


@functools.total_ordering
class Result:
    def __init__(self, roll: Roll, num_rolls: int):
        self.roll = roll
        self.num_rolls = num_rolls

    def __eq__(self, other):
        return self.roll == other.roll and self.num_rolls == other.num_rolls

    def __lt__(self, other):
        return (self.roll, -self.num_rolls) < (other.roll, -other.num_rolls)

    def __str__(self):
        return f"{self.roll} ({self.num_rolls} rolls)"

    def value(self) -> int:
        roll_type = self.roll.type()
        if roll_type == RollType.SHOCK_OUT:
            return 13
        elif roll_type == RollType.SHOCK:
            return self.roll.dice[0]
        elif roll_type == RollType.TRIPLET or roll_type == RollType.STRAIGHT:
            return 2
        else:
            return 1
