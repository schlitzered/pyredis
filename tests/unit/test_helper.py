__author__ = 'schlitzer'

from collections import deque
from unittest import TestCase
from unittest.mock import Mock, call, patch
from uuid import uuid4
import threading

from pyredis.exceptions import PyRedisError
from pyredis.helper import dict_from_list, tag_from_key, slot_from_key, ClusterMap


class TestHelperUnit(TestCase):
    def test_dict_from_list(self):
        source = ['test1', 1234, 'test2', 5678]
        expected = {
            'test1': 1234,
            'test2': 5678
        }
        result = dict_from_list(source)
        self.assertEqual(result, expected)

    def test_tag_from_key_no_tag(self):
        key = 'testkey'
        result = tag_from_key(key)
        self.assertEqual(key.encode(), result)
        pass

    def test_tag_from_key_1lcb_1rcb(self):
        key = 'blarg{testtag}sdfsdf'
        tag = b'testtag'
        result = tag_from_key(key)
        self.assertEqual(tag, result)

    def test_tag_from_key_1lcb_0rcb(self):
        key = '{asdas'
        result = tag_from_key(key)
        self.assertEqual(key.encode(), result)

    def test_tag_from_key_0lcb_1rcb(self):
        key = 'sadasd}a'
        result = tag_from_key(key)
        self.assertEqual(key.encode(), result)

    def test_tag_from_key_2lcb_2rcb(self):
        key = 'blarg{{testtag}sd}fsdf'
        tag = b'{testtag'
        result = tag_from_key(key)
        self.assertEqual(tag, result)

    def test_slot_from_key(self):
        key = 'blarg'.encode()
        result = slot_from_key(key)
        self.assertEqual(5534, result)


class TestClusterMap(TestCase):
    def setUp(self):
        self.addCleanup(patch.stopall)

        connection_patcher = patch('pyredis.helper.Connection', autospec=True)
        self.connection_mock = connection_patcher.start()

        self.seeds = [('host1', 12345), ('host2', 12345), ('host3', 12345)]
        self.map = [
            [
                0,
                5460,
                ['127.0.0.1', 7000],
                ['127.0.0.1', 7003]
            ],
            [
                5461,
                10922,
                ['127.0.0.1', 7001],
                ['127.0.0.1', 7004]
            ],
            [
                10923,
                16383,
                ['127.0.0.1', 7002],
                ['127.0.0.1', 7005]
            ]
        ]
        self.minimap = [
            [
                0,
                2,
                ['127.0.0.1', 7000],
                ['127.0.0.1', 7003]
            ],
            [
                3,
                3,
                ['127.0.0.1', 7001],
                ['127.0.0.1', 7004]
            ],
            [
                4,
                5,
                ['127.0.0.1', 7002],
                ['127.0.0.1', 7005]
            ]
        ]

    def test___init__(self):
        clustermap = ClusterMap(self.seeds)
        self.assertEqual(clustermap._map, {})
        self.assertEqual(clustermap._seeds, deque(self.seeds))

    def test__make_str(self):
        result = ClusterMap._make_str(['127.0.0.1', 7002])
        self.assertEqual(result, '127.0.0.1_7002')

    def test__fetch_map_first_try_ok(self):
        conn1 = Mock()
        conn1.read.return_value = self.map

        self.connection_mock.return_value = conn1

        clustermap = ClusterMap(self.seeds)

        result = clustermap._fetch_map()

        self.assertEqual(result, self.map)
        conn1.write.assert_called_with('CLUSTER', 'SLOTS')
        self.assertTrue(conn1.close.called)

    def test__fetch_map_second_try_ok(self):
        conn1 = Mock()
        conn1.read.side_effect = PyRedisError
        conn2 = Mock()
        conn2.read.return_value = self.map

        self.connection_mock.side_effect = [conn1, conn2]

        clustermap = ClusterMap(self.seeds)

        result = clustermap._fetch_map()

        self.assertEqual(result, self.map)
        conn1.write.assert_called_with('CLUSTER', 'SLOTS')
        self.assertTrue(conn1.close.called)
        conn2.write.assert_called_with('CLUSTER', 'SLOTS')
        self.assertTrue(conn2.close.called)

    def test__fetch_map_exception(self):
        conn1 = Mock()
        conn1.read.side_effect = PyRedisError
        conn2 = Mock()
        conn2.read.side_effect = PyRedisError
        conn3 = Mock()
        conn3.read.side_effect = PyRedisError

        self.connection_mock.side_effect = [conn1, conn2, conn3]

        clustermap = ClusterMap(self.seeds)


        self.assertRaises(PyRedisError, clustermap._fetch_map)

        self.connection_mock.assert_has_calls([
            call(host='host1', port=12345, encoding='utf-8'),
            call(host='host2', port=12345, encoding='utf-8'),
            call(host='host3', port=12345, encoding='utf-8')
        ])

        conn1.write.assert_called_with('CLUSTER', 'SLOTS')
        self.assertTrue(conn1.close.called)
        conn2.write.assert_called_with('CLUSTER', 'SLOTS')
        self.assertTrue(conn2.close.called)
        conn3.write.assert_called_with('CLUSTER', 'SLOTS')
        self.assertTrue(conn3.close.called)

    def test_update(self):
        clustermap = ClusterMap(self.seeds)
        update = Mock()
        id = clustermap.id
        clustermap._update_slot = update
        clustermap._fetch_map = Mock()
        clustermap._fetch_map.return_value = self.minimap
        id_new = clustermap.update(clustermap.id)
        clustermap._update_slot.assert_has_calls(
            [
                call(0, ['127.0.0.1', 7000], [['127.0.0.1', 7003]]),
                call(1, ['127.0.0.1', 7000], [['127.0.0.1', 7003]]),
                call(2, ['127.0.0.1', 7000], [['127.0.0.1', 7003]]),
                call(3, ['127.0.0.1', 7001], [['127.0.0.1', 7004]]),
                call(4, ['127.0.0.1', 7002], [['127.0.0.1', 7005]]),
                call(5, ['127.0.0.1', 7002], [['127.0.0.1', 7005]])
            ]
        )
        self.assertNotEqual(clustermap.id, id)
        self.assertEqual(clustermap.id, id_new)

    def test_update_slot(self):
        clustermap = ClusterMap(self.seeds)
        clustermap._update_slot(0, ['127.0.0.1', 7000], [['127.0.0.1', 7003]])
        self.assertEqual(
            clustermap._map[0],
            {'master': '127.0.0.1_7000', 'slave': '127.0.0.1_7003'}
        )

    def test_get_slot_master(self):
        clustermap = ClusterMap(self.seeds)
        clustermap._fetch_map = Mock()
        clustermap._fetch_map.return_value = self.map
        clustermap.update(clustermap.id)
        result = clustermap.get_slot('blarg')
        self.assertEqual(result, '127.0.0.1_7001')

    def test_get_slot_slaves(self):
        clustermap = ClusterMap(self.seeds)
        clustermap._fetch_map = Mock()
        clustermap._fetch_map.return_value = self.map
        clustermap.update(clustermap.id)
        result = clustermap.get_slot('blarg')
        self.assertEqual(result, '127.0.0.1_7001')

    def test_hosts_master(self):
        clustermap = ClusterMap(self.seeds)
        clustermap._fetch_map = Mock()
        clustermap._fetch_map.return_value = self.minimap
        clustermap.update(clustermap.id)
        self.assertEqual(
            ({'127.0.0.1_7000', '127.0.0.1_7001', '127.0.0.1_7002'}),
            clustermap.hosts())

    def test_hosts_slaves(self):
        clustermap = ClusterMap(self.seeds)
        clustermap._fetch_map = Mock()
        clustermap._fetch_map.return_value = self.minimap
        clustermap.update(clustermap.id)
        self.assertEqual(
            ({'127.0.0.1_7003', '127.0.0.1_7004', '127.0.0.1_7005'}),
            clustermap.hosts(slave=True))
