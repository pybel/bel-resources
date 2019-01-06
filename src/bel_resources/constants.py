# -*- coding: utf-8 -*-

"""Constants for reading and writing BEL script, namespace files, and annotation files."""

import re
from typing import Iterable

VERSION = '0.0.1'

METADATA_LINE_RE = re.compile(r"(SET\s+DOCUMENT|DEFINE\s+NAMESPACE|DEFINE\s+ANNOTATION)")

NAMESPACE_URL_FMT = 'DEFINE NAMESPACE {} AS URL "{}"'
NAMESPACE_PATTERN_FMT = 'DEFINE NAMESPACE {} AS PATTERN "{}"'
ANNOTATION_URL_FMT = 'DEFINE ANNOTATION {} AS URL "{}"'
ANNOTATION_PATTERN_FMT = 'DEFINE ANNOTATION {} AS PATTERN "{}"'
ANNOTATION_LIST_FMT = 'DEFINE ANNOTATION {} AS LIST {{{}}}'


def format_annotation_list(annotation: str, values: Iterable[str]) -> str:
    """Generate an annotation list definition."""
    return ANNOTATION_LIST_FMT.format(annotation, ', '.join('"{}"'.format(e) for e in sorted(values)))


NAMESPACE_DOMAIN_BIOPROCESS = 'BiologicalProcess'
NAMESPACE_DOMAIN_CHEMICAL = 'Chemical'
NAMESPACE_DOMAIN_GENE = 'Gene and Gene Products'
NAMESPACE_DOMAIN_OTHER = 'Other'
#: The valid namespace types
#: .. seealso:: https://wiki.openbel.org/display/BELNA/Custom+Namespaces
NAMESPACE_DOMAIN_TYPES = {
    NAMESPACE_DOMAIN_BIOPROCESS,
    NAMESPACE_DOMAIN_CHEMICAL,
    NAMESPACE_DOMAIN_GENE,
    NAMESPACE_DOMAIN_OTHER
}
