import json
import urllib2, time
import config

class Brisk(object):
    HOST = 'http://www.briskchallenge.com'
    TEAM_NAME = 'BogoBot'

    def __init__(self, game_id=False, bot_id=1):
        res = self.join_game(game_id, bot_id)
        self.game_id = res['game']
        self.player_id = res['player']
        self.token = res['token']

    def join_game(self, game_id, bot_id):
        # data = { 'join': True, 'team_name': self.TEAM_NAME, 'token': config.TOKEN, "no_bot": True, "game": 1662066685}
        data = { 'join': True, 'team_name': self.TEAM_NAME, 'no_bot': True }
        res = self.post(self.url_root(), data)
        return res

    def url_root(self):
        return self.HOST + "/v1/brisk/game"

    def url_game(self):
        return self.url_root() + "/" + str(self.game_id)

    def url_player(self):
        return self.url_game() + "/player/" + str(self.player_id)

    def url_territory(self, territory_id):
        return self.url_player() + "/territory/" + str(territory_id)

    def post(self, url, data):
        req = urllib2.Request(url, json.dumps(data))
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            import pprint
            pp = pprint.PrettyPrinter()
            pp.pprint(self.get_game_state())
            pp.pprint(self.get_player_status())
            print url
            pp.pprint(data)
            raise e
        res = response.read()
        try:
            return json.loads(res)
        except ValueError:
            # probably empty respose so no JSON to decode
            return res

    def get(self, url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def get_game_state(self):
        return self.get(self.url_game())

    def get_map_layout(self):
        return self.get(self.url_game() + "?map=true")
        
    def get_player_status(self, lite=False):
        return self.get(self.url_player() + {False:"", True:"?check_turn=true"}[lite])

    def get_enemy_status(self):
        players = self.get_players_status()['players']
        if not players or len(players) == 1:
            return None
        enemy_id = players[0]['player'] if players[0]['player'] is not self.player_id else players[1]['player']
        return self.get(self.url_game() + "/player/" + str(enemy_id))

    def get_players_status(self):
        return self.get(self.url_game() + "/players")

    def get_territory_status(self, territory_id):
        territory = self.get_map_layout()['territories'][territory_id-1]
        territory.update(self.get_game_state()['territories'][territory_id-1])
        return territory

    def end_turn(self):
        return self.post(self.url_player(), {'token':self.token, 'end_turn':True})
        
    def get_history(self):
        return self.get(self.url_game() + "/history")

    def attack(self, attacker_territory_id, defender_territory_id, num_attacker_armies):
        url = self.url_territory(defender_territory_id)
        data = {'token':self.token, 'num_armies':num_attacker_armies, 'attacker':attacker_territory_id}
        return self.post(url, data)

    def place_armies(self, territory_id, num_armies):
        url = self.url_territory(territory_id)
        data = {'token':self.token, 'num_armies':num_armies}
        return self.post(url, data)

    def transfer_armies(self, from_territory_id, to_territory_id, num_armies):
        url = self.url_territory(from_territory_id)
        data = {'token':self.token, 'num_armies':num_armies, 'destination':to_territory_id}
        return self.post(url, data)

    def get_map_svg(self):
        url = self.url_game() + "?map=svg"
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read() # "<svg>\n ... </svg>"

    def reward(self):
        url = self.HOST + "/v1/brisk/reward.php"
        data = {'game':self.game_id, 'player':self.player_id, 'token':self.token}
        req = urllib2.Request(url, json.dumps(data))
        response = urllib2.urlopen(req)
        return response.read() # ???


# end class Brisk
