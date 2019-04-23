import requests
from flask import jsonify

from Source.config import database
from Source.settings import CONFIG


class PokeData:
    def __init__(self):
        self.data = database["poke-monsters"]

    def update(self, **kwargs):
        all_pokemons = list()
        response = requests.get(CONFIG['url-poke-list']).json()
        while response.get('next', None):
            all_pokemons += response['results']
            response = requests.get(response['next']).json()
        all_pokemons += response['results']
        self.data.drop()
        self.data.insert_many(all_pokemons)
        return "holi"

    def pokemons_get_powers(self, **kwargs):
        pokemons = self.data.find()
        for chinense_draw in pokemons[0:1]:
            key = dict(_id=chinense_draw['_id'])
            new_data = dict(chinense_draw)
            new_data['moves'] = list()
            new_data['moves_url'] = list(requests.get(chinense_draw['url']).json()['moves'])
            for x in new_data['moves_url']:
                print(x['move'].keys())
                data = requests.get(x['move']['url']).json()
                new_data['moves'].append(dict(
                    name=x['move']['name'],
                    power=data['power'],
                    accuracy=data['accuracy']
                ))

            # chinense_draw = requests.get(chinense_draw['url'])
            self.data.update_one(key, { "$set": new_data})
        return jsonify(
            {
                'status': 200,
                'data': 'done'
            }
        )

    def retrieve_all(self, **kwargs):
        pokemons = self.data.find()
        data = [dict(
            name=x['name'],
            moves=x.get('moves', None)
        ) for x in pokemons]
        print(f'data es: {data}')
        return jsonify(
            {
                'status': 200,
                'data': data
            }
        )

    # @staticmethod
    def exc(self, **kwargs):
        methods = {
            'update': self.update,
            'list': self.retrieve_all,
            'update-powers': self.pokemons_get_powers,
        }

        task = kwargs.get('task', None)
        method = methods.get(task, None)

        if not method:
            raise Exception('Invalid task required')
        return method(**kwargs)
