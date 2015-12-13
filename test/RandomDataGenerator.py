import random

class RandomDataGenerator:
    """ Genrates Random Data for MS-GSP with given limits """

    maxUniqItems = 0
    maxTransactions = 10
    minMIS = 0.05
    maxMIS = 0.3
    minSDC = 0.005
    maxSDC = 0.2

    numItems = 0

    def __init__(self, max_items=3, max_transactions=10, mis_range=(0.05, 0.3), sdc_range=(0.005, 0.2)):
        self.maxUniqItems = max_items
        self.maxTransactions = max_transactions
        self.minMIS = mis_range[0]
        self.maxMIS = mis_range[1]
        self.minSDC = sdc_range[0]
        self.maxSDC = sdc_range[1]
        self.numItems = 0

    def genTransactions(self):

        # numT = random.randint(1, self.maxTransactions)
        # self.numItems = random.randint(1, self.maxUniqItems)
        self.numItems = self.maxUniqItems
        T = []

        for i in range(self.maxTransactions):
            nitemsets = random.randint(1, self.numItems > 3 and 10 or 3)
            itemsets = []
            for j in range(nitemsets):
                nitems = random.randint(1, self.numItems > 3 and 10 or 3)
                items = []
                for k in range(nitems):
                    items.append(random.randint(1, self.numItems))
                itemsets.append(list(set(items)))
            T.append(itemsets)

        return T

    def genMIS(self):
        MS = {}
        for i in range(self.numItems):
            MS[i+1] = random.uniform(self.minMIS, self.maxMIS)
        return MS

    def genSDC(self):
        return random.uniform(self.minSDC, self.maxSDC)

    def genData(self):
        data = {}
        data["T"] = self.genTransactions()
        data["MS"] = self.genMIS()
        data["SDC"] = self.genSDC()

        return data
