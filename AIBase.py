import Brisk
import sys

class AIBase(Brisk.Brisk):

    # Methods to be implemented by subclasses

    def reinforce(num_reserves):
        ''' Returns {<territoryId>: <num troops deployed>} '''
        pass

    def attack(legal_territories_to_attack):
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

    class FortifyError(object):
        _prefix = "FortifyError: "

        def NOT_ADJACENT(tFrom, tTo):
            return "%sCannot fortify from %d to %d: they are not adjacent." % (_prefix, tFrom, tTo))
        def NOT_ENOUGH_ARMIES(tFrom, tTo, num_armies):
            return "%sCannot fortify from %d to %d: less than %d armies to move." % (_prefix, tFrom, tTo, num_armies)


    # Private utilities

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

    def _generate_continent_ratings(map_layout):
        continent_rating = {}
        for continent in map_layout['continents']:
            border_territories = []
            for territory_id in continent['territories']:
                for adjacent_id in map_layout['territories'][territory_id-1]['adjacent_territories']:
                    if adjacent_id not in continent['territories']:
                        border_territories.append(territory_id)
                        break
            continent_rating[continent['continent']] = float(15 + continent['continent_bonus'] - 4 * len(border_territories)) / len(continent['territories'])
        def f(continent_id):
            return continent_rating[continent_id]
        return f

    # Public utilities

    def pp(jsonObject):
        ''' Pretty prints json '''
        json.dumps(jsonObject, indents=4)

    def getTerritoryById(tid, territories):
        for t in territories:
            if t['territory'] == tid:
                return t

    continent_rating = _generate_continent_rating(map_layout)


    # Core AI execution methods

    def __init__(self):
        super(AIBase, self).__init__()
        self.map_layout = self.get_map_layout()
        self.refresh_state()

    def do_reinforce(self):
        num_reserves = self.player_status['num_reserves']
        reinforcements = self.reinforce(num_reserves)

        num_deployed = sum(reinforcements.values))
        # All troops must be deployed
        if (num_deployed < num_reserves)
            err(ReinforceError.LEFTOVER_ARMY)
        # Cannot deploy too many troops
        elif (num_deployed > num_reserves):
            err(ReinforceError.TOO_MUCH_ARMY)

        # Execute reinforcement
        for territoryId, num_troops in reinforcements:
            self.place_armies(territoryId, num_troops)


    def do_attack(self):
        

    def do_fortify(self):
        legal_forts = self._create_set_of_legal_fortifications()
        fortification = self.fortify(legal_forts)

        if fortification:
            tFrom, tTo, num_armies = fortification
            # Fortification must occur between adjacent territories
            if fortification not in legal_forts:
                err(FortifyError.NOT_ADJACENT(tFrom, tTo))
            else:
                t = getTerritoryById(tFrom, self.player_status['territories'])
                # There must be enough troops to move
                if num_armies > t.num_armies - 1:
                    err(FortifyError.NOT_ENOUGH_ARMIES(tFrom, tTo, num_armies))
                else:
                    # Everything is valid
                    self.transfer_armies(tFrom, tTo, num_armies)
        else:
            self.end_turn()




    def refresh_state(self):
        self.game_state = self.get_game_state()
        self.player_status = self.get_player_status()
        self.player_status_lite = self.get_player_status(True)

    def err(msg):
        print msg
        print "Current game state:"
        pp(self.game_state)
        print "\nCurrent player status:"
        pp(self.player_status)
        sys.exit(1)

    def run(self):
        print self.game.game_id
        # refresh state
        # do reinforce
        # refresh state
        # do attack
        # refresh state
        # do fortify