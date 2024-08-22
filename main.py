from result import Result
from roll import Roll, RollType
from agent import Agent, SimpleAgent
from typing import List, MutableMapping, Tuple, Mapping


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

    return Result(roll, num_rolls)


def play_single_round(players: List[Agent], verbose: bool = False) -> List[Tuple[Agent, Result]]:
    first, rest = players[0], players[1:]
    first_result = play_single_turn(first, verbose=verbose)
    max_rolls = first_result.num_rolls
    results = [(first, first_result)]
    if verbose:
        print()
        print(f"first player rolled {max_rolls} times, this is the max number of rolls for this round")
        print()

    for player in rest:
        results.append((player, play_single_turn(player, max_rolls=max_rolls,
                                                 worst_prev_result=min(map(lambda r: r[1], results)), verbose=verbose)))
        if verbose:
            print()

    if verbose:
        sorted_results = sorted(results, key=lambda r: r[1])
        print(
            f"round completed, winner: {sorted_results[0]}, loser: {sorted_results[-1]}, round value: {sorted_results[0][1].value()}")
    return results


def play_single_game(players: List[Agent], verbose: bool = False) -> Agent:
    players = players.copy()
    bank_tokens = 13
    tokens: MutableMapping[Agent, int] = {a: 0 for a in players}
    while bank_tokens > 0 or len(tokens.keys()) > 1:
        results = sorted(play_single_round(players, verbose=False), key=lambda r: r[1], reverse=True)
        winner, winner_result = results[0]
        loser, _ = results[-1]
        value = winner_result.value()
        if winner_result.roll.type() == RollType.SHOCK_OUT:
            bank_tokens = 0
            tokens = {loser: 13}
        elif bank_tokens > 0:
            actual_tokens = min(bank_tokens, value)
            bank_tokens -= actual_tokens
            tokens[loser] += actual_tokens
        else:
            actual_tokens = min(tokens[winner], value)
            tokens[winner] -= actual_tokens
            tokens[loser] += actual_tokens
        if verbose:
            print(f"single round completed, winner: {winner} ({winner_result}, value: {value}), loser: {loser}")
            print("new tokens: ", end="")
            if bank_tokens > 0:
                print(f"{bank_tokens} bank tokens, ", end="")
            print(", ".join(f"{a}: {t}" for a, t in tokens.items()))

        if bank_tokens == 0 and 0 in tokens.values():
            finished = [a for a, t in tokens.items() if t == 0]
            for a in finished:
                del tokens[a]
                players.remove(a)
            if verbose:
                print(f"{", ".join(str(a) for a in finished)} left the game, {len(players)} player(s) remaining")

        if len(players) > 1:
            index_loser = players.index(loser)
            players = players[index_loser:] + players[:index_loser]

    loser = tokens.popitem()[0]
    return loser


def main():
    players = [SimpleAgent("David"), SimpleAgent("Felix"), SimpleAgent("Julian")]
    stats: Mapping[Agent, int] = {p: 0 for p in players}
    games, num_games_as_txt = 100_000, "100k"
    print("simulation progress in 1k: ", end="", flush=True)
    for _ in range(1, games + 1):
        loser = play_single_game(players, verbose=False)
        stats[loser] += 1
        if _ % 1000 == 0:
            print(".", end="" if _ % 10_000 else " ", flush=True)
    print(f"({num_games_as_txt})\n\ngame statistics:", flush=True)
    for p, v in stats.items():
        print(f"{p}: {v} games lost ({v / games:.2%})", flush=True)


if __name__ == "__main__":
    main()
