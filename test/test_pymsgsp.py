__author__ = 'ragib'

import unittest
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from MSGSP import pyMSGSP
from MSGSP import MSCandidateJoinCriteria
from Utils import Utils

class TestPyMSGSP(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def comparator(self, a, b):
        if len(a) < len(b):
            return -1
        elif len(a) > len(b):
            return 1
        else:
            return Utils.seqLength(a) - Utils.seqLength(b)

    def test_getminmis(self):
        inputData = {'T': [[[1]], [[2]], [[2]], [[1], [1, 2]]], 'MS': {1: 0.09600845652974467, 2: 0.2357830588199925}, 'SDC': 0.056047812216985904}
        pymsgsp = pyMSGSP(inputData["T"], inputData["MS"], inputData["SDC"])

        self.assertEqual(pymsgsp.getMinMIS([]), sys.maxint)
        self.assertTrue(abs(pymsgsp.getMinMIS([[1]]) - 0.09600845652974467) <= 0.0001)
        self.assertTrue(abs(pymsgsp.getMinMIS([[1, 2]]) - 0.09600845652974467) <= 0.0001)
        self.assertTrue(abs(pymsgsp.getMinMIS([[1], [2]]) - 0.09600845652974467) <= 0.0001)
        self.assertTrue(abs(pymsgsp.getMinMIS([[1], [1]]) - 0.09600845652974467) <= 0.0001)

    def test_getstrictlyminimummis(self):
        inputData = {'T': [[[1]], [[2]], [[2]], [[1], [1, 2]]], 'MS': {1: 0.09600845652974467, 2: 0.2357830588199925}, 'SDC': 0.056047812216985904}
        pymsgsp = pyMSGSP(inputData["T"], inputData["MS"], inputData["SDC"])

        self.assertEqual(pymsgsp.getStrictlyMinimumMIS([]), sys.maxint)
        self.assertTrue(abs(pymsgsp.getStrictlyMinimumMIS([[1]]) - 0.09600845652974467) <= 0.0001)
        self.assertTrue(abs(pymsgsp.getStrictlyMinimumMIS([[1, 2]]) - 0.09600845652974467) <= 0.0001)
        self.assertTrue(abs(pymsgsp.getStrictlyMinimumMIS([[1], [2]]) - 0.09600845652974467) <= 0.0001)
        self.assertEqual(pymsgsp.getStrictlyMinimumMIS([[1], [1]]), sys.maxint)

    def test_extendsequence(self):
        inputData = {'T': [[[1]], [[2]], [[2]], [[1], [1, 2]]], 'MS': {1: 0.09600845652974467, 2: 0.2357830588199925}, 'SDC': 0.056047812216985904}
        pymsgsp = pyMSGSP(inputData["T"], inputData["MS"], inputData["SDC"])

        s1 = [[1]]
        s2 = [[2]]
        self.assertEqual(pymsgsp.extendSequence(s1, s2, MSCandidateJoinCriteria.FORWARD), [[[1], [2]]])

        s1 = [[1], [2]]
        s2 = [[2], [2]]
        self.assertEqual(pymsgsp.extendSequence(s1, s2, MSCandidateJoinCriteria.FORWARD), [[[1], [2], [2]]])

    def test_canprune(self):
        inputData = {'T': [[[1]], [[2]], [[2]], [[1], [1, 2]]], 'MS': {1: 0.09600845652974467, 2: 0.2357830588199925}, 'SDC': 0.056047812216985904}
        pymsgsp = pyMSGSP(inputData["T"], inputData["MS"], inputData["SDC"])

        s = [[1], [1]]
        self.assertFalse(pymsgsp.canPrune(s))

    def test_level2candidategenspm(self):
        inputData = {'T': [[[1]], [[2], [2]], [[1], [1, 2]]], 'MS': {1: 0.09600845652974467, 2: 0.2357830588199925}, 'SDC': 0.056047812216985904}
        pymsgsp = pyMSGSP(inputData["T"], inputData["MS"], inputData["SDC"])

        M = Utils.getUniqueItems(inputData["T"])
        M.sort(key=lambda item: inputData["MS"][item])
        SUP = Utils.genItemSupportCount(M, inputData["T"])
        L = [(M[m], SUP[m]) for m in range(len(M))]

        out1 = pymsgsp.level2CandidateGenSPM(L)
        out2 = [[[1, 1]], [[1], [1]], [[1, 2]], [[1], [2]], [[2], [1]], [[2, 2]], [[2], [2]]]

        out1 = sorted(out1, cmp=self.comparator)
        out2 = sorted(out2, cmp=self.comparator)

        self.assertEqual(out1, out2)

    def test_mscandidategenspm(self):

        inputData = {'T': [[[1]], [[2], [2]], [[1], [1, 2]]], 'MS': {1: 0.09600845652974467, 2: 0.2357830588199925}, 'SDC': 0.056047812216985904}
        pymsgsp = pyMSGSP(inputData["T"], inputData["MS"], inputData["SDC"])

        T = inputData["T"]
        M = Utils.getUniqueItems(T)
        M.sort(key=lambda item: inputData["MS"][item])
        SUP = Utils.genItemSupportCount(M, T)
        L = [(M[m], SUP[m]) for m in range(len(M))]

        C2 = pymsgsp.level2CandidateGenSPM(L)
        cSUP = Utils.genSupportCount(C2, T)
        F2 = [C2[c] for c in range(len(C2)) if float(cSUP[c])/len(T) >= pymsgsp.getMinMIS(C2[c])]

        out1 = pymsgsp.MSCandidateGenSPM(F2)
        out2 = [[[1], [1], [1]], [[1], [1, 2]], [[1], [1], [2]], [[1, 2], [2]], [[1], [2], [2]], [[2], [2], [2]]]

        out1 = sorted(out1, cmp=self.comparator)
        out2 = sorted(out2, cmp=self.comparator)

        self.assertEqual(out1, out2)



