from collections import defaultdict
import re


class DataProcessor:
    """ Takes input data for MSGSP and performes processing """

    DATA_FILE = "data/data.txt"
    PARAM_FILE = "data/para.txt"
    OUTPUT_FILE = "data/out.txt"

    DATA = []
    PARA = {}
    SDC = 0

    DEBUG = False

    def __init__(self, data_file_path, param_file_path, output_file_path, debug=False):
        self.DATA_FILE = data_file_path
        self.PARAM_FILE = param_file_path
        self.OUTPUT_FILE = output_file_path
        self.DEBUG = debug

    def loadInput(self):

        with open(self.DATA_FILE) as f:
            for line in f:
                line = line.strip()[1:-1]
                row_data = [[int(i) for i in re.split(',| ', s) if i != ''] for s in re.split(r'}{', line[1:-1])]
                self.DATA.append(row_data)

                if self.DEBUG:
                    print line, "->", row_data

        with open(self.PARAM_FILE) as f:
            for line in f:
                isMISMatch = re.match("^MIS\(\d+", line.strip())
                if isMISMatch:
                    item, value = int(isMISMatch.group().split('(')[1]), float(line.strip().split('=')[1].strip())
                    self.PARA[item] = value

                    if self.DEBUG:
                        print item, "->", value
                else :
                    self.SDC = float(line.strip().split('=')[1].strip())
                    if self.DEBUG:
                        print "SDC ->", self.SDC

        return {"T": self.DATA, "MS": self.PARA, "SDC": self.SDC}

    def printOutput(self, data):

        if not data:
            print "None"
            return

        with open(self.OUTPUT_FILE, 'w') as outFile:
            for i in range(max(data.keys())):

                print "Number of length", i+1, "sequential patterns:", len(data[i+1])
                outFile.write("Number of length " + str(i+1) + " sequential patterns: " + str(len(data[i+1])) + "\n")

                for j in data[i+1]:
                    seqi = []
                    for k in j[0]:
                        seqi.append("{" + ", ".join([str(l) for l in k]) + "}")

                    seq = "<" + ", ".join(seqi) + ">"

                    print "pattern:", seq, " count:", j[1]
                    outFile.write("pattern: " + seq + " count: " + str(j[1]) + "\n")

                print ""
                outFile.write("\n")

