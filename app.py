from flask import Flask
from Source.flask_celery import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

celery = make_celery(app)


@app.route('/process/<name>')
def process(name):
    return name[::-1]


@app.route('/celery/count/<number>')
def count_celery(number):
    print_for.delay(int(number))
    return number


@celery.task(name='app.print_for')
def print_for(number):
    for _ in range(number):
        print(_)


if __name__ == '__main__':
    app.run(debug=True)
