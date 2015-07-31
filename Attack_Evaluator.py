import features
from utils import get_territory_by_id

class Attack_Evaluator():
	def __init__(self):
		pass

	# action = (attacking_territory, defending_territory, num_armies) triple
	def evaluate_action(self, action, map_layout, player_status, enemy_status):
		(sim_player_status, sim_enemy_status) = self._simulate(action, player_status, enemy_status)
		return features.evaluate(sim_map_layout, sim_player_status, sim_enemy_status)

	def _simulate(self, action, player_status, enemy_status):
		sim_player_status = player_status
		sim_player_status['territories'] = [t for t in player_status['territories'] if t['territory'] is not action['territory']]
		action['num_armies'] += 1
		sim_player_status['territories'].append(action)
		return (sim_player_status, enemy_status)