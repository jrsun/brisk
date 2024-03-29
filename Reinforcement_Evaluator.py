import features
import time
import copy
from utils import get_territory_by_id, wrapper

class Reinforcement_Evaluator():
    def __init__(self):
        pass

    # action = territory object
    def evaluate_action(self, action, map_layout, player_status, enemy_status): # 0.0005
        (sim_player_status, sim_enemy_status) = self._simulate(action, player_status, enemy_status)
        return features.evaluate_reinforce(map_layout, sim_player_status, sim_enemy_status)

    def _simulate(self, action, player_status, enemy_status): # 0.0004
        sim_player_status = copy.deepcopy(player_status) # 0.00035
        sim_player_status['num_armies'] += 1
        sim_player_status['num_reserves'] -= 1
        t = get_territory_by_id(action['territory'], sim_player_status['territories']) # 9e-6
        t['num_armies'] += 1
        return (sim_player_status, enemy_status)

if __name__ == "__main__":
    import EvaluatorAI
    b = EvaluatorAI.EvaluatorAI()
    time.sleep(5)
    r = Reinforcement_Evaluator()
    b._refresh_state()
    possible_action = b.player_status['territories'][0]
    import timeit
    from utils import wrapper
    wrapped = wrapper(r.evaluate_action, possible_action, b.map_layout, b.player_status, b.get_enemy_status())
    print "Waiting... "
    print "Evaluate (s): " + str(timeit.Timer(wrapped).timeit(number=1)/1)
