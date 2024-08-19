from typing import List, Tuple, Mapping
from agent import Agent
from roll import Roll, Result


class GameState:
    def __init__(self, players: Tuple[Agent, ...]):
       self.players = players
       self.active_players: Tuple[Agent, ...] = self.players
       self.token_map: Mapping[Agent, int] = { p:0 for p in self.players }
       self.current_player = 0
       self.max_rolls = 3
       self.current_player_roll = 0
       self.current_roll: Roll = Roll((0, 0, 0))
       self.roll_results: List[Result] = []