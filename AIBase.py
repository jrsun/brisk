import Brisk, config
import sys, time

class AIBase(Brisk.Brisk):

    # Methods to be implemented by subclasses

    def reinforce(num_reserves):
        ''' Returns {<territoryId>: <num troops deployed>} '''
        pass

    def battle(legal_territories_to_attack):
        ''' Returns (attack, defend), or a None value if not attacking '''
        pass

    def fortify(legal_territories_to_fortify):
        ''' Returns (from_territory, to_territory), or a None value if ending turn '''
        pass



    # Error codes

    class ReinforceError(object):
        _prefix = "ReinforceError: "
        LEFTOVER_ARMY = _prefix + "You did not deploy all of your troops."
        TOO_MUCH_ARMY = _prefix + "You deployed more troops than you have."
        def TERRITORY_NOT_OWNED(territoryIds):
            return "%sYou don't own the following territories: %s" % (_prefix, str(territoryIds))

    class AttackError(object):
        _prefix = "AttackError: "
        def ILLEGAL_ATTACK(tattack, tdefend):
            return "%sCannot attack %d from %d: they are not adjacent, or you do not own the attacking territory." % (_prefix, tdefend, tattack)
        def NOT_ENOUGH_ARMY(tattack, tdefend, num_armies):
            return "%sCannot attack %d from %d: less than %d armies to move." % (_prefix, tdefend, tattack, num_armies)
        def TOO_MUCH_ARMY(tattack, tdefend, num_armies):
            return "%sCannot attack %d from %d with %d armies: cannot attack with more than 3 armies" % (_prefix, tdefend, tattack, num_armies)

    class FortifyError(object):
        _prefix = "FortifyError: "
        def ILLEGAL_FORTIFY(tfrom, tto):
            return "%sCannot fortify from %d to %d: they are not adjacent, or you do not own at least one of the territories." % (_prefix, tfrom, tto)
        def NOT_ENOUGH_ARMY(tfrom, tto, num_armies):
            return "%sCannot fortify from %d to %d: less than %d armies to move." % (_prefix, tfrom, tto, num_armies)



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
                for adjacent_id in self.map_layout['territories'][territory_id-1]['adjacent_territories']:
                    if adjacent_id not in continent['territories']:
                        border_territories.append(territory_id)
                        break
            self.continent_rating[continent['continent']] = float(15 + continent['continent_bonus'] - 4 * len(border_territories)) / len(continent['territories'])

    def _refresh_state(self):
        self.game_state = self.get_game_state()
        self.player_status = self.get_player_status()
        self.player_status_lite = self.get_player_status(True)



    # Public utilities

    def pp(jsonObject):
        ''' Pretty prints json '''
        json.dumps(jsonObject, indents=4)

    # Could optimize this
    def get_territory_by_id(tid, territories):
        for t in territories:
            if t['territory'] == tid:
                return t
        return None



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
        invalid_ids = filter(lambda tid: get_territory_by_id(tid,self.player_status['territories']) == None, reinforcements.keys())
        if invalid_ids:
            err(ReinforceError.TERRITORY_NOT_OWNED(invalid_ids))

        num_deployed = sum(reinforcements.values())
        # All troops must be deployed
        if (num_deployed < num_reserves):
            err(ReinforceError.LEFTOVER_ARMY)
        # Cannot deploy too many troops
        elif (num_deployed > num_reserves):
            err(ReinforceError.TOO_MUCH_ARMY)

        # Execute reinforcement
        for territoryId, num_troops in reinforcements:
            self.place_armies(territoryId, num_troops)


    def do_battle(self):
        ''' Returns True when done, false otherwise '''
        legal_attacks = self._create_set_of_legal_battles()
        attacks = self.battle(legal_attacks)

        if attacks:
            tattack, tdefend, num_armies = attacks
            if ((tattack, tdefend) not in legal_attacks):
                err(AttackError.ILLEGAL_ATTACK(tattack, tdefend))
            else:
                t = get_territory_by_id(tattack, self.player_status['territories'])
                # There must be enough troops to attack
                if num_armies > t.num_armies - 1:
                    err(AttackError.NOT_ENOUGH_ARMY(tattack, tdefend, num_armies))
                # There can't be more than 3 troops attacking
                elif num_armies > 3:
                    err(AttackError.TOO_MUCH_ARMY(tattack, tdefend, num_armies))
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
            # Fortification must occur between adjacent territories
            if (tfrom, tto) not in legal_forts:
                err(FortifyError.ILLEGAL_FORTIFY(tfrom, tto))
            else:
                t = get_territory_by_id(tfrom, self.player_status['territories'])
                # There must be enough troops to move
                if num_armies > t.num_armies - 1:
                    err(FortifyError.NOT_ENOUGH_ARMY(tfrom, tto, num_armies))
                else:
                    # Everything is valid
                    self.transfer_armies(tfrom, tto, num_armies)
        else:
            self.end_turn()

    def err(msg):
        print msg
        print "Current game state:"
        pp(self.game_state)
        print "\nCurrent player status:"
        pp(self.player_status)
        sys.exit(1)

    def run(self):
        print "Game ID: %d" % self.game_id

        while not self.game_state['winner']:

            if self.player_status['current_turn']:

                self._refresh_state()
                self.do_reinforce()

                done = False
                while not done:
                    self._refresh_state()
                    done = self.do_battle()

                # refresh state
                self._refresh_state()
                self.do_fortify()

            self._refresh_state()
            time.sleep(config.POLL_TIME)

