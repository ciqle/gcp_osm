import unittest
from unittest.mock import MagicMock
from datetime import datetime

# Assuming the utility functions are imported
from osmium.pbf_parser import osm_entity_to_dict, osm_entity_to_dict_full, osm_entity_node_dict, osm_entity_way_dict, \
    osm_entity_relation_dict


class TestUtilityFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_osm_entity = MagicMock()
        self.mock_osm_entity.id = 1
        self.mock_osm_entity.tags = [MagicMock(k='highway', v='residential')]
        self.mock_osm_entity.version = 2
        self.mock_osm_entity.user = 'test_user'
        self.mock_osm_entity.changeset = 12345
        self.mock_osm_entity.visible = True
        self.mock_osm_entity.timestamp = datetime(2024, 1, 1)

    def test_osm_entity_to_dict(self):
        result = osm_entity_to_dict(self.mock_osm_entity)
        expected = {
            'id': 1,
            'all_tags': [{'key': 'highway', 'value': 'residential'}]
        }
        self.assertEqual(result, expected)

    def test_osm_entity_to_dict_full(self):
        result = osm_entity_to_dict_full(self.mock_osm_entity)
        expected = {
            'id': 1,
            'all_tags': [{'key': 'highway', 'value': 'residential'}],
            'version': 2,
            'username': 'test_user',
            'changeset': 12345,
            'visible': True,
            'osm_timestamp': int(datetime.timestamp(datetime(2024, 1, 1))),
        }
        self.assertEqual(result, expected)

    def test_osm_entity_node_dict(self):
        self.mock_osm_entity.location.valid.return_value = True
        self.mock_osm_entity.location.lat = 51.5074
        self.mock_osm_entity.location.lon = -0.1278
        result = osm_entity_node_dict(self.mock_osm_entity)
        expected = {
            'id': 1,
            'all_tags': [{'key': 'highway', 'value': 'residential'}],
            'version': 2,
            'username': 'test_user',
            'changeset': 12345,
            'visible': True,
            'osm_timestamp': int(datetime.timestamp(datetime(2024, 1, 1))),
            'latitude': 51.5074,
            'longitude': -0.1278,
        }
        self.assertEqual(result, expected)

    def test_osm_entity_way_dict(self):
        self.mock_osm_entity.nodes = [MagicMock(ref=1), MagicMock(ref=2)]
        result = osm_entity_to_dict_full(self.mock_osm_entity)
        result.update({'nodes': [{'id': 1}, {'id': 2}]})
        expected = {
            'id': 1,
            'all_tags': [{'key': 'highway', 'value': 'residential'}],
            'version': 2,
            'username': 'test_user',
            'changeset': 12345,
            'visible': True,
            'osm_timestamp': int(datetime.timestamp(datetime(2024, 1, 1))),
            'nodes': [{'id': 1}, {'id': 2}]
        }
        self.assertEqual(result, expected)

    def test_osm_entity_relation_dict(self):
        self.mock_osm_entity.members = [MagicMock(type='node', ref=1, role=''),
                                        MagicMock(type='way', ref=2, role='outer')]
        result = osm_entity_relation_dict(self.mock_osm_entity)
        expected = {
            'id': 1,
            'all_tags': [{'key': 'highway', 'value': 'residential'}],
            'version': 2,
            'username': 'test_user',
            'changeset': 12345,
            'visible': True,
            'osm_timestamp': int(datetime.timestamp(datetime(2024, 1, 1))),
            'members': [{'type': 'node', 'id': 1, 'role': ''}, {'type': 'way', 'id': 2, 'role': 'outer'}]
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
