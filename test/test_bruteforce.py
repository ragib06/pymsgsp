__author__ = 'ragib'

import unittest
import os
import sys
import inspect
import logging

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from BruteForce import BruteForceSPM
from MSGSP import pyMSGSP
from RandomDataGenerator import RandomDataGenerator
from Utils import Utils


# python -m unittest -v test_bruteforce.TestBruteForce.test_sample


class TestBruteForce(unittest.TestCase):
    def setUp(self):
        # self.inputData = {'T': [[[1]], [[2]], [[2]], [[1], [1, 2]]], 'MS': {1: 0.09600845652974467, 2: 0.2357830588199925}, 'SDC': 0.056047812216985904}
        # self.inputData = {'T': [[[1, 2], [2]], [[2, 3], [1], [2, 3]], [[2, 3]], [[1, 3]], [[1, 3], [1, 2, 3], [2, 3]]], 'MS': {1: 0.25702407161838653, 2: 0.08575639786409932, 3: 0.17145036805581798}, 'SDC': 0.07057225398948441}
        # self.inputData = {'T': [[[2], [1, 2], [2, 3]], [[1]], [[2], [1], [1, 3]], [[1, 2, 3]], [[2], [2], [1, 2, 3]], [[1, 3], [2, 3]], [[2], [2, 3], [1]], [[1, 2, 3], [3], [1, 3]], [[3], [1]], [[3], [2], [2]]], 'MS': {1: 0.060929914031876184, 2: 0.26660420634518706, 3: 0.16460662595201303}, 'SDC': 0.15822490055135152}
        self.inputData = {'T': [[[1, 3], [2]], [[1, 2], [3]], [[1, 3], [2]], [[1, 2], [1, 2, 3], [1, 3]], [[1, 3]], [[2, 3]], [[1, 2], [2]], [[1, 2, 3]], [[1, 2], [1, 3], [2, 3]], [[2, 3], [2, 3], [1, 2]]], 'MS': {1: 0.09044942217630313, 2: 0.29971392690105775, 3: 0.16224978413819546}, 'SDC': 0.15900593576294117}

    def tearDown(self):
        pass

    def comparator(self, a, b):
        if len(a) < len(b):
            return -1
        elif len(a) > len(b):
            return 1
        else:
            if Utils.seqLength(a) == Utils.seqLength(b):
                return a[0][0] - b[0][0]
            else:
                return Utils.seqLength(a) - Utils.seqLength(b)

    def test_sample(self):
        algo1 = pyMSGSP(self.inputData["T"], self.inputData["MS"], self.inputData["SDC"], logging.ERROR)
        algo2 = BruteForceSPM(self.inputData["T"], self.inputData["MS"], self.inputData["SDC"])

        output1 = algo1.run()
        output2 = algo2.run()

        for s in output1:
            for it in s:
                it.sort()

        for s in output2:
            for it in s:
                it.sort()

        for t in output1:
            self.assertTrue(t in output2)

    def test_random(self):

        RDG = RandomDataGenerator()

        for i in range(10):
            randomData = RDG.genData()
            print 'randomData', i+1, ':', randomData

            algo1 = BruteForceSPM(randomData["T"], randomData["MS"], randomData["SDC"])
            algo2 = pyMSGSP(randomData["T"], randomData["MS"], randomData["SDC"], logging.ERROR)

            output1 = algo1.run()
            output2 = algo2.run()

            for s in output1:
                for it in s:
                    it.sort()

            for s in output2:
                for it in s:
                    it.sort()

            for t in output1:
                self.assertTrue(t in output2)

