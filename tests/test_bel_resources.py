# -*- coding: utf-8 -*-

"""Tests for utilities for BEL resources."""

import time
import unittest

from bel_resources import EmptyResourceError, get_bel_resource, split_file_to_annotations_and_definitions
from bel_resources.read_document import sanitize_file_lines
from bel_resources.utils import get_iso_8601_date
from tests.constants import TEST_ANNOTATION_PATH, TEST_NAMESPACE_EMPTY_PATH
from tests.examples import simple
from tests.mocks import mock_bel_resources


class TestUtils(unittest.TestCase):
    """Test utilities."""

    def test_get_date(self):
        """Test getting the date."""
        d = get_iso_8601_date()
        self.assertIsInstance(d, str)
        self.assertEqual(d[:4], time.strftime('%Y'))
        self.assertEqual(d[4:6], time.strftime('%m'))
        self.assertEqual(d[6:8], time.strftime('%d'))


class TestBELResources(unittest.TestCase):
    """Test utilities for BEL resources."""

    def test_raises_on_empty(self):
        """Test that an error is thrown if an empty resource is downloaded."""
        with self.assertRaises(EmptyResourceError):
            get_bel_resource(TEST_NAMESPACE_EMPTY_PATH)

    def test_raises_on_missing(self):
        """Test that an error is thrown if a non-existent resource is specified."""
        # TODO

    def test_raises_on_invalid(self):
        """Test that an error is thrown if the resource is malformed."""
        # TODO

    def _help_test_annotation(self, res):
        expected_values = {
            'TestAnnot1': 'O',
            'TestAnnot2': 'O',
            'TestAnnot3': 'O',
            'TestAnnot4': 'O',
            'TestAnnot5': 'O'
        }

        self.assertEqual(expected_values, res['Values'])

    def test_get_from_path(self):
        """Test downloading a resource from a file path."""
        res = get_bel_resource(TEST_ANNOTATION_PATH)
        self._help_test_annotation(res)

    def test_get_from_url(self):
        """Test downloading a resource by URL."""
        with mock_bel_resources:
            res = get_bel_resource('https://example.com/test_an_1.belanno')
        self._help_test_annotation(res)


class TestSplitLines(unittest.TestCase):
    """Test splitting file into annotations and definitions."""

    def test_parts(self):
        """Test splitting file into annotations and definitions."""
        lines = simple.splitlines()
        docs, definitions, statements = split_file_to_annotations_and_definitions(lines)
        self.assertEqual(8, len(list(docs)))
        self.assertEqual(4, len(list(definitions)))
        self.assertEqual(14, len(list(statements)))


class TestSanitizeLines(unittest.TestCase):
    """Tests for :py:func:`sanitize_file_lines`."""

    def test_count(self):
        """Test that the right number of lines are retrieved."""
        lines = simple.splitlines()
        lines = list(sanitize_file_lines(lines))
        self.assertEqual(26, len(lines))

    def _help_test_line(self, statement: str, expect: str) -> None:
        lines = list(sanitize_file_lines(statement.split('\n')))
        self.assertEqual(1, len(lines))
        line = lines[0][1]
        self.assertEqual(expect, line)

    def test_already_correct(self):
        """Test when the line is already correct."""
        expect = statement = '''SET Evidence = "1.1.1 Easy case"'''
        self._help_test_line(statement, expect)

    def test_line_break_operator_no_whitespace(self):
        """Test when a backward slash break is use without whitespace."""
        statement = '''SET Evidence = "3.1 Backward slash break test \\
second line"'''
        expect = '''SET Evidence = "3.1 Backward slash break test second line"'''
        self._help_test_line(statement, expect)

    def test_line_break_operator_with_whitespace(self):
        """Test when a backward slash break is use with whitespace."""
        statement = '''SET Evidence = "3.2 Backward slash break test with whitespace \\
second line"'''
        expect = '''SET Evidence = "3.2 Backward slash break test with whitespace second line"'''
        self._help_test_line(statement, expect)

    def test_line_break_operator_multiple(self):
        """Test when multiple backward slash break are used."""
        statement = '''SET Evidence = "3.3 Backward slash break test \\
second line \\
third line"'''
        expect = '''SET Evidence = "3.3 Backward slash break test second line third line"'''
        self._help_test_line(statement, expect)

    def test_missing_line_break(self):
        """Test when a backward slash break is omitted in a new line."""
        statement = '''SET Evidence = "4.1 Malformed line breakcase
second line"'''
        expect = '''SET Evidence = "4.1 Malformed line breakcase second line"'''
        self._help_test_line(statement, expect)

    def test_missing_line_break_2(self):
        """Test a real example."""
        statement = '''SET Evidence = "The phosphorylation of S6K at Thr389, which is the TORC1-mediated site, was not
inhibited in the SIN1-/- cells (Figure 5A)."'''
        expect = (
            'SET Evidence = "The phosphorylation of S6K at Thr389, which is the TORC1-mediated site, was not '
            'inhibited in the SIN1-/- cells (Figure 5A)."'
        )
        self._help_test_line(statement, expect)

    def test_multiple_missing_line_breaks(self):
        """Test when a backward slash break is omitted in multiple new lines."""
        statement = '''SET Evidence = "4.2 Malformed line breakcase
second line
third line"'''
        expect = '''SET Evidence = "4.2 Malformed line breakcase second line third line"'''
        self._help_test_line(statement, expect)

    def test_multiple_missing_line_breaks_2(self):
        """Test forgotten delimiters."""
        s = [
            'SET Evidence = "Something',
            'or other',
            'or other"'
        ]

        result = list(sanitize_file_lines(s))
        expect = [(1, 'SET Evidence = "Something or other or other"')]

        self.assertEqual(expect, result)

    def test_line_numbers(self):
        """Test the line number follow-through."""
        statements = [
            '# Set document-defined annotation values\n',
            'SET Species = 9606',
            'SET Tissue = "t-cells"',
            '# Create an Evidence Line for a block of BEL Statements',
            'SET Evidence = "Here we show that interfereon-alpha (IFNalpha) is a potent producer \\',
            'of SOCS expression in human T cells, as high expression of CIS, SOCS-1, SOCS-2, \\',
            'and SOCS-3 was detectable after IFNalpha stimulation. After 4 h of stimulation \\',
            'CIS, SOCS-1, and SOCS-3 had ret'
        ]

        result = list(sanitize_file_lines(statements))

        expect = [
            (2, 'SET Species = 9606'),
            (3, 'SET Tissue = "t-cells"'),
            (5,
             'SET Evidence = "Here we show that interfereon-alpha (IFNalpha) is a potent producer of SOCS expression '
             'in human T cells, as high expression of CIS, SOCS-1, SOCS-2, and SOCS-3 was detectable after IFNalpha '
             'stimulation. After 4 h of stimulation CIS, SOCS-1, and SOCS-3 had ret')
        ]

        self.assertEqual(expect, result)

    def test_sanitize_comment(self):
        """Test that comments are sanitized."""
        s = [
            'SET Evidence = "yada yada yada" //this is a comment'
        ]

        result = list(sanitize_file_lines(s))
        expect = [(1, 'SET Evidence = "yada yada yada"')]

        self.assertEqual(expect, result)
