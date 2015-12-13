__author__ = 'ragib'

from Utils import Utils


class BruteForceSPM:
    """ Brute Force Implementation for Sequential Pattern Mining """

    T = []
    MS = []
    SDC = 1.0
    DEBUG = False

    def __init__(self, t, ms, sdc, debug=False):
        self.T = t
        self.MS = ms
        self.SDC = sdc
        self.DEBUG = debug

    def run(self):

        L = Utils.getUniqueItems(self.T)
        SUP = Utils.genItemSupportCount(L, self.T)
        lSUP = {}
        for l in range(len(L)):
            lSUP[L[l]] = SUP[l]

        if len(L) > 3:
            print "SORRY! Can't run Brute Force with these large data"
            return []

        C = Utils.generateAllSubsets(L)
        S = Utils.generateAllSequences(C)

        outputData = []

        for seq in S:
            count = 0
            minSUP = 999
            maxSUP = 0
            minMIS = 999

            for s in range(len(seq)):
                for i in seq[s]:
                    if lSUP[i] < minSUP:
                        minSUP = lSUP[i]
                    if lSUP[i] > maxSUP:
                        maxSUP = lSUP[i]
                    if self.MS[i] < minMIS:
                        minMIS = self.MS[i]

            for d in self.T:
                if Utils.isSubsequence(seq, d):
                    count += 1

            if ((float(count) / len(self.T)) >= minMIS) and (float(maxSUP - minSUP) / len(self.T) <= self.SDC):
                outputData.append(seq)

        return outputData
