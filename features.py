import time
from utils import get_territory_by_id
from collections import deque
import math
    
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
def distance_to_frontier_feature(map_layout, player_status, enemy_status):
    td = 0
    for t in player_status['territories']:
        td += (_distance(t['territory'], map_layout, player_status, enemy_status) * t['num_armies'])
    return float(player_status['num_armies']) / td

def _distance(t_id, map_layout, player_status, enemy_status):
    q = deque()
    path = (t_id, )
    q.append(path)
    visited = set([t_id])
    while q:
        path = q.popleft()
        last_node = path[-1]
        if get_territory_by_id(last_node, enemy_status['territories']):
            return len(path) - 1
        for node in get_territory_by_id(last_node, map_layout['territories'])['adjacent_territories']:
            if node not in visited:
                visited.add(node)
                q.append(path + (node, ))
    return 99999

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

def partial_continent_score_feature(map_layout, player_status, enemy_status):
    partial_continent_score = 0
    player_territory_ids = [t['territory'] for t in player_status['territories']]
    for c in map_layout['continents']:
        we_have = 0
        for t_id in c['territories']:
            if t_id in player_territory_ids:
                we_have += 1
        partial_continent_score += ((float(we_have) / len(c['territories'])) ** 2) * c['rating']
    return partial_continent_score

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
    # return armies_feature(map_layout, player_status, enemy_status) * 0.6 + \
    return continent_safety_feature(map_layout, player_status, enemy_status) * -20 + \
        continent_threat_feature(map_layout, player_status, enemy_status) * 1 + \
        enemy_expected_reinforcements_feature(map_layout, player_status, enemy_status) * -0.3 + \
        distance_to_frontier_feature(map_layout, player_status, enemy_status) * 10
        # more_than_one_army_feature(map_layout, player_status, enemy_status) * -0.05

def evaluate_battle(map_layout, player_status, enemy_status): # 0.0001
    a = armies_feature(map_layout, player_status, enemy_status)
    b = continent_safety_feature(map_layout, player_status, enemy_status)
    c = continent_threat_feature(map_layout, player_status, enemy_status)
    d = enemy_expected_reinforcements_feature(map_layout, player_status, enemy_status)
    e = enemy_occupied_continents_feature(map_layout, player_status, enemy_status)
    f = hinterland_feature(map_layout, player_status, enemy_status)
    g = more_than_one_army_feature(map_layout, player_status, enemy_status)
    h = occupied_territories_feature(map_layout, player_status, enemy_status)
    i = our_expected_reinforcements_feature(map_layout, player_status, enemy_status)
    j = own_occupied_continents_feature(map_layout, player_status, enemy_status)
    k = partial_continent_score_feature(map_layout, player_status, enemy_status)
    # print "armies feature: %f" % a
    # print "continent safety feature: %f" % b
    # print "continent threat feature: %f" % c
    # print "enemy expected reinforcements feature: %f" % d
    # print "enemy occupied continents feature: %f" % e
    # print "hinterland feature: %f" % f
    # print "more than one army feature: %f" % g
    # print "occupied territories feature: %f" % h
    # print "our expected reinforcements feature: %f" % i
    # print "own occupied continents feature: %f" % j
    # print "partial continent score feature: %f" % k
    # print "\n"
    # Continent first strategy
    # return a * 1 * 0.05 + \
    #     b * 0.2 * -0.1 + \
    #     c * 0.05 * 0.2 + \
    #     d * 0.02 * -0.1 + \
    #     e * 0.1 * -0.2 + \
    #     f * 0.033 * 0.001 + \
    #     g * 1 * -0.05 + \
    #     h * 1 * 0.3 + \
    #     i * 0.05 * 0.3 + \
    #     j * 0.2 * 0.5
    # Aggressive conquest, with focus on continent protection
    return a * 1 * 0.1 + \
    b * 0.2 * -50 + \
    c * 0.05 * 0.1 + \
    d * 0.02 * -0.1 + \
    e * 0.1 * -0.1 + \
    f * 0.033 * 0.1 + \
    g * 1 * -0.1 + \
    h * 1 * 20 + \
    i * 0.05 * 20 + \
    j * 0.2 * 20 + \
    k * 1 * 20

def evaluate_fortify(map_layout, player_status, enemy_status): # 0.0001
    # armies feature is constant
    # return armies_feature(map_layout, player_status, enemy_status) * 0.6 + \
    return continent_safety_feature(map_layout, player_status, enemy_status) * -0.3 + \
        continent_threat_feature(map_layout, player_status, enemy_status) * 1 + \
        enemy_expected_reinforcements_feature(map_layout, player_status, enemy_status) * -0.3 + \
        more_than_one_army_feature(map_layout, player_status, enemy_status) * 0.1 + \
        distance_to_frontier_feature(map_layout, player_status, enemy_status) * 50

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
        