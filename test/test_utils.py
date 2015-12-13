__author__ = 'ragib'

import unittest
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Utils import Utils

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getuniqueitems(self):
        data = []
        self.assertEqual(Utils.getUniqueItems(data), [])

        data = [[[1]]]
        self.assertEqual(Utils.getUniqueItems(data), [1])

        data = [[[1]], [[2], [2]], [[1], [1, 2]]]
        self.assertEqual(Utils.getUniqueItems(data), [1, 2])

        data = [[[1], [2, 3]], [[4, 5, 6], [7]]]
        self.assertEqual(Utils.getUniqueItems(data), [1, 2, 3, 4, 5, 6, 7])

        data = [[[1, 2, 3]]]
        self.assertEqual(Utils.getUniqueItems(data), [1, 2, 3])

    def test_issubset(self):
        sub = []
        sup = []
        self.assertTrue(Utils.isSubset(sub, sup))

        sub = []
        sup = [1]
        self.assertTrue(Utils.isSubset(sub, sup))

        sub = [1]
        sup = []
        self.assertFalse(Utils.isSubset(sub, sup))

        sub = [1]
        sup = [1]
        self.assertTrue(Utils.isSubset(sub, sup))

        sub = [1]
        sup = [2]
        self.assertFalse(Utils.isSubset(sub, sup))

    def test_issubsequence(self):
        sub = []
        sup = []
        self.assertTrue(Utils.isSubsequence(sub, sup))

        sub = []
        sup = [[1], [2]]
        self.assertTrue(Utils.isSubsequence(sub, sup))

        sub = [[2], [3]]
        sup = [[1, 2, 3], [1, 2, 3, 4]]
        self.assertTrue(Utils.isSubsequence(sub, sup))

        sub = [[1, 3], [3, 3, 3]]
        sup = [[1, 2, 3], [1, 2, 3, 4]]
        self.assertFalse(Utils.isSubsequence(sub, sup))

    def test_genitemsupportcount(self):
        data = []
        items = []
        self.assertEqual(Utils.genItemSupportCount(items, data), [])

        data = [[[1]]]
        items = [1]
        self.assertEqual(Utils.genItemSupportCount(items, data), [1])

        data = [[[1]], [[2], [2]], [[1], [1, 2]]]
        items = [1, 2]
        self.assertEqual(Utils.genItemSupportCount(items, data), [2, 2])

        data = [[[1], [2, 3]], [[4, 5, 6], [7]]]
        items = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(Utils.genItemSupportCount(items, data), [1, 1, 1, 1, 1, 1, 1])

        data = [[[1, 2, 3]]]
        items = [1, 2, 3]
        self.assertEqual(Utils.genItemSupportCount(items, data), [1, 1, 1])

    def test_gensupportcount(self):
        data = []
        candidates = []
        self.assertEqual(Utils.genSupportCount(candidates, data), [])

        data = [[[1]]]
        candidates = [[[1]]]
        self.assertEqual(Utils.genSupportCount(candidates, data), [1])

        data = [[[1]], [[2], [2]], [[1], [1, 2]]]
        candidates = [[[1]], [[2]], [[2], [2]], [[1], [2]], [[2], [1]]]
        self.assertEqual(Utils.genSupportCount(candidates, data), [2, 2, 1, 1, 0])

    def test_seqlength(self):
        s = []
        self.assertEqual(Utils.seqLength(s), 0)

        s = [[1]]
        self.assertEqual(Utils.seqLength(s), 1)

        s = [[2, 3]]
        self.assertEqual(Utils.seqLength(s), 2)

        s = [[1], [2, 3]]
        self.assertEqual(Utils.seqLength(s), 3)

        s = [[1], [2, 3], [4]]
        self.assertEqual(Utils.seqLength(s), 4)

        s = [[1], [1, 1], [1]]
        self.assertEqual(Utils.seqLength(s), 4)

    def test_removeitem(self):
        s = []
        ts = s
        self.assertEqual(Utils.removeItem(s, 0), [])
        self.assertEqual(s, ts)

        s = [[30, 70, 80]]
        ts = s
        self.assertEqual(Utils.removeItem(s, 0), [[70, 80]])
        self.assertEqual(s, ts)

        s = [[70, 80], [90]]
        ts = s
        self.assertEqual(Utils.removeItem(s, Utils.seqLength(s)-1), [[70, 80]])
        self.assertEqual(s, ts)

    def test_getitem(self):
        s = []
        self.assertEqual(Utils.getItem(s, 4), None)

        s = [[30, 70, 80]]
        self.assertEqual(Utils.getItem(s, 0), 30)

        s = [[70, 80], [90]]
        self.assertEqual(Utils.getItem(s, Utils.seqLength(s)-1), 90)

