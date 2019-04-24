from flask import Flask
from flask import jsonify
from flask import request

from Source.flask_celery import make_celery
from Source.poke_data import PokeData
from Source.poke_league import PokeLeague

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)


@app.route('/poke-data/<task>', methods=['GET', 'POST'])
def poke_data(task):
    kwargs_request = dict(request.get_json() or {})
    kwargs_request.update(dict(request.args))
    kwargs_request.update(dict(task=task))

    _task = PokeData()
    with_celery = _task.methods.get(task, {}).get('Async', False)

    if with_celery:
        execute_poke_task.delay(**kwargs_request)
        return jsonify({
            'status': 200,
            'data': {
                'Async': True,
            }
        })

    data = _task.exc(**kwargs_request)
    return jsonify({
        'status': 200,
        'data': {
            'result': data
        }
    })


@app.route('/poke-league/<task>', methods=['GET', 'POST'])
def poke_league(task):
    kwargs_request = dict(request.get_json() or {})
    kwargs_request.update(dict(request.args))
    kwargs_request.update(dict(task=task))

    _task = PokeLeague()
    with_celery = _task.methods.get(task, {}).get('Async', False)

    if with_celery:
        execute_poke_league.delay(**kwargs_request)
        return jsonify({
            'status': 200,
            'data': {
                'Async': True,
            }
        })

    data = _task.exc(**kwargs_request)
    return jsonify({
        'status': 200,
        'data': {
            'result': data
        }
    })


@celery.task(name='app.poke-task')
def execute_poke_task(**kwargs):
    return PokeData().exc(**kwargs)


@celery.task(name='app.poke-league')
def execute_poke_league(**kwargs):
    return PokeLeague().exc(**kwargs)


if __name__ == '__main__':
    app.run(debug=True)
