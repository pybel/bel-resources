# -*- coding: utf-8 -*-

"""Utilities for handling OBO."""

import json
from typing import Callable, Union

import networkx as nx
import obonet

from bel_resources import write_namespace

__all__ = [
    'convert_obo_to_belns',
]

EncodingFunction = Callable[[nx.MultiDiGraph, str], str]


def convert_obo_to_belns(url: str,
                         path: str,
                         use_names: bool = False, encoding: Union[str, EncodingFunction] = None,
                         ) -> None:
    """Convert an OBO file to a BEL namespace."""
    graph = obonet.read_obo(url)

    name = graph.graph['name']
    ontology = graph.graph['ontology']

    if isinstance(encoding, str):
        x = encoding
        encoding = lambda _, __: x

    if use_names:
        values = {
            data['name']: encoding(graph, node)
            for node, data in graph.nodes(data=True)
            if node.startswith(ontology.upper() + ':')
        }
    else:
        values = {
            node[1 + len(ontology):]: encoding
            for node in graph
            if node.startswith(ontology.upper() + ':')
        }

    with open(path, 'w') as file:
        write_namespace(
            values=values,
            namespace_name=name,
            namespace_keyword=ontology,
            namespace_domain=None,
            namespace_version=graph.graph['data-version'],
            file=file,
        )


def convert_obo_to_belanno(url: str, path: str):
    """Convert an OBO file to a BEL annotation."""
    graph = obonet.read_obo(url)
    print(json.dumps(graph.graph, indent=2))
    name = graph.graph['name']
    ontology = graph.graph['ontology']

    values = {
        node[1 + len(ontology):]: 'P'
        for node in graph
        if node.startswith(ontology.upper() + ':')
    }

    with open(path, 'w') as file:
        write_namespace(
            values=values,
            namespace_name=name,
            namespace_keyword=ontology,
            namespace_domain=None,
            namespace_version=graph.graph['data-version'],
            file=file,
        )


if __name__ == '__main__':
    convert_obo_to_belns(
        url='http://purl.obolibrary.org/obo/doid.obo',
        path='/Users/cthoyt/Desktop/doid-names.belns',
        use_names=True,
        encoding='O',
    )
