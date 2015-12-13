from collections import defaultdict
import sys
import copy
import logging
from datetime import datetime


from DataProcessor import DataProcessor
from BruteForce import BruteForceSPM
from Utils import Utils


class MSCandidateJoinCriteria:
    FORWARD = 1
    REVERSE = 2
    APRIORI = 3


class pyMSGSP:
    """ MS-GSP alogorithm """

    T = []
    MS = []
    SDC = 1.0

    def __init__(self, t, ms, sdc, logLevel=logging.WARNING):
        self.T = t
        self.MS = ms
        self.SDC = sdc
        logging.basicConfig(stream=sys.stderr, level=logLevel)

    def run(self):
        M = Utils.getUniqueItems(self.T)
        M.sort(key=lambda item: self.MS[item])
        logging.info('M: %s', M)

        SUP = Utils.genItemSupportCount(M, self.T)
        logging.info('SUP: %s', SUP)

        L = [(M[m], SUP[m]) for m in range(len(M))]
        logging.info('L: %s', L)

        F1 = [l for l in L if float(l[1])/len(self.T) >= self.MS[l[0]]]
        F = [ [[f[0]]] for f in F1 ]

        logging.info('F1: %s length: %s', F1, len(F1))

        k = 2
        Fk, Ck = F1, []

        while(Fk):
            logging.warning('candidate level: %d', k)
            if k == 2:
                Ck = self.level2CandidateGenSPM(L)
                logging.warning('C2 length: %s', len(Ck))
                logging.info('C2: %s length: %s', Ck, len(Ck))

            else:
                Ck = self.MSCandidateGenSPM(Fk)
                logging.warning('C%d length: %s', k, len(Ck))
                logging.info('C%d: %s length: %s', k, Ck, len(Ck))

            cSUP = Utils.genSupportCount(Ck, self.T)
            logging.debug('cSUP: %s', cSUP)
            Fk = [Ck[c] for c in range(len(Ck)) if float(cSUP[c])/len(self.T) >= self.getMinMIS(Ck[c])]
            F.extend(Fk)

            logging.info('F%d: %s', k, Fk)
            logging.warning('F%d length: %s', k, len(Fk))

            k += 1

        logging.info('F: %s', F)
        return F

    def getMinMIS(self, seq):
        minMIS = sys.maxint
        for itemset in seq:
            for item in itemset:
                if self.MS[item] < minMIS:
                    minMIS = self.MS[item]

        return minMIS

    def getStrictlyMinimumMIS(self, seq):
        minMIS = sys.maxint
        strict = True
        for itemset in seq:
            for item in itemset:
                if self.MS[item] < minMIS:
                    minMIS = self.MS[item]
                    strict = True
                elif minMIS == self.MS[item]:
                    strict = False
        if strict:
            return minMIS
        else:
            return sys.maxint

    def extendSequence(self, s1, s2, criteria):
        newCandidates = []

        if criteria == MSCandidateJoinCriteria.FORWARD:
            if len(s2[-1]) == 1:
                s1copy = copy.deepcopy(s1)
                s1copy.append(s2[-1])
                newCandidates.append(s1copy)

                if Utils.seqLength(s1) == 2 and len(s1) == 2 and s2[-1][-1] > s1[-1][-1]:
                    s1copy1 = copy.deepcopy(s1)
                    s1copy1[-1].append(s2[-1][-1])
                    newCandidates.append(s1copy1)

            elif (Utils.seqLength(s1) == 2 and len(s1) == 1 and s2[-1][-1] > s1[-1][-1]) or Utils.seqLength(s1) > 2:
                s1copy = copy.deepcopy(s1)
                s1copy[-1].append(s2[-1][-1])
                newCandidates.append(s1copy)
        elif criteria == MSCandidateJoinCriteria.REVERSE:
            if len(s1[0]) == 1:
                s2copy = copy.deepcopy(s2)
                s2copy.insert(0, s1[0])
                newCandidates.append(s2copy)

                if Utils.seqLength(s2) == 2 and len(s2) == 2 and s1[0][0] > s2[0][0]:
                    s2copy1 = copy.deepcopy(s2)
                    s2copy1[0].insert(0, s1[0][0])
                    newCandidates.append(s2copy1)

            elif (Utils.seqLength(s2) == 2 and len(s2) == 1 and s1[0][0] > s2[0][0]) or Utils.seqLength(s2) > 2:
                s2copy1 = copy.deepcopy(s2)
                s2copy1[0].insert(0, s1[0][0])
                newCandidates.append(s2copy1)
        elif criteria == MSCandidateJoinCriteria.APRIORI:
            if len(s2[-1]) == 1:
                s1copy = copy.deepcopy(s1)
                s1copy.append(s2[-1])
                newCandidates.append(s1copy)
            else:
                s1copy = copy.deepcopy(s1)
                s1copy[-1].append(s2[-1][-1])
                newCandidates.append(s1copy)

        return newCandidates

    def canPrune(self, seq):
        sLowestMIS = self.getStrictlyMinimumMIS(seq)
        k = Utils.seqLength(seq)

        for i in range(k):
            item = Utils.getItem(seq, i)

            if self.MS[item] == sLowestMIS:
                continue

            k_1_subseq = Utils.removeItem(seq, i)

            count = 0
            for d in self.T:
                if Utils.isSubsequence(k_1_subseq, d):
                    count += 1

            if float(count) / len(self.T) < self.getMinMIS(k_1_subseq):
                return True

        return False

    def level2CandidateGenSPM(self, L):
        C2 = []
        for l in range(len(L)):
            supl = float(L[l][1]) / len(self.T)
            if supl >= self.MS[L[l][0]]:
                h = l
                while h < len(L):
                    suph = float(L[h][1]) / len(self.T)
                    if suph >= self.MS[L[l][0]] and abs(supl - suph) <= self.SDC:
                        if L[l][0] < L[h][0]:
                            C2.append([[L[l][0], L[h][0]]])
                        else:
                            C2.append([[L[h][0], L[l][0]]])

                        C2.append([[L[l][0]], [L[h][0]]])

                        if L[l][0] != L[h][0]:
                            C2.append([[L[h][0]], [L[l][0]]])

                    h += 1

        return C2

    def MSCandidateGenSPM(self, F):
        logging.debug('MSCandidateGenSPM: %s', F)

        cs = []
        for s1 in F:
            for s2 in F:
                if self.MS[s1[0][0]] == self.getStrictlyMinimumMIS(s1):
                    if (Utils.removeItem(s1, 1) == Utils.removeItem(s2, Utils.seqLength(s2)-1)) and (self.MS[s2[-1][-1]] >= self.MS[s1[0][0]]): #TODO: need to check why >= here?
                        nc = self.extendSequence(s1, s2, MSCandidateJoinCriteria.FORWARD)
                        for c in nc:
                            cs.append(c)
                            logging.debug('join: %s %s -> %s %d', s1, s2, c, MSCandidateJoinCriteria.FORWARD)
                elif self.MS[s2[-1][-1]] == self.getStrictlyMinimumMIS(s2):
                    if (Utils.removeItem(s2, Utils.seqLength(s2)-2) == Utils.removeItem(s1, 0)) and (self.MS[s1[0][0]] > self.MS[s2[-1][-1]]):
                        nc = self.extendSequence(s1, s2, MSCandidateJoinCriteria.REVERSE)
                        for c in nc:
                            cs.append(c)
                            logging.debug('join: %s %s -> %s %d', s1, s2, c, MSCandidateJoinCriteria.REVERSE)
                else:
                    if Utils.removeItem(s1, 0) == Utils.removeItem(s2, Utils.seqLength(s2)-1):
                        nc = self.extendSequence(s1, s2, MSCandidateJoinCriteria.APRIORI)
                        for c in nc:
                            cs.append(c)
                            logging.debug('join: %s %s -> %s %d', s1, s2, c, MSCandidateJoinCriteria.APRIORI)

        return [c for c in cs if self.canPrune(c) is False]

if __name__ == "__main__":

    data_file = "data/dataS.txt"
    para_file = "data/paraS.txt"
    result_file = "data/resultS.txt"

    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            if len(sys.argv) < 4:
                logging.error("Not enough arguments !!")
                sys.exit()
            else:
                data_file = sys.argv[2]
                para_file = sys.argv[3]
                result_file = sys.argv[4]


    DP = DataProcessor(data_file, para_file, result_file, False)
    inputData = DP.loadInput()

    startTime = datetime.now()
    print 'Execution started at:', startTime
    algo = pyMSGSP(inputData["T"], inputData["MS"], inputData["SDC"], logging.INFO)
    # algo = BruteForceSPM(inputData["T"], inputData["MS"], inputData["SDC"])

    outputData = algo.run()
    print 'Execution time:', datetime.now() - startTime

    outputDict = defaultdict(list)

    for seq in outputData:
        count = 0
        for d in inputData["T"]:
            if Utils.isSubsequence(seq, d):
                count += 1
        outputDict[Utils.seqLength(seq)].append((seq, count))

    DP.printOutput(outputDict)




