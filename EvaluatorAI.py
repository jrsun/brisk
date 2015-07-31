import AIBase
import Reinforcement_Evaluator

class EvaluatorAI(AIBase.AIBase):

    def __init__(self):
        super(EvaluatorAI, self).__init__()
        self.re = Reinforcement_Evaluator.Reinforcement_Evaluator()

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

    def _choose_best_reinforce(self, legal_territories_to_reinforce): # < 0.008
        ''' Returns best territory_id to place an army '''
        score = {}
        for territory in legal_territories_to_reinforce:
            score[self.re.evaluate_action(territory, self.map_layout, self.player_status, self.enemy_status)] = territory
        return score[max(score)]['territory']

    def battle(self, legal_territories_to_attack):
        ''' Returns (attack, defend, num_armies_to_attack), or a None value if not attacking '''


    def fortify(self, legal_territories_to_fortify):
        ''' Returns (from_territory, to_territory, num_armies_to_move), or a None value if ending turn '''

if __name__ == '__main__':
    bot = EvaluatorAI()
    bot.run()
    # import time
    # time.sleep(5)
    # bot._refresh_state()
    # import timeit
    # from utils import wrapper
    # wrapped = wrapper(bot._choose_best_reinforce, bot.player_status['territories'])
    # print "Waiting... "
    # print "Evaluate (s): " + str(timeit.Timer(wrapped).timeit(number=1)/1)
