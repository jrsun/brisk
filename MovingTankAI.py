import AIBase
import time

class MovingTankAI(AIBase.AIBase):

    def __init__(self):
        super(MovingTankAI, self).__init__()
        self.tank_territory = None # Territory object
        self.target = None # Territory object



    def reinforce(self, num_reserves):
        ''' Returns {<territoryId>: <num troops deployed>} '''
        if self.tank_territory == None or get_territory_by_id(tank_territory['territory'], self.player_status['territories']) == None:
            self.tank_territory = self.player_status['territories'][0]
        return { self.tank_territory['territory']: num_reserves }
        


    def battle(self, legal_territories_to_attack):
        ''' Returns (attack, defend, num_armies_to_attack), or a None value if not attacking '''

        targets = filter(lambda (attack,defend): attack['territory'] == self.tank_territory['territory'], legal_territories_to_attack)

        if targets:

            attack, defend = targets[0]
            self.target = defend
            army_count = attack['num_armies']

            if (army_count == 1):
                return None
            else:
                return (attack['territory'], defend['territory'], 3 if army_count > 3 else (2 if army_count == 3 else 1))

        else:
            return None



    def fortify(self, legal_territories_to_fortify):
        ''' Returns (from_territory, to_territory, num_armies_to_move), or a None value if ending turn '''

        start = time.time()

        if self.target:

            conqueredTerritory = AIBase.get_territory_by_id(self.target['territory'], self.player_status['territories'])

            if conqueredTerritory:

                tmp = self.tank_territory
                self.tank_territory = self.target

                num_armies = tmp['num_armies']
                if num_armies > 1:

                    print time.time() - start

                    return (tmp['territory'], self.target['territory'], num_armies - 1)

        print "Failed; %d" % (time.time() - start)
        return None

if __name__ == '__main__':
    bot = MovingTankAI()
    bot.run()