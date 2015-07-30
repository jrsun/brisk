import Brisk
import time
import random
import itertools

POLL_TIME = 0.5 # seconds

class RandomAI(Brisk.Brisk):
    
    def __init__(self):
        super(RandomAI, self).__init__()
        self.map_layout = self.get_map_layout()
        print self.game_id

    def main(self):
        while True:
            while self.get_player_status(True)['current_turn'] is False:
                time.sleep(POLL_TIME)
            self.player_status = self.get_player_status()

            self.do_reinforce()
            self.do_attack()
            self.do_fortify() or self.end_turn()

    def do_reinforce(self):
        print "REINFORCE"
        reserves = self.player_status['num_reserves']
        # create set of legal territories to reinforce
        territories = [t['territory'] for t in self.player_status['territories']]
        for i in xrange(reserves):
            # choose best territory
            random_territory = random.choice(territories)
            self.place_armies(random_territory, 1)
        return False

    def do_attack(self):
        print "ATTACK"
        battles = self._create_set_of_legal_battles()
        best_battle = self._choose_best_battle(battles)
        
        # debug
        best_attack = (best_battle[0]['territory'],
            best_battle[1]['territory'],
            min(3, best_battle[0]['num_armies'] - 1))
        self.attack(*best_attack)

        return False

    def _create_set_of_legal_battles(self):
        battles = []
        territories = self.get_game_state()['territories']
        ours = filter(lambda t: t['player'] is self.player_id and t['num_armies'] > 1, territories)
        for t in ours:
            adjacent_territories = self.map_layout['territories'][t['territory']-1]['adjacent_territories']
            for a in adjacent_territories:
                if territories[a-1]['player'] is not self.player_id:
                    battles.append((t, territories[a-1]))
        return battles

    def _choose_best_battle(self, battles):
        return random.choice(battles)

    def do_fortify(self):
        print "FORTIFY"
        return False

if __name__ == "__main__":
    s = RandomAI()
    s.main()
