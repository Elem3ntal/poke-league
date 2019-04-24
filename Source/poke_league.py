from datetime import datetime

from Source.config import database
from Source.poke_data import PokeData


class PokeLeague:
    methods = dict()

    def __init__(self):
        self.data = database["poke-leagues"]
        self.methods.update({
            'new-league': {
                'exc': self.new_league,
                'Async': True
            },
            'list': {
                'exc': self.get_all_leagues,
                'Async': False
            },
            'new-contender': {
                'exc': self.new_contender,
                'Async': True
            }
        })

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
