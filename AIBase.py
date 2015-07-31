import Brisk, config, utils
import sys, time, json

# Error codes

class ReinforceError(object):
    _prefix = "ReinforceError: "
    LEFTOVER_ARMY = _prefix + "You did not deploy all of your troops."
    TOO_MUCH_ARMY = _prefix + "You deployed more troops than you have."
    @staticmethod
    def TERRITORY_NOT_OWNED(territoryIds):
        return "ReinforceError: You don't own the following territories: %s" % str(territoryIds)

class AttackError(object):
    @staticmethod
    def ILLEGAL_ATTACK(tattack, tdefend):
        return "AttackError: Cannot attack %d from %d: they are not adjacent, or you do not own the attacking territory." % ( tdefend, tattack)
    @staticmethod
    def NOT_ENOUGH_ARMY(tattack, tdefend, num_armies):
        return "AttackError: Cannot attack %d from %d: less than %d armies to move." % (tdefend, tattack, num_armies)
    @staticmethod
    def TOO_MUCH_ARMY(tattack, tdefend, num_armies):
        return "AttackError: Cannot attack %d from %d with %d armies: cannot attack with more than 3 armies" % (tdefend, tattack, num_armies)

class FortifyError(object):
    @staticmethod
    def ILLEGAL_FORTIFY(tfrom, tto):
        return "FortifyError: Cannot fortify from %d to %d: they are not adjacent, you do not own at least one of the territories, or you have only 1 troop in the source territory." % (tfrom, tto)
    @staticmethod
    def NOT_ENOUGH_ARMY(tfrom, tto, num_armies):
        return "FortifyError: Cannot fortify from %d to %d: less than %d armies to move." % (tfrom, tto, num_armies)



class AIBase(Brisk.Brisk):

    # Methods to be implemented by subclasses

    def reinforce(self, num_reserves):
        ''' Returns {<territoryId>: <num troops deployed>} '''
        pass

    def battle(self, legal_territories_to_attack):
        ''' Returns (attack, defend, num_armies_to_attack), or a None value if not attacking '''
        pass

    def fortify(self, legal_territories_to_fortify):
        ''' Returns (from_territory, to_territory, num_armies_to_move), or a None value if ending turn '''
        pass



    # Private utilities

    def _create_set_of_legal_battles(self):
        battles = []
        territories = self.get_game_state()['territories']
        ours = filter(lambda t: t['player'] is self.player_id and t['num_armies'] > 1, territories)
        for t in ours:
            adjacent_territories = self.map_layout['territories'][t['territory']-1]['adjacent_territories']
            for a in adjacent_territories:
                if territories[a-1]['player'] is not self.player_id:
                    battles.append((t, territories[a-1]))
        # battles = [battle]
        # battle = (territory, territory)
        # territory = {'territory': 2, 'num_armies': 3, 'player': 1}
        return battles

    def _create_set_of_legal_fortifications(self):
        fortifications = []
        territories = self.get_game_state()['territories']
        ours = filter(lambda t: t['player'] is self.player_id and t['num_armies'] > 1, territories)
        for t in ours:
            adjacent_territories = self.map_layout['territories'][t['territory']-1]['adjacent_territories']
            for a in adjacent_territories:
                if territories[a-1]['player'] is self.player_id:
                    fortifications.append((t, territories[a-1]))

        return fortifications

    def _generate_continent_ratings(self):
        self.continent_rating = {}
        for continent in self.map_layout['continents']:
            border_territories = []
            for territory_id in continent['territories']:
                #TODO no index-1
                for adjacent_id in self.map_layout['territories'][territory_id-1]['adjacent_territories']:
                    if adjacent_id not in continent['territories']:
                        border_territories.append(territory_id)
                        break
            self.continent_rating[continent['continent']] = float(15 + continent['continent_bonus'] - 4 * len(border_territories)) / len(continent['territories'])

    def _refresh_state(self):
        self.game_state = self.get_game_state()
        self.player_status = self.get_player_status()
        self.player_status_lite = self.get_player_status(True)
        self.enemy_status = self.get_enemy_status()

    def _err(self, msg):
        print "Current game state:"
        utils.pp(self.game_state)
        print "\nCurrent player status:"
        utils.pp(self.player_status)
        print msg
        sys.exit(1)



    # Core AI execution methods

    def __init__(self):
        super(AIBase, self).__init__()
        self.map_layout = self.get_map_layout()
        self._refresh_state()
        self._generate_continent_ratings()

    def do_reinforce(self):
        num_reserves = self.player_status['num_reserves']
        reinforcements = self.reinforce(num_reserves)

        # TODO handle error when placing in enemy territory
        invalid_ids = filter(lambda t_id: utils.get_territory_by_id(t_id,self.player_status['territories']) == None, reinforcements.keys())
        if invalid_ids:
            self._err(ReinforceError.TERRITORY_NOT_OWNED(invalid_ids))

        num_deployed = sum(reinforcements.values())
        # All troops must be deployed
        if (num_deployed < num_reserves):
            self._err(ReinforceError.LEFTOVER_ARMY)
        # Cannot deploy too many troops
        elif (num_deployed > num_reserves):
            self._err(ReinforceError.TOO_MUCH_ARMY)

        # Execute reinforcement
        for t_id, num_troops in reinforcements.iteritems():
            self.place_armies(t_id, num_troops)


    def do_battle(self):
        ''' Returns True when done, false otherwise '''
        legal_battles = self._create_set_of_legal_battles()
        attacks = self.battle(legal_battles)

        if attacks:
            tattack, tdefend, num_armies = attacks
            legal_battles_to_ids = map(lambda (a,d): (a['territory'], d['territory']), legal_battles)
            if ((tattack, tdefend) not in legal_battles_to_ids):
                self._err(AttackError.ILLEGAL_ATTACK(tattack, tdefend))
            else:
                t = utils.get_territory_by_id(tattack, self.player_status['territories'])
                # There must be enough troops to attack
                if num_armies > t['num_armies'] - 1:
                    self._err(AttackError.NOT_ENOUGH_ARMY(tattack, tdefend, num_armies))
                # There can't be more than 3 troops attacking
                elif num_armies > 3:
                    self._err(AttackError.TOO_MUCH_ARMY(tattack, tdefend, num_armies))
                else:
                    # Everything is valid
                    self.attack(tattack, tdefend, num_armies)
            return False
        else:
            return True
        

    def do_fortify(self):
        legal_forts = self._create_set_of_legal_fortifications()
        fortification = self.fortify(legal_forts)

        if fortification:
            tfrom, tto, num_armies = fortification
            legal_forts_to_ids = map(lambda (f,t): (f['territory'], t['territory']), legal_forts)
            print legal_forts_to_ids
            # Fortification must occur between adjacent territories
            if (tfrom, tto) not in legal_forts_to_ids:
                self._err(FortifyError.ILLEGAL_FORTIFY(tfrom, tto))
            else:
                t = utils.get_territory_by_id(tfrom, self.player_status['territories'])
                # There must be enough troops to move
                if num_armies > t['num_armies'] - 1:
                    self._err(FortifyError.NOT_ENOUGH_ARMY(tfrom, tto, num_armies))
                else:
                    # Everything is valid
                    self.transfer_armies(tfrom, tto, num_armies)
        else:
            self.end_turn()

    def run(self):
        print "Game ID: %d" % self.game_id

        while not self.game_state['winner']:

            if self.player_status['current_turn']:
                print "New turn"

                print "Reinforcing..."
                self._refresh_state()
                # Handles the possibility that previous fortify has not ended the turn right away.
                if self.player_status['num_reserves'] == 0:
                    print "num_reserves is 0, retrying...\n"
                    time.sleep(config.POLL_TIME)
                    self._refresh_state()
                    continue # Redo all the initial checks of the loop
                self.do_reinforce()

                print "Attacking..."
                done = False
                while not done:
                    self._refresh_state()
                    done = self.do_battle()

                print "Fortifying..."
                # refresh state
                self._refresh_state()
                self.do_fortify()

                print "End turn!\n"

            time.sleep(config.POLL_TIME)
            self._refresh_state()

