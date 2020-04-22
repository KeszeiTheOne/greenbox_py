import click
from app.UpdateSensor import UpdateSensorAction

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):


if __name__ == '__main__':
    hello()
