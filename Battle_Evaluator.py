import features
import time
import copy
import Battle_Computer
from utils import get_territory_by_id, wrapper

class Battle_Evaluator():
    def __init__(self):
        pass

    # action = (src, dest)
    # Unlike reinforcement and fortify, a simulation returns a list of possible outcomes w/ probabilities
    # evaluate_action takes expected value
    def evaluate_action(self, action, map_layout, player_status, enemy_status): # 0.0005
        simulated_outcomes = self._simulate(action, player_status, enemy_status)
        return sum([prob*features.evaluate_battle(map_layout, sim['player_status'], sim['enemy_status']) for (prob, sim) in simulated_outcomes.iteritems()])
        
    def _simulate(self, action, player_status, enemy_status): # 0.0004
        # outcomes = {prob: game_state}
        outcomes = {}

        # if win
        src, dest = action

        win_prob = Battle_Computer.compute(src['num_armies'], dest['num_armies'])
        win_player_status = copy.deepcopy(player_status)
        win_enemy_status = copy.deepcopy(enemy_status)
        win_src = get_territory_by_id(action[0]['territory'], win_player_status['territories'])
        win_src['num_armies'] = (win_src['num_armies'] / 2) + 1
        win_dest = get_territory_by_id(action[1]['territory'], win_enemy_status['territories'])
        win_player_status['territories'].append(win_dest)
        win_enemy_status['territories'].remove(win_dest)
        win_state = {
            'player_status': win_player_status,
            'enemy_status': win_enemy_status
        }

        lose_prob = 1 - win_prob
        lose_player_status = copy.deepcopy(player_status)
        lose_player_status['num_armies'] -= (src['num_armies'] - 1)
        lose_enemy_status = copy.deepcopy(enemy_status)
        lose_src = get_territory_by_id(action[0]['territory'], lose_player_status['territories'])
        lose_src['num_armies'] = 1
        lose_dest = get_territory_by_id(action[1]['territory'], lose_enemy_status['territories'])
        lose_state = {
            'player_status': lose_player_status,
            'enemy_status': lose_enemy_status
        }

        outcomes[win_prob] = win_state
        outcomes[lose_prob] = lose_state

        return outcomes

if __name__ == "__main__":
    import EvaluatorAI
    b = EvaluatorAI.EvaluatorAI()
    time.sleep(5)
    r = Battle_Evaluator()
    b._refresh_state()
    possible_action = (b.player_status['territories'][0], b.enemy_status['territories'][0])
    import timeit
    from utils import wrapper
    wrapped = wrapper(r.evaluate_action, possible_action, b.map_layout, b.player_status, b.get_enemy_status())
    print "Waiting... "
    print "Evaluate (s): " + str(timeit.Timer(wrapped).timeit(number=1)/1)
