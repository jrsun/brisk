import features
from utils import get_territory_by_id
import copy, time

class Fortify_Evaluator():
    def __init__(self):
        pass

    # action = (source_territory, destination_territory, num_armies)
    def evaluate_action(self, action, map_layout, player_status, enemy_status):
        (sim_player_status, sim_enemy_status) = self._simulate(action, player_status, enemy_status)
        return features.evaluate(map_layout, sim_player_status, sim_enemy_status)

    def _simulate(self, action, player_status, enemy_status):
        ''' Takes away num_armies from source, and add num_armies to the destination '''
        source, destination, num_armies = action
        sim_player_status = copy.deepcopy(player_status)
        sim_source = get_territory_by_id(source['territory'], sim_player_status['territories'])
        sim_source['num_armies'] -= num_armies
        sim_dest = get_territory_by_id(dest['territory'], sim_player_status['territories'])
        sim_dest['num_armies'] += num_armies
        return (sim_player_status, enemy_status)

if __name__ == "__main__":
    import EvaluatorAI
    b = EvaluatorAI.EvaluatorAI()
    time.sleep(2)
    r = Fortify_Evaluator()
    b._refresh_state()
    source, dest = b._create_set_of_legal_fortifications()[0]
    possible_action = (source, dest, source['num_armies'] - 1)
    print features.evaluate(b.map_layout, b.player_status, b.get_enemy_status())
    print r.evaluate_action(possible_action, b.map_layout, b.player_status, b.get_enemy_status())