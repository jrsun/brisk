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

            self.reinforce()
            self.attack()
            self.fortify() or self.end_turn()

    def reinforce(self):
        reserves = self.player_status['num_reserves']
        # create set of legal territories to reinforce
        territories = [t['territory'] for t in self.player_status['territories']]
        for i in xrange(reserves):
            # choose best territory
            random_territory = random.choice(territories)
            self.place_armies(random_territory, 1)
        return False

    def attack(self):
        battles = self._create_set_of_legal_battles()
        best_battle = self._choose_best_battle(battles)
        
        armies = self.
        return False

    def _create_set_of_legal_battles(self):
        territories = self.get_game_state()['territories']
        ours = []
        theirs = []
        for t in territories:
            if t['player'] is self.player_id:
                ours.append(t['territory'])
            else:
                theirs.append(t['territory'])
        return list(itertools.product(ours, theirs))

    def _choose_best_battle(self, battles):
        return random.choice(battles)

    def fortify(self):
        return False

if __name__ == "__main__":
    s = RandomAI()
    s.main()
