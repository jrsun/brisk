import AIBase
import time

class MovingTankAI(AIBase.AIBase):

    def __init__(self):
        super(MovingTankAI, self).__init__()
        self.tank_territory_id = None # Territory ID
        self.target_id = None # Territory ID



    def reinforce(self, num_reserves):
        ''' Returns {<territoryId>: <num troops deployed>} '''
        if self.tank_territory_id == None or utils.get_territory_by_id(self.tank_territory_id, self.player_status['territories']) == None:
            self.tank_territory_id = self.player_status['territories'][0]['territory']
        return { self.tank_territory_id: num_reserves }
        


    def battle(self, legal_territories_to_attack):
        ''' Returns (attack, defend, num_armies_to_attack), or a None value if not attacking '''

        targets = filter(lambda (attack,defend): attack['territory'] == self.tank_territory_id, legal_territories_to_attack)

        if targets:

            attack, defend = targets[0]
            self.target_id = defend['territory']
            army_count = attack['num_armies']

            if (army_count == 1):
                return None
            else:
                return (attack['territory'], defend['territory'], 3 if army_count > 3 else (2 if army_count == 3 else 1))

        else:
            return None



    def fortify(self, legal_territories_to_fortify):
        ''' Returns (from_territory, to_territory, num_armies_to_move), or a None value if ending turn '''

        if self.target_id:

            conqueredTerritory = utils.get_territory_by_id(self.target_id, self.player_status['territories'])

            if conqueredTerritory:

                tmp_id = self.tank_territory_id
                self.tank_territory_id = self.target_id
                source = utils.get_territory_by_id(tmp_id, self.player_status['territories'])

                num_armies = source['num_armies']
                if num_armies > 1:
                    return (tmp_id, self.target_id, num_armies - 1)

        return None

if __name__ == '__main__':
    bot = MovingTankAI()
    bot.run()