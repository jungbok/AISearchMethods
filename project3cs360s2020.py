"""
JungBok lee
6896785721
CS360_intro_AI_PA1

"""
import numpy as np

class Decision:
    def __init__(self):
        inputFile = "input5.txt"
        self.n, self.obstacles, self.destination = self.readInput(inputFile)
        self.cValues = np.zeros((self.n, self.n), dtype=np.double)
        self.uValues = np.zeros((self.n, self.n), dtype=np.double)
        self.policies = np.empty((self.n, self.n), dtype="|S1")
        self.valueIteration()
        print(self.uValues)
        self.policyIteration()
        self.printPolicies()

    # reads input from the textfile and returns values: gridsize, obstacle positions, destination
    def readInput(self, inputFile):
        fp = open(inputFile, 'r')
        fl = fp.readline()
        # n = size of board
        n = int(fl)
        # number of Obstacles
        forl = fp.readline()
        nObstacles = int(forl)
        # print
        ##########################################################
        nalines = fp.readlines()
        obstacles = []
        destination = (0,0)
        for i, line in enumerate(nalines):
            x, y = line.split(",", 1)
            # last line has to be destination
            if i == nObstacles:
                destination = (int(x), int(y))
            else:
                obstacles.append((int(x),int(y)))
        fp.close()

        #print(n)
        #print(obstacles)
        #print(destination)

        return n, obstacles, destination

    # value iteration functions: (x,y) iteration
    def valueIteration(self):
        # delta = maximum change in utility of any state in an iteration
        # delta = 0
        gamma = 0.9
        epsilon = 0.01
        # print(cValues)
        # print(uValues)
        boardSize = self.n
        #value iteration
        while(True):
            delta = 0
            for col in range(boardSize):
                for row in range(boardSize):
                    self.cValues[col][row] = self.uValues[col][row]

            for col in range(boardSize):
                for row in range(boardSize):
                    utility = self.calcUtility(col, row)
                    self.uValues[col][row] = self.calcReward(col, row) + gamma*utility

                    diff = abs(self.uValues[col][row] - self.cValues[col][row])
                    #delta = max(delta, diff)
                    if delta < diff:
                        delta = diff

            #if delta < epsilon * (1 - gamma)/gamma:
            # print(delta)
            if delta < 0.01:
                break

    def policyIteration(self):
        boardSize = self.n
        for col in range(boardSize):
            for row in range(boardSize):
                if (col,row) == self.destination:
                    self.policies[col][row] = '.'
                elif (col,row) in set(self.obstacles):
                    self.policies[col][row] = 'o'
                else:
                    self.calcPolicy(col,row)

    # repeated function - can be optimized
    def calcPolicy(self, col, row):
        # up
        if row - 1 < 0:
            up = self.cValues[col][row]
        else:
            up = self.cValues[col][row - 1]

        # heading down
        if row + 1 >= self.n:
            down = self.cValues[col][row]
        else:
            down = self.cValues[col][row+1]

        # heading East
        if col + 1 >= self.n:
            right = self.cValues[col][row]
        else:
            right = self.cValues[col+1][row]

        # heading West
        if col - 1 < 0:
            left = self.cValues[col][row]
        else:
            left = self.cValues[col-1][row]

        utilityUp = 0.7 * up + 0.1*(down + right + left)
        utilityDown = 0.7 * down + 0.1*(up + right + left)
        utilityRight= 0.7 * right + 0.1*(up + down + left)
        utilityLeft = 0.7 * left + 0.1*(up + down + right)

        maxUtilityPolicy = max(max(utilityUp, utilityDown), max(utilityRight, utilityLeft))

        if maxUtilityPolicy == utilityUp:
            policy = '^'
        elif maxUtilityPolicy == utilityDown:
            policy = 'v'
        elif maxUtilityPolicy == utilityRight:
            policy = '>'
        else:
            policy = '<'

        self.policies[col][row] = policy


    # calculate utility with probability given. 0.7 : 0.1: 0.1: 0.1
    def calcUtility(self, col, row):
        if (col, row) == self.destination:
            return 0

        # heading north
        if row - 1 < 0:
            N = self.cValues[col][row]
        else:
            N = self.cValues[col][row - 1]

        # heading south
        if row + 1 >= self.n:
            S = self.cValues[col][row]
        else:
            S = self.cValues[col][row+1]

        # heading East
        if col + 1 >= self.n:
            E = self.cValues[col][row]
        else:
            E = self.cValues[col+1][row]

        # heading West
        if col - 1 < 0:
            W = self.cValues[col][row]
        else:
            W = self.cValues[col-1][row]

        utilityN = 0.7 * N + 0.1*(S + E + W)
        utilityS = 0.7 * S + 0.1*(N + E + W)
        utilityE= 0.7 * E + 0.1*(N + S + W)
        utilityW = 0.7 * W + 0.1*(N + S + E)

        maxUtility = max(max(utilityN, utilityS), max(utilityE, utilityW))
        #print(maxUtility)
        return maxUtility


    # Reward calculation: -1 for every tile as each step costs 1
    def calcReward(self, c, r):
        if (c,r) == self.destination:
           return 99
        else:
            for obstacle in self.obstacles:
                if (c,r) == obstacle:
                    return -101
            return -1


    def printPolicies(self):
        try:
            f = open('output.txt', 'w')
            for col in range(self.n):
                for row in range(self.n):
                    char = self.policies[row][col].decode('utf-8')
                    f.write(char)
                f.write("\n")


        except IOError:
            print("unable to write output file")
        finally:
            f.close()




if __name__ == "__main__":
    d = Decision()