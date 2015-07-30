import Brisk
import time
import random
import itertools

POLL_TIME = 0.5 # seconds

class RandomAI(Brisk.Brisk):
    
    def __init__(self):
        super(RandomAI, self).__init__()
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
        reserves = self.player_status['num_reserves']
        # create set of legal territories to reinforce
        territories = [t['territory'] for t in self.player_status['territories']]
        for i in xrange(reserves):
            # choose best territory
            random_territory = random.choice(territories)
            self.place_armies(random_territory, 1)
        return False

    def do_attack(self):
        battles = self._create_set_of_legal_battles()
        best_battle = self._choose_best_battle(battles)
        
        # debug
        best_attack = (best_battle[0]['territory'],
            best_battle[1]['territory'],
            best_battle[0]['num_armies'])
        self.attack(*best_attack)

        return False

    def _create_set_of_legal_battles(self):
        territories = self.get_game_state()['territories']
        ours = []
        theirs = []
        for t in territories:
            if t['player'] is self.player_id:
                ours.append(t)
            else:
                theirs.append(t)
        return list(itertools.product(ours, theirs))

    def _choose_best_battle(self, battles):
        return random.choice(battles)

    def do_fortify(self):
        return False

if __name__ == "__main__":
    s = RandomAI()
    s.main()
