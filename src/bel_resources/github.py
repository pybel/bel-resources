# -*- coding: utf-8 -*-

"""Tools for BEL namespaces on GitHub."""

import sys

import requests

FILE_API_URL = 'https://api.github.com/repos/{owner}/{repo}/commits?path={path}'
RAW_URL = 'https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{path}'


def get_github_hash(owner: str, repo: str, path: str) -> str:
    """Get the SHA hash corresponding to the most recent update to the BEL namespace file on a GitHub repository."""
    url = FILE_API_URL.format(owner=owner, repo=repo, path=path.lstrip('/'))
    res = requests.get(url)
    res_json = res.json()
    most_recent_commit = res_json[0]
    return most_recent_commit['sha']


def get_github_url(owner: str, repo: str, path: str) -> str:
    """Get the URL corresponding to the most recent update to the BEL namespace file on a GitHub repository."""
    sha = get_github_hash(owner, repo, path)
    return RAW_URL.format(owner=owner, repo=repo, sha=sha, path=path.lstrip('/'))


def get_conso_names_url() -> str:
    """Get the URL for the most recent version of Curation of Neurodegeneration Supporting Ontology (CONSO) names."""
    return get_github_url('pharmacome', 'conso', 'export/conso-names.belns')


def get_conso_identifiers_url() -> str:
    """Get the URL for the most recent version of CONSO identifiers."""
    return get_github_url('pharmacome', 'conso', 'export/conso.belns')


def get_famplex_url() -> str:
    """Get the URL for the most recent version of FamPlex names."""
    return get_github_url('sorgerlab', 'famplex', 'export/famplex.belns')


if __name__ == '__main__':
    print(get_github_hash(*sys.argv[1:4]))
