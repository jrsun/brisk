import AIBase

class TestSubmissiveAI(AIBase.AIBase):

    def reinforce(self, num_reserves):
        ''' Returns {<territoryId>: <num troops deployed>} '''
        # Always puts all troops in the first territory on the list
        return { self.player_status['territories'][0]['territory']: num_reserves }

    def battle(self, legal_territories_to_attack):
        ''' Returns (attack, defend), or a None value if not attacking '''
        return None

    def fortify(self, legal_territories_to_fortify):
        ''' Returns (from_territory, to_territory, num_armies_to_move), or a None value if ending turn '''
        return None

if __name__ == '__main__':
    bot = TestSubmissiveAI()
    bot.run()