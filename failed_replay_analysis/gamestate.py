

class Player:
    def __init__(self, race, opp_race):
        self.race = race
        self.opp_race = opp_race

class GameState:
    def __init__(self, replay_path, player):
        self.replay_path = replay_path
        self.player = player
        self.vespene = 0
        self.minerals = 0
        self.food_cap = 0
        self.food_used = 0
        self.food_army = 0
        self.food_workers = 0
        self.idle_worker_count = 0
        self.army_count = 0
        self.warp_gate_count = 0
        self.larva_count = 0
        self.timestamp = 0

        