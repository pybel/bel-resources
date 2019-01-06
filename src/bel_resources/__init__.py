# -*- coding: utf-8 -*-

"""Utilities for downloading, reading, and writing BEL script, namespace files, and annotation files."""

from .exc import EmptyResourceError, InvalidResourceError, MissingResourceError, ResourceError  # noqa: F401
from .read_document import split_file_to_annotations_and_definitions  # noqa: F401
from .read_utils import get_bel_resource, get_lines, parse_bel_resource  # noqa: F401
from .write_annotation import write_annotation  # noqa: F401
from .write_document import make_knowledge_header  # noqa: F401
from .write_namespace import write_namespace  # noqa: F401
