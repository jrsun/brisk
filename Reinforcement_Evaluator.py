import features
from utils import get_territory_by_id

class Reinforcement_Evaluator():
	def __init__(self):
		pass

	# action = territory object
	def evaluate(self, action, map_layout, player_status, enemy_status):
		(sim_map_layout, sim_player_status, sim_enemy_status) = self._simulate(action, map_layout, player_status, enemy_status)
		return features.evaluate(sim_map_layout, sim_player_status, sim_enemy_status)

	def _simulate(self, action, map_layout, player_status, enemy_status):
		sim_player_status = player_status
		sim_player_status['territories'] = [t for t in player_status['territories'] if t['territory'] is not action['territory']]
		action['num_armies'] += 1
		sim_player_status['territories'].append(action)
		return (map_layout, sim_player_status, enemy_status)