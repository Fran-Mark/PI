import click

@click.command()
@click.option('--name', prompt='Your name', help='Your name', required=True)
@click.argument('number')
def cli(name, number):
    for i in range(int(number)):
        print("Hello, " + name + "!")

