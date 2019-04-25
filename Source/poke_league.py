from datetime import datetime

from Source.config import database
from Source.poke_data import PokeData


def create_stats():
    return dict(victories=0, losses=0, draw=0)


def get_ranking(contender=None):
    if 'stats' not in contender:
        return 0, 0, 0

    return (-contender['stats']['victories'],
            -contender['stats']['draw'],
            contender['stats']['losses'])


def power_combat(player=None):
    power = 0.0
    for pokemon in player.get('pokemons', []):
        for move in pokemon.get('moves', []):
            power += (move.get('power', 0) * (move.get('accuracy', 0) / 100.0))
    return power


class PokeLeague:
    methods = dict()

    def __init__(self):
        self.data = database["poke-leagues"]
        self.methods.update({
            'new-league': {
                'exc': self.new_league,
                'Async': True
            },
            'new-contender': {
                'exc': self.new_contender,
                'Async': True
            },
            'fight': {
                'exc': self.fight,
                'Async': True
            },
            'friendly-fight': {
                'exc': self.friendly_fight,
                'Async': False
            },
            'list': {
                'exc': self.get_all_leagues,
                'Async': False
            },
            'ranking': {
                'exc': self.ranking,
                'Async': False
            },
        })

    def friendly_fight(self, **kwargs):
        player_1_name = kwargs.get('player1', False)
        player_2_name = kwargs.get('player2', False)
        if not all([player_1_name, player_2_name]):
            return 'not enough player names for a friendly fight'

        result = dict()
        contenders = [_contender
                      for league in self.data.find()
                      for _contender in league['contenders']
                      if _contender['name'] in [player_1_name, player_2_name]]
        resume_player1 = dict(
            name=contenders[0]['name'],
            power_combat=power_combat(contenders[0])
        )
        resume_player2 = dict(
            name=contenders[1]['name'],
            power_combat=power_combat(contenders[1])
        )
        if resume_player1['power_combat'] > resume_player2['power_combat']:
            result['win'] = resume_player1['name']
        elif resume_player1['power_combat'] < resume_player2['power_combat']:
            result['win'] = resume_player2['name']
        else:
            result['draw'] = True
        result['contenders'] = list([
            resume_player1,
            resume_player2
        ])

        return result

    def ranking(self, **kwargs):
        league = kwargs.get('league', None)
        finder = self.data.find() if not league else self.data.find(dict(name=league))
        all_contenders = [j for i in finder for j in i['contenders']]
        return sorted(
            all_contenders,
            key=lambda x: get_ranking(x)
        )

    def fight(self, **kwargs):
        league = kwargs.get('league', False)
        player_1_name = kwargs.get('player1', False)
        player_2_name = kwargs.get('player2', False)

        if not all([league, player_1_name, player_2_name]):
            return False

        for league in self.data.find({'name': league}):
            player_1 = sorted(league['contenders'],
                              key=lambda x: x['name'] == player_1_name,
                              reverse=True)[0]
            player_2 = sorted(league['contenders'],
                              key=lambda x: x['name'] == player_2_name,
                              reverse=True)[0]

            if not all([player_1['name'] == player_1_name, player_2['name'] == player_2_name]):
                return False
            league['contenders'].remove(player_1)
            league['contenders'].remove(player_2)

            power_1 = power_combat(player_1)

            power_2 = power_combat(player_2)

            if 'stats' not in player_1:
                player_1['stats'] = create_stats()
            if 'stats' not in player_2:
                player_2['stats'] = create_stats()

            if power_1 > power_2:
                player_1['stats']['victories'] += 1
                player_2['stats']['losses'] += 1

            elif power_2 > power_1:
                player_2['stats']['victories'] += 1
                player_1['stats']['losses'] += 1

            else:
                player_1['stats']['draw'] += 1
                player_2['stats']['draw'] += 1

            league['contenders'].append(player_1)
            league['contenders'].append(player_2)

            self.data.update({'name': league['name']}, league)
            return True

    def new_league(self, **kwargs):
        if 'name' not in kwargs:
            return False

        for _ in self.data.find({'name': kwargs.get('name')}):
            return False

        league = dict()
        league['name'] = kwargs.get('name')
        league['contenders'] = list()
        league['created'] = datetime.now()
        league['open'] = True

        self.data.insert_one(league)

    def get_all_leagues(self, **kwargs):
        leagues = self.data.find()
        data = [dict(
            name=x['name'],
            created=x.get('created', None),
            contenders=x['contenders'],
            open=x['open']
        ) for x in leagues]
        return data

    def new_contender(self, **kwargs):
        request_league = kwargs.get('league', None)
        contender_name = kwargs.get('contender_name', None)
        contender_pokemons = kwargs.get('contender_pokemons', None)
        if not request_league:
            return False
        for league in self.data.find({'name': request_league}):
            for contender in league['contenders']:
                if contender['name'] == contender_name:
                    return False
            chinese_draw = PokeData().get_chinese_draw(contender_pokemons)
            league['contenders'].append({
                'name': contender_name,
                'pokemons': list(chinese_draw)
            })
            self.data.update({'name': request_league}, league)

    def exc(self, **kwargs):
        task = kwargs.get('task', None)
        method = self.methods.get(task, None)

        if not method:
            raise Exception('Invalid task required')
        return method['exc'](**kwargs)
