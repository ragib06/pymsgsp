import copy
import itertools

class Utils:
    """ Utility Methods for MS-GSP """

    @staticmethod
    def getUniqueItems(data):
        uItems = {}

        for row in data:
            for l in row:
                for item in l:
                    if uItems.has_key(item):
                        pass
                    else:
                        uItems[item] = True

        items = sorted(uItems.keys())

        return items

    @staticmethod
    def isSubset(sub, sup):
        # TODO: check why is this happening?
        if len(list(set(sub))) != len(sub):
            return False

        for i in sub:
            if i not in sup:
                return False

        return True

    @staticmethod
    def isSubsequence(sub, sup):
        mark = {}

        next = 0
        for i in sub:
            found = False
            j = next
            while j < len(sup):
                if mark.has_key(j):
                    pass
                else:
                    if Utils.isSubset(i, sup[j]):
                        mark[j] = True
                        found = True
                        next = j+1
                        break
                j += 1
            if not found:
                return False

        return True

    @staticmethod
    def genItemSupportCount(items, data):
        seqOfItems = [[[i]] for i in items]
        return Utils.genSupportCount(seqOfItems, data)

    @staticmethod
    def genSupportCount(Ck, data):

        sup = [0] * len(Ck)

        for s in range(len(Ck)):
            count = 0
            for d in data:
                if Utils.isSubsequence(Ck[s], d):
                    count += 1
            sup[s] = count

        return sup

    @staticmethod
    def seqLength(seq):
        length = 0

        for e in seq:
            length += len(e)

        return length

    @staticmethod
    def removeItem(seq, index):

        seqcopy = copy.deepcopy(seq)

        length = Utils.seqLength(seqcopy)
        if index < 0 or index >= length:
            return []

        count = 0
        for itemset in seqcopy:
            if count + len(itemset) <= index:
                count += len(itemset)
            else:
                del itemset[index - count]
                break

        return [itemset for itemset in seqcopy if len(itemset) > 0]

    @staticmethod
    def getItem(seq, index):
        length = Utils.seqLength(seq)

        if index < 0 or index >= length:
            return None

        count = 0
        for itemset in seq:
            if count + len(itemset) <= index:
                count += len(itemset)
            else:
                return itemset[index - count]

        return None

    @staticmethod
    def generateAllSubsets(L):
        subsets = []
        for i in range(1 << len(L)):
            s = []
            for j in range(len(L)):
                if i & 1 << j:
                    s.append(L[j])
            if s:
                subsets.append(s)

        return subsets


    @staticmethod
    def generateSequences(L, T, n, k, out):
        if k == n:
            out.append(T)
            return

        for i in L:
            tt = copy.deepcopy(T)
            tt.append(i)
            Utils.generateSequences(L, tt, n, k+1, out)


    @staticmethod
    def generateAllSequences(L):

        seqs = []
        for length in range(1, 6):
            Utils.generateSequences(L, [], length, 0, seqs)
            # print length, ':', seqs


        return seqs

        # subsets = []
        # for i in range(1 << len(L)):
        #     s = []
        #     for j in range(len(L)):
        #         if i & 1 << j:
        #             s.append(L[j])
        #     if s:
        #         perm = list(itertools.permutations(s))
        #         for p in perm:
        #             subsets.append(list(p))
        #
        # return subsets