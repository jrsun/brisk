
def evaluate(game_state, map_layout, players_status, player_status, phase=None):
    # 4.5.1
    def armies_feature():
        return player_status['num_armies'] / sum([player['num_armies'] for player in players_status['players']])

    # 4.5.11
    def occupied_territories_feature():
        return player_status['num_territories'] / sum([player['num_territories'] for player in players_status['players']])

    # 4.5.12
    def our_expected_reinforcements_feature():
        our_expected_reinforcements = max(player_status['num_territories'] / 3, 3)
        player_territory_ids = [t['territory'] for t in player_status['territories']]
        for c in map_layout['continents']:
            if set(c['territories']).issubset(set(player_territory_ids)):
                our_expected_reinforcements += c['continent_bonus']
        return our_expected_reinforcements

    def enemy_expected_reinforcements_feature():
        players = players_status['players']
        enemy_status = players_status['players'][0] if players_status['players'][0]

