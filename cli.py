import click
import random

from transformations import transformations


choices = transformations.keys()


@click.command()
@click.option('--transformation', type=click.Choice(choices))
@click.option('--person', multiple=True, help='Repeatable.',
              default=['Jack Sprat', 'Benjamin Bunny', 'Mrs. Tiggywinkle'])
def order(transformation, person):
    """ Print a random order of people, possibly transformed. """
    if transformation is None:
        transformation = random.choice(list(transformations.keys()))
    people = list(person)
    random.shuffle(people)
    for p in people:
        click.echo(transformations[transformation](p))


if __name__ == '__main__':
    order()
