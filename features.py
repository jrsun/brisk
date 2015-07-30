
def evaluate(game_state, map_layout, players_status, player_status, phase=None):
    # 4.5.1
    def armies_feature():
        return player_status['num_armies'] / sum([player['num_armies'] for player in players_status['players']])

    # 4.5.11
    def occupied_territories_feature():
        return player_status['num_territories'] / sum([player['num_territories'] for player in players_status['players']])

    # 4.5.12
    def our_expected_reinforcements_feature():
        pass

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

continent_rating = _generate_continent_rating(map_layout)