import random

import requests

from Source.config import database
from Source.settings import CONFIG


class PokeData:
    methods = dict()

    def __init__(self):
        self.data = database["poke-monsters"]
        self.methods.update({
            'update': {
                'exc': self.update,
                'Async': True
            },
            'list': {
                'exc': self.retrieve_all,
                'Async': False
            },
            'update-powers': {
                'exc': self.pokemons_get_powers,
                'Async': True
            },
        })

    def update(self, **kwargs):
        all_pokemons = list()
        response = requests.get(CONFIG['url-poke-list']).json()
        while response.get('next', None):
            all_pokemons += response['results']
            response = requests.get(response['next']).json()
        all_pokemons += response['results']
        self.data.drop()
        self.data.insert_many(all_pokemons)
        return True

    def pokemons_get_powers(self, **kwargs):
        chinese_draw = kwargs.get('pokemon', None)
        if not chinese_draw:
            return False

        key = dict(name=chinese_draw['name'])
        new_data = dict(chinese_draw)
        new_data['moves'] = list()
        new_data['moves_url'] = list(requests.get(chinese_draw['url']).json()['moves'])
        for x in new_data['moves_url']:
            data = requests.get(x['move']['url']).json()
            new_data['moves'].append(dict(
                name=x['move']['name'],
                power=data['power'] or 0,
                accuracy=data['accuracy'] or 0
            ))
        self.data.update_one(key, {"$set": new_data})
        return True

    def retrieve_all(self, **kwargs):
        pokemons = self.data.find()
        data = [dict(
            name=x['name'],
            moves=x.get('moves', None) or []
        ) for x in pokemons]
        return data

    def exc(self, **kwargs):
        task = kwargs.get('task', None)
        method = self.methods.get(task, None)

        if not method:
            raise Exception('Invalid task required')
        return method['exc'](**kwargs)

    def get_chinese_draw(self, contender_pokemons):
        contender_pokemons = int(contender_pokemons)
        poke_data = list(self.data.find())
        random.shuffle(poke_data)
        chosen = list(poke_data[:contender_pokemons])

        for i in range(contender_pokemons):
            if not chosen[i].get('moves', None):
                chosen[i] = self.pokemon_get_power(chosen[i])

        return list([dict(name=x['name'],
                          url=x['url'],
                          moves=x['moves'])
                     for x
                     in chosen])

    def pokemon_get_power(self, chinese_draw):
        key = dict(name=chinese_draw['name'])
        new_data = dict(chinese_draw)
        new_data['moves'] = list()
        new_data['moves_url'] = list(requests.get(chinese_draw['url']).json()['moves'])
        for x in new_data['moves_url']:
            print(f'{new_data["name"]} is getting power: {x["move"]["name"]}')
            data = requests.get(x['move']['url']).json()
            new_data['moves'].append(dict(
                name=x['move']['name'],
                power=data['power'] or 0,
                accuracy=data['accuracy'] or 0
            ))
        self.data.update_one(key, {"$set": new_data})
        return new_data
