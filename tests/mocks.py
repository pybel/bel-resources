# -*- coding: utf-8 -*-

"""Mocks for PyBEL testing."""

from unittest import mock

from tests.constants import TEST_ANNOTATION_PATH, TEST_NAMESPACE_EMPTY_PATH

__all__ = [
    'MockResponse',
    'MockSession',
    'mock_bel_resources',
]


class MockResponse:
    """See http://stackoverflow.com/questions/15753390/python-mock-requests-and-the-response."""

    def __init__(self, url_to_mock: str):
        """Build a mock for the requests Response object."""
        if url_to_mock.endswith('test_an_1.belanno'):
            self.path = TEST_ANNOTATION_PATH

        elif url_to_mock.endswith('test_ns_empty.belns'):
            self.path = TEST_NAMESPACE_EMPTY_PATH

        else:
            raise ValueError

    def iter_lines(self):
        """Iterate the lines of the mock file."""
        with open(self.path, 'rb') as file:
            yield from file

    def raise_for_status(self):
        """Mock raising an error, by not doing anything at all."""


class MockSession:
    """Patches the session object so requests can be redirected through the filesystem without rewriting BEL files."""

    def mount(self, prefix, adapter):
        """Mock mounting an adapter by not doing anything."""

    @staticmethod
    def get(url: str):
        """Mock getting a URL by returning a mock response."""
        return MockResponse(url)

    def close(self):
        """Mock closing a connection by not doing anything."""


mock_bel_resources = mock.patch('bel_resources.utils.requests.Session', side_effect=MockSession)
