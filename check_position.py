import json
import requests
from yahoo_oauth import OAuth2
from bs4 import BeautifulSoup
from argparse import ArgumentParser

class Player(object):

    def __init__(self, contents):
        for item in contents:
            if isinstance(item, dict):
                for key, val in item.items():
                    self.__dict__[key] = val

        self.__dict__['status'] = self.__dict__.get('status', None)

    def __repr__(self):
        return "Player<%s>" % self.name['full']

BASE_URL = 'https://fantasysports.yahooapis.com/fantasy/v2'
GAME_ID = 359
LEAGUE_ID = 1107081
LEAGUE = "%u.l.%u" % (GAME_ID, LEAGUE_ID)
TEAM_ID = 10
TEAM = "t.%u" % TEAM_ID

LEAGUE_URL = "%s/league/%s" % (BASE_URL, LEAGUE)
TEAM_URL = "%s/team/%s.%s" % (BASE_URL, LEAGUE, TEAM)

PLAYER_URL = "%s/players" % LEAGUE_URL
ROSTER_URL = "%s/roster/players" % TEAM_URL

FANTASY_PROS = "https://www.fantasypros.com/nfl/start/%s-%s.php"

oauth = OAuth2(None, None, from_file='keys.json')

if not oauth.token_is_valid():
    oauth.refresh_access_token()
# Example
response = oauth.session.get(TEAM_URL)


def request(url):
    result = oauth.session.get("%s?format=json" % url).text
    return json.loads(result)

def get_my_team():
    roster = request(ROSTER_URL)
    roster_size = roster['fantasy_content']['team'][1]['roster']['0']['players']['count']
    for i in range(roster_size):
        player = Player(roster['fantasy_content']['team'][1]['roster']['0']['players'][str(i)]['player'][0])
        yield player

def get_available_players(position, type):
    players = request("%s;count=10;status=%s;position=%s;sort_week=10;sort=PTS" % (PLAYER_URL, type, position))['fantasy_content']['league'][1]['players']
    player_count = players['count']
    for i in range(player_count):
        player = Player(players[str(i)]['player'][0])
        yield player

def start(player_a, player_b):
    a = '-'.join(player_a.lower().split(' '))
    b = '-'.join(player_b.lower().split(' '))
    url = FANTASY_PROS % (a, b)
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    result = soup.find_all('table', class_='full-width')[0].tbody.find_all('tr')[1].find_all('td')[1:]
    picks = [p.find('div', class_='player-name').text.strip() for p in result]
    return [player_a == picks[0], player_b == picks[0]]

def check_position(team, position):
    players = [t for t in team if position in [p['position'] for p in t.eligible_positions]]
    pos = "WR,RB,TE" if position == "W/R/T" else position
    waiver = list(get_available_players(pos, 'W'))
    free_agents = list(get_available_players(pos, 'FA'))
    for p in players:
        print("Checking: %s" % p.name['full'])
        for w in waiver + free_agents:
            try:
                comparison = start(p.name['full'], w.name['full'])
                if comparison[1]:
                    print("Better player: %s" % w.name['full'])
            except:
                pass

def parse_args():
    argparser = ArgumentParser()
    argparser.add_argument('position')
    return argparser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    my_team = list(get_my_team())

    check_position(my_team, args.position)
