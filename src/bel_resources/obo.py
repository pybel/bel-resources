# -*- coding: utf-8 -*-

"""Utilities for handling OBO."""

from typing import Callable, Optional, TextIO, Union

import networkx as nx
import obonet

from bel_resources import write_namespace

__all__ = [
    'convert_obo_to_belns',
    'convert_obo_graph_to_belns',
    'convert_obo_to_belanno',
    'convert_obo_graph_to_belanno',
]

EncodingFunction = Callable[[nx.MultiDiGraph, str], str]


def convert_obo_to_belns(url: str,
                         path: str,
                         use_names: bool = False,
                         encoding: Union[str, EncodingFunction] = None,
                         ) -> None:
    """Convert an OBO file to a BEL namespace."""
    graph = obonet.read_obo(url)
    with open(path, 'w') as file:
        convert_obo_graph_to_belns(graph, file=file, use_names=use_names, encoding=encoding)


def convert_obo_graph_to_belns(graph: nx.MultiDiGraph,
                               file: Optional[TextIO] = None,
                               use_names: bool = False,
                               encoding: Union[None, str, EncodingFunction] = None,
                               process_identifiers: Optional[Callable[[str], str]] = None,
                               ) -> None:
    name = graph.graph['name']
    ontology = graph.graph['ontology']

    if encoding is None:
        encoding = ''

    if isinstance(encoding, str):
        x = encoding
        encoding = lambda _, __: x

    if use_names:
        values = {
            data['name']: encoding(graph, node)
            for node, data in graph.nodes(data=True)
            if node.startswith(ontology.upper() + ':')
        }
    elif process_identifiers is not None:
        values = {
            process_identifiers(node): encoding(graph, node)
            for node in graph
            if node.startswith(ontology.upper() + ':')
        }
    else:
        values = {
            node: encoding(graph, node)
            for node in graph
            if node.startswith(ontology.upper() + ':')
        }

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
    with open(path, 'w') as file:
        convert_obo_graph_to_belanno(graph, file=file)


def convert_obo_graph_to_belanno(graph: nx.MultiDiGraph, file: Optional[TextIO] = None, ) -> None:
    """Convert an OBO graph to a BEL annotation."""
    name = graph.graph['name']
    ontology = graph.graph['ontology']

    values = {
        node[1 + len(ontology):]: 'P'
        for node in graph
        if node.startswith(ontology.upper() + ':')
    }

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
