import AIBase
import Reinforcement_Evaluator

class EvaluatorAI(AIBase.AIBase):

    def __init__(self):
        super(EvaluatorAI, self).__init__()

    def reinforce(self, num_reserves):
        ''' Returns {<territoryId>: <num troops deployed>} '''
        legal_territories_to_reinforce = self.player_status['territories']
        reinforcements = {}
        for i in xrange(num_reserves):
            territory_id = self._choose_best_reinforce(legal_territories_to_reinforce)
            if reinforcements.has_key(territory_id):
                reinforcements[territory_id] += 1
            else:
                reinforcements[territory_id] = 1
        return reinforcements

    def _choose_best_reinforce(self, legal_territories_to_reinforce):
        ''' Returns best territory_id to place an army '''
        return legal_territories_to_reinforce[0]['territory']

    def battle(self, legal_territories_to_attack):
        ''' Returns (attack, defend, num_armies_to_attack), or a None value if not attacking '''


    def fortify(self, legal_territories_to_fortify):
        ''' Returns (from_territory, to_territory, num_armies_to_move), or a None value if ending turn '''

if __name__ == '__main__':
    bot = EvaluatorAI()
    bot.run()