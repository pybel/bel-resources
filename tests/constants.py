# -*- coding: utf-8 -*-

"""Testing resources for PyBEL."""

import os

HERE = os.path.dirname(os.path.realpath(__file__))

RESOURCES_DIRECTORY_PATH = os.path.join(HERE, 'resources')

TEST_ANNOTATION_PATH = os.path.join(RESOURCES_DIRECTORY_PATH, 'test_an_1.belanno')
assert os.path.exists(TEST_ANNOTATION_PATH)

TEST_NAMESPACE_EMPTY_PATH = os.path.join(RESOURCES_DIRECTORY_PATH, 'test_ns_empty.belns')
assert os.path.exists(TEST_NAMESPACE_EMPTY_PATH)
