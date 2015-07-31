import time
from utils import get_territory_by_id
    
# 4.5.1
def armies_feature(map_layout, player_status, enemy_status):
    return float(player_status['num_armies']) / (player_status['num_armies'] + enemy_status['num_armies'])

# 4.5.2 - not useful

# 4.5.3ish
def continent_safety_feature(map_layout, player_status, enemy_status):
    player_occupied_continents = []
    player_territory_ids = [t['territory'] for t in player_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(player_territory_ids)):
            player_occupied_continents.append(c)

    continent_safety_feature = 0
    for c in player_occupied_continents:
        total_border_threat = 0
        for border_territory_id in c['border_territories']:
            total_border_threat += _enemy_threat(border_territory_id, map_layout, player_status, enemy_status)
        total_border_threat *= c['rating']
        continent_safety_feature += total_border_threat
    return continent_safety_feature

# 4.5.4ish
def continent_threat_feature(map_layout, player_status, enemy_status):
    enemy_occupied_continents = []
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(enemy_territory_ids)):
            enemy_occupied_continents.append(c)

    continent_threat_feature = 0
    for c in enemy_occupied_continents:
        total_border_threat = 0
        for border_territory_id in c['border_territories']:
            total_border_threat += _our_threat(border_territory_id, map_layout, player_status, enemy_status)
        total_border_threat *= c['rating']
        continent_threat_feature += total_border_threat
    return continent_threat_feature

# assumes t_id in player territories
def _enemy_threat(t_id, map_layout, player_status, enemy_status):
    bst = 0
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    player_territory_ids = [t['territory'] for t in player_status['territories']]
    for adjacent_id in get_territory_by_id(t_id, map_layout['territories'])['adjacent_territories']:
        if adjacent_id in enemy_territory_ids:
            bst += get_territory_by_id(adjacent_id, enemy_status['territories'])['num_armies']
    bsr = float(bst) / get_territory_by_id(t_id, player_status['territories'])['num_armies']
    return bsr

# assumes t_id in enemy territories
def _our_threat(t_id, map_layout, player_status, enemy_status):
    bst = 0
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    player_territory_ids = [t['territory'] for t in player_status['territories']]
    for adjacent_id in get_territory_by_id(t_id, map_layout['territories'])['adjacent_territories']:
        if adjacent_id in player_territory_ids:
            bst += get_territory_by_id(adjacent_id, player_status['territories'])['num_armies']
    bsr = float(bst) / get_territory_by_id(t_id, enemy_status['territories'])['num_armies']
    return bsr

# TODO: 4.5.5 - distance to frontier

# 4.5.6
def enemy_expected_reinforcements_feature(map_layout, player_status, enemy_status):
    enemy_expected_reinforcements = max(len(enemy_status['territories']) / 3, 3)
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(enemy_territory_ids)):
            enemy_expected_reinforcements += c['continent_bonus']
    return enemy_expected_reinforcements

# 4.5.7
def enemy_occupied_continents_feature(map_layout, player_status, enemy_status):
    enemy_occupied_continents = 0
    enemy_territory_ids = [t['territory'] for t in enemy_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(enemy_territory_ids)):
            enemy_occupied_continents += 1
    return enemy_occupied_continents

# 4.5.8
def hinterland_feature(map_layout, player_status, enemy_status):
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
def more_than_one_army_feature(map_layout, player_status, enemy_status):
    fortified = 0
    total = 0
    for t in player_status['territories']:
        if t['num_armies'] > 1:
            fortified += 1
        total += 1
    return float(fortified) / total

# 4.5.11
def occupied_territories_feature(map_layout, player_status, enemy_status):
    return float(len(player_status['territories'])) / (len(player_status['territories']) + len(enemy_status['territories']))

# 4.5.12
def our_expected_reinforcements_feature(map_layout, player_status, enemy_status):
    our_expected_reinforcements = max(len(player_status['territories']) / 3, 3)
    player_territory_ids = set([t['territory'] for t in player_status['territories']])
    for c in map_layout['continents']:
        if set(c['territories']).issubset(player_territory_ids):
            our_expected_reinforcements += c['continent_bonus']
    return our_expected_reinforcements

# 4.5.13
def own_occupied_continents_feature(map_layout, player_status, enemy_status):
    player_occupied_continents = 0
    player_territory_ids = [t['territory'] for t in player_status['territories']]
    for c in map_layout['continents']:
        if set(c['territories']).issubset(set(player_territory_ids)):
            player_occupied_continents += 1
    return player_occupied_continents

    # # Debug only
    # if debug:
    #     print "Enemy Reinf: " + str(timeit.timeit(enemy_expected_reinforcements_feature, number=10))
    #     print "Hinter: " + str(timeit.timeit(hinterland_feature, number=10))
    #     print "Our Cont: " + str(timeit.timeit(own_occupied_continents_feature, number=10))
    #     # print "Armies: " + str(armies_feature())
    #     # print "Enemy Reinf: " + str(enemy_expected_reinforcements_feature())
    #     # print "Enemy Cont: " + str(enemy_occupied_continents_feature())
    #     # print "Hinter: " + str(hinterland_feature())
    #     # print ">1 Army: " + str(more_than_one_army_feature())
    #     # print "Our Terr: " + str(occupied_territories_feature())
    #     # print "Our Reinf: " + str(our_expected_reinforcements_feature())
    #     # print "Our Cont: " + str(own_occupied_continents_feature())

    # return armies_feature() * 0.6 + \
    #     enemy_expected_reinforcements_feature() * -0.3 + \
    #     enemy_occupied_continents_feature() * -0.3 + \
    #     hinterland_feature() * 0.3 + \
    #     more_than_one_army_feature() * -0.1 + \
    #     occupied_territories_feature() * 0.2 + \
    #     our_expected_reinforcements_feature() * 0.2 + \
    #     own_occupied_continents_feature() * 1.0

def evaluate_reinforce(map_layout, player_status, enemy_status): # 0.0001
    # armies_feature is constant
    # more_than_one_army_feature is constant
    # return armies_feature(map_layout, player_status, enemy_status) * 0.6 + \
    return continent_safety_feature(map_layout, player_status, enemy_status) * -0.5 + \
        continent_threat_feature(map_layout, player_status, enemy_status) * 0.05 + \
        enemy_expected_reinforcements_feature(map_layout, player_status, enemy_status) * -0.3
        # more_than_one_army_feature(map_layout, player_status, enemy_status) * -0.1

def evaluate_battle(map_layout, player_status, enemy_status): # 0.0001
    return armies_feature(map_layout, player_status, enemy_status) * 0.6 + \
        continent_safety_feature(map_layout, player_status, enemy_status) * -0.01 + \
        continent_threat_feature(map_layout, player_status, enemy_status) * 0.05 + \
        enemy_expected_reinforcements_feature(map_layout, player_status, enemy_status) * -0.3 + \
        enemy_occupied_continents_feature(map_layout, player_status, enemy_status) * -0.5 + \
        hinterland_feature(map_layout, player_status, enemy_status) * 0.1 + \
        more_than_one_army_feature(map_layout, player_status, enemy_status) * -0.1 + \
        occupied_territories_feature(map_layout, player_status, enemy_status) * 0.7 + \
        our_expected_reinforcements_feature(map_layout, player_status, enemy_status) * 0.2 + \
        own_occupied_continents_feature(map_layout, player_status, enemy_status) * 0.7

def evaluate_fortify(map_layout, player_status, enemy_status): # 0.0001
    # armies feature is constant
    # more_than_one_army_feature is constant
    # return armies_feature(map_layout, player_status, enemy_status) * 0.6 + \
    return continent_safety_feature(map_layout, player_status, enemy_status) * -0.3 + \
        continent_threat_feature(map_layout, player_status, enemy_status) * 0.05 + \
        enemy_expected_reinforcements_feature(map_layout, player_status, enemy_status) * -0.3
        # more_than_one_army_feature(map_layout, player_status, enemy_status) * -0.1

if __name__ == "__main__":
    import AIBase
    b = AIBase.AIBase()
    print b.game_id
    time.sleep(5)
    b._refresh_state()
    map_layout = b.map_layout
    player_status = b.get_player_status()
    enemy_status = b.get_enemy_status()
    # from utils import wrapper
    # wrapped = wrapper(evaluate, b.map_layout, b.player_status, b.get_enemy_status())
    # import timeit
    # print "Evaluate (s): " + str(timeit.Timer(wrapped).timeit(number=100)/100)
        