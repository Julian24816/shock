from abc import ABC, abstractmethod

from result import Result
from roll import Roll, RollType
from typing import Tuple


class Action:
    @staticmethod
    def keep_all():
        return Action(False, (True, True, True))

    @staticmethod
    def flip_third():
        return Action(True, (False, False, False))

    @staticmethod
    def keep(dice: Tuple[bool, bool, bool]):
        return Action(False, dice)

    @staticmethod
    def keep_none():
        return Action(False, (False, False, False))

    def __init__(self, flip_third: bool, keep_dice: Tuple[bool, bool, bool]):
        self.flip_third = flip_third
        self.keep_dice = keep_dice

    def __str__(self):
        return "stop" if all(self.keep_dice) else "flip third" if self.flip_third else f"keep dice: {self.keep}"


class Agent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def play(self, current_roll: Roll, current_roll_num: int, rolls_left: int, worst_prev_result: Result = None,
             verbose: bool = False) -> Action:
        pass

    @abstractmethod
    def __str__(self):
        return self.name + " (Unknown Agent)"


class SimpleAgent(Agent):
    def play(self, current_roll: Roll, current_roll_num: int, rolls_left: int, worst_prev_result: Result = None,
             verbose: bool = False) -> Action:
        is_first_player = worst_prev_result is None

        if current_roll.type() == RollType.SHOCK_OUT:
            if verbose:
                print(self.name, "rolled SHOCK OUT, stopping")
            return Action.keep_all()

        if is_first_player:
            if current_roll.type() > RollType.HIGHEST:
                if verbose:
                    print(self.name, f"rolled {current_roll.type().name}, stopping")
                return Action.keep_all()
            elif current_roll.is_flipping_third_allowed():
                return Action.flip_third()
            elif min(current_roll.dice) == 5:
                if verbose:
                    print(self.name, "good enough, stopping")
                return Action.keep_all()
            else:
                return Action.keep([dice >= 5 for dice in current_roll.dice])

        else:
            if current_roll > worst_prev_result.roll:
                if verbose:
                    print(self.name, "rolled better than worst previous roll, stopping")
                Action.keep_all()
            if current_roll == worst_prev_result.roll and current_roll_num < worst_prev_result.num_rolls:
                if verbose:
                    print(self.name, "rolled same as worst previous roll but earlier, stopping")
                Action.keep_all()

        return Action.keep_none()

    def __str__(self):
        return self.name + " (SimpleAgent)"
