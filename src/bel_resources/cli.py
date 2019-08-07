# -*- coding: utf-8 -*-

"""A command line interface for BEL Resources.

Why does this file exist, and why not put this in ``__main__``?
You might be tempted to import things from ``__main__`` later, but that will cause
problems--the code will get executed twice:
 - When you run `python3 -m bel_resources` python will execute
   ``__main__.py`` as a script. That means there won't be any
   ``bel_resources.__main__`` in ``sys.modules``.
 - When you import __main__ it will get executed again (as a module) because
   there's no ``bel_resources.__main__`` in ``sys.modules``.
Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import sys
from getpass import getuser

import click
from bel_resources import parse_bel_resource, write_annotation, write_namespace
from bel_resources.constants import NAMESPACE_DOMAIN_OTHER


@click.group()
@click.version_option()
def main():
    """Command Line Interface for BEL Resources."""


@main.group()
def namespace():
    """Namespace file utilities."""


@namespace.command()
@click.argument('name')
@click.argument('keyword')
@click.argument('domain')
@click.argument('citation')
@click.option('--author', default=getuser())
@click.option('--description')
@click.option('--species')
@click.option('--version')
@click.option('--contact')
@click.option('--license')
@click.option('--values', default=sys.stdin, help="A file containing the list of names")
@click.option('--output', type=click.File('w'), default=sys.stdout)
def write(name, keyword, domain, citation, author, description, species, version, contact, license, values, output):
    """Build a namespace from items."""
    write_namespace(
        name, keyword, domain, author, citation, values,
        namespace_description=description,
        namespace_species=species,
        namespace_version=version,
        author_contact=contact,
        author_copyright=license,
        file=output,
    )


@namespace.command()
@click.option('-f', '--file', type=click.File('r'), default=sys.stdin, help="Path to input BEL Namespace file")
@click.option('-o', '--output', type=click.File('w'), default=sys.stdout,
              help="Path to output converted BEL Annotation file")
def convert_to_annotation(file, output):
    """Convert a namespace file to an annotation file."""
    resource = parse_bel_resource(file)

    write_annotation(
        keyword=resource['Namespace']['Keyword'],
        values={k: '' for k in resource['Values']},
        citation_name=resource['Citation']['NameString'],
        description=resource['Namespace']['DescriptionString'],
        file=output,
    )


@main.group()
def annotation():
    """Annotation file utilities."""


@annotation.command()
@click.option('-f', '--file', type=click.File('r'), default=sys.stdin, help="Path to input BEL Namespace file")
@click.option('-o', '--output', type=click.File('w'), default=sys.stdout,
              help="Path to output converted BEL Namespace file")
@click.option('--keyword', help="Set custom keyword. useful if the annotation keyword is too long")
@click.option('--author', default=getuser())
def convert_to_namespace(file, output, keyword, author):
    """Convert an annotation file to a namespace file."""
    resource = parse_bel_resource(file)

    write_namespace(
        namespace_keyword=(keyword or resource['AnnotationDefinition']['Keyword']),
        namespace_name=resource['AnnotationDefinition']['Keyword'],
        namespace_description=resource['AnnotationDefinition']['DescriptionString'],
        author_name=author,
        namespace_domain=NAMESPACE_DOMAIN_OTHER,
        values=resource['Values'],
        citation_name=resource['Citation']['NameString'],
        file=output,
    )
