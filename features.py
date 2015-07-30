
# def evaluate(game_state, map_layout, player_status, players_status, enemy_status, phase=None):
    # 4.5.1
def armies_feature():
    return float(player_status['num_armies']) / sum([player['num_armies'] for player in players_status['players']])

# TODO: 4.5.2 - 4.5.5

# 4.5.6
def enemy_expected_reinforcements_feature():
    enemy_expected_reinforcements = max(enemy_status['num_territories'] / 3, 3)
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(enemy_territory_ids)):
            enemy_expected_reinforcements += c['continent_bonus']
    return enemy_expected_reinforcements

# 4.5.7
def enemy_occupied_continents_feature():
    enemy_occupied_continents = 0
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(enemy_territory_ids)):
            enemy_occupied_continents += 1
    return enemy_occupied_continents

# 4.5.8
def hinterland_feature():
    hinterlands = 0
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    player_territory_ids = [t['territory'] for t in player_status['territories']]
    for territory_id in player_territory_ids:
        #TODO no index
        for adjacent_id in map_layout['territories'][territory_id-1]['adjacent_territories']:
            if adjacent_id in enemy_territory_ids:
                break
        else:
            hinterlands += 1
    return hinterlands

# 4.5.10
def more_than_one_army_feature():
    fortified = 0
    total = 0
    for t in player_status['territories']:
        if t['num_armies'] > 1:
            fortified += 1
        total += 1
    return float(fortified) / total

# 4.5.11
def occupied_territories_feature():
    return float(player_status['num_territories']) / sum([player['num_territories'] for player in players_status['players']])

# 4.5.12
def our_expected_reinforcements_feature():
    our_expected_reinforcements = max(player_status['num_territories'] / 3, 3)
    player_territory_ids = set([t['territory'] for t in player_status['territories']])
    for c in map_layout['continents']:
        if set(c['territories']).issubset(player_territory_ids):
            our_expected_reinforcements += c['continent_bonus']
    return our_expected_reinforcements

# 4.5.13
def own_occupied_continents_feature():
    player_occupied_continents = 0
    player_territory_ids = [t['territory'] for t in player_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(player_territory_ids)):
            player_occupied_continents += 1
    return player_occupied_continents
