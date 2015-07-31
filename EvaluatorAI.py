import AIBase
import Reinforcement_Evaluator
import Battle_Evaluator
import Fortify_Evaluator
#debug
import features

class EvaluatorAI(AIBase.AIBase):

    def __init__(self):
        super(EvaluatorAI, self).__init__()
        self.re = Reinforcement_Evaluator.Reinforcement_Evaluator()
        self.be = Battle_Evaluator.Battle_Evaluator()
        self.fe = Fortify_Evaluator.Fortify_Evaluator()
        self.current_battle = None

    # what if there is no legal move?

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
        return score[max(score)]['territory'] if len(score) > 0 else None

    def battle(self, legal_territories_to_attack):
        ''' Returns (attack, defend, num_armies_to_attack), or a None value if not attacking '''
        best_battle = self._choose_best_battle(legal_territories_to_attack)
        if not best_battle:
            return None
        f, t = best_battle
        n = min(f['num_armies'] - 1, 3)
        return (f['territory'], t['territory'], n)

    def _choose_best_battle(self, legal_territories_to_attack):
        score = {}
        curr_score = features.evaluate(self.map_layout, self.player_status, self.enemy_status)
        for (src, dest) in legal_territories_to_attack:
            battle = (src, dest)
            # score[random.random()] = battle
            score[self.be.evaluate_action(battle, self.map_layout, self.player_status, self.enemy_status)] = battle
        if len(score) == 0 or max(score) - curr_score <= 0.5:
            return None
        print max(score) - curr_score
        return score[max(score)]

    def fortify(self, legal_territories_to_fortify):
        f, t, n = self._choose_best_fortify(legal_territories_to_fortify)
        return (f['territory'], t['territory'], n)
        ''' Returns (from_territory, to_territory, num_armies_to_move), or a None value if ending turn '''

    def _choose_best_fortify(self, legal_territories_to_fortify):
        score = {}
        for (src, dest) in legal_territories_to_fortify:
            fortification = (src, dest, src['num_armies'] - 1)
            score[self.fe.evaluate_action(fortification, self.map_layout, self.player_status, self.enemy_status)] = fortification
        return score[max(score)] if len(score) > 0 else None

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
