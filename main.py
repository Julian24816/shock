from roll import Roll, Result
from agent import Agent, SimpleAgent
from typing import List


def play_single_turn(agent: Agent, max_rolls: int = 3, worst_prev_result: Result = None, verbose: bool = False):
    assert 1 <= max_rolls <= 3, "max rolls needs to be between 1 and 3"
    assert worst_prev_result is not None or max_rolls == 3, "max rolls needs to be 3 if first player"

    if verbose:
        print(f"playing with a maximum of {max_rolls} rolls, trying to beat {worst_prev_result}")

    roll = Roll.new_roll()
    num_rolls = 1
    if verbose:
        print("1. roll:", roll)

    while num_rolls < max_rolls:

        action = agent.play(roll, num_rolls, max_rolls - num_rolls, worst_prev_result, verbose=verbose)

        if all(action.keep_dice):
            if verbose:
                print("stopping")
            break
        if action.flip_third:
            roll = roll.reroll_flipping_third()
            if verbose:
                print("rerolling flipping third")
        else:
            roll = roll.reroll_keeping(*action.keep_dice)
            if verbose:
                print(f"rerolling keeping {action.keep_dice} dice")
        num_rolls += 1
        if verbose:
            print(f"{num_rolls}. roll:", roll)
            if num_rolls == max_rolls:
                print(f"reached maximum of {max_rolls} rolls")

    return Result(agent.name, roll, num_rolls)

def play_single_round(players: List[Agent], verbose: bool = False) -> List[Result]:
    first, rest = players[0], players[1:]
    first_result = play_single_turn(first, verbose=verbose)
    max_rolls = first_result.num_rolls
    results = [first_result]
    if verbose:
        print()
        print(f"first player rolled {max_rolls} times, this is the max number of rolls for this round")
        print()

    for player in rest:
        results.append(play_single_turn(player, max_rolls=max_rolls, worst_prev_result=min(results), verbose=verbose))
        if verbose:
            print()

    if verbose:
        print(f"round completed, winner: {max(results)}, loser: {min(results)}, round value: {max(results).value()}")
    return results


def main():
    players = [SimpleAgent("David"), SimpleAgent("Felix"), SimpleAgent("Julian")]
    for _ in range(1000):
        results = play_single_round(players, verbose=False)
        print("winner:", max(results))


if __name__ == "__main__":
    main()
