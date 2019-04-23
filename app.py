from flask import Flask
from flask import jsonify

from Source.flask_celery import make_celery
from Source.poke_data import PokeData

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)


@app.route('/poke-data/<task>')
def poke_data(task):
    _task = PokeData()
    with_celery = _task.methods.get(task, {}).get('Async', False)
    if with_celery:
        execute_poke_task.delay(task)
        return jsonify({
            'status': 200,
            'data': {
                'Async': True,
            }
        })
    data = _task.exc(task=task)
    return jsonify({
        'status': 200,
        'data': {
            'result': data
        }
    })


@celery.task(name='app.poke-task')
def execute_poke_task(task):
    return PokeData().exc(task=task)


if __name__ == '__main__':
    app.run(debug=True)
