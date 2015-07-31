import features
import time
import copy
from utils import get_territory_by_id

class Reinforcement_Evaluator():
	def __init__(self):
		pass

	# action = territory object
	def evaluate_action(self, action, map_layout, player_status, enemy_status):
		(sim_player_status, sim_enemy_status) = self._simulate(action, player_status, enemy_status)
		print sim_player_status['territories'][0]
		return features.evaluate(map_layout, sim_player_status, sim_enemy_status)

	def _simulate(self, action, player_status, enemy_status):
		sim_player_status = copy.deepcopy(player_status)
		t = get_territory_by_id(action['territory'], sim_player_status['territories'])
		t['num_armies'] += 1
		return (sim_player_status, enemy_status)

if __name__ == "__main__":
	import EvaluatorAI
	b = EvaluatorAI.EvaluatorAI()
	time.sleep(2)
	r = Reinforcement_Evaluator()
	b._refresh_state()
	possible_action = b.player_status['territories'][0]
	print r.evaluate_action(possible_action, b.map_layout, b.player_status, b.get_enemy_status())