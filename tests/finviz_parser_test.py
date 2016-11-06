from unittest import TestCase

from parsers import FinvizKeyStatsParser


class TestFinvizKeyStatsParser(TestCase):

    def test_finviz_key_stats_parser_instance_and_props(self):
        parser = FinvizKeyStatsParser()
        self.assertEqual(len(parser.indicators), len(parser.key_names))
