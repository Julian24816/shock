import random



class MoveChoice:
    def __init__(self, keep_first, keep_second, keep_third, flip_a_one = False):
        self.keep_first = keep_first
        self.keep_second = keep_second
        self.keep_third = keep_third
        self.flip_a_one = flip_a_one
   
   

class GameState:
    def __init__(self, *actors):
        self.actors = actors
        self.current_player_index = 0
        
    def get_current_player(self):
        return self.actors[self.current_player_index]
    
    def apply_move(self, actor, move):
        pass
    
    def is_valid_move(self, move):
        return True
    

class Actor:
    def __init__(self, name):
        self.name = name

class Game:
    def __init__(self, *actors):
        self.game_state = GameState(actors)
    
    def step(self, verbose=False):
        actor = self.game_state.get_current_player()
        if verbose: print(f"its {actor}'s turn")
        choice = actor.choose_move(self.game_state)
        if verbose: print(f"{actor} chose {choice}")
        if not self.game_state.is_valid_move(choice):
            raise Exception("Invalid move")
        self.apply_move(actor, choice)
        if verbose: print("the game state is now:", self.game_state)

def main():
    game = Game(Actor("David"), Actor("Felix"), Actor("Julian"), Actor("Zorro"))
    while True:
        game.step()
        input()

if __name__ == "__main__":
    main()