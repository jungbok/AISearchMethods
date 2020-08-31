"""
JungBok lee
6896785721
CS360_intro_AI_PA1

"""
# global n
from queue import PriorityQueue
import sys

class Drone:
    # initialization
    def __init__(self):
        inputFile = "input39.txt"
        bSize, d, p, astar, board, a_dict, maxScore = self.readInput(inputFile)

        if not astar:
            # call dfs
            self.dfs(bSize, d, p, board, maxScore)
        else:
            self.aSearch(bSize, d, a_dict, maxScore)

    '''
      First line: strictly positive 32-bit integer n,
                  the width/height of the n x n delivery area, n <= 15 
      Second line: strictly positive 32-bit integer d, the number of drones, d <= n 
      Third line: strictly positive 32-bit integer p, the number of packages, p <= 100 
      Fourth line: algorithm to use, either astar for A* search or dfs for depth-first search 
      Next a lines: the list of package x,y coordinates, separated with the End-of-line character LF.
      Multiple lines with the same x,y coordinates denote multiple packages with the same location. 
     '''
    def readInput(self, inputFile):
        astar = True
        #try:
        fp = open(inputFile, 'r')
        # board size
        fl = fp.readline()
        bSize = int(fl)
        # number of drones
        sl = fp.readline()
        d = int(sl)
        # number of packages
        tl = fp.readline()
        p = int(tl)
        # algorithm to use: astar or dfs
        forl = fp.readline()
        forl = forl.strip()
            # print
            ##########################################################
            # print(astar)
        if forl != "astar":
            astar = False

        # store packages
        packages = [None]*p
        c = 0
        nalines = fp.readlines()
        for line in nalines:
            lhs, rhs = line.split(",", 1)
            packages[c] = (int(lhs), int(rhs))
            c += 1

        Board, pack_dict, ms = self.creatBoard(bSize, d, packages)

        #except IOError:
            #print("Unable to open the file")
        #finally:
        fp.close()

        return bSize, d, p, astar, Board, pack_dict, ms


    # create board - is this necessary?
    def creatBoard(self, n, d, packages):
        # initialize board with 0 in the beginning
        rows, cols = (n, n)
        board = [[0 for i in range(cols)] for j in range(rows)]
        # packet dictionary
        pack_dict = {}
        # add packages on the board
        # maxScore is limit that you can never go over
        maxScore = 0
        for package in packages:
            board[package[0]][package[1]] += 1
            # coordinates = x*n + y
            coor = (package[0], package[1])
            if coor in pack_dict:
                pack_dict[coor] = pack_dict[coor] + 1
            else:
                pack_dict[coor] = 1

        # sort dictionary/ more package, front of the dictionary, as a drone can hold more than one package
        # sorted(pack_dict.items(), key= lambda item:pack_dict.items())
        pack_dict = dict(sorted(pack_dict.items(), key=lambda x: x[1], reverse=True))
        print(pack_dict)
        nd = d
        # package mapping
        for key in pack_dict:
            if nd > 0:
                maxScore += pack_dict[key]
            nd -= 1

        return board, pack_dict, maxScore

    def dfs(self, n, d, p, board, maxScore):
        rows, cols = (n, n)
        # visited = [[False for k in range(cols)] for t in range(rows)]
        # stack: contains (#of packages, # of drones, droneBoard)
        state = []
        droneBoard = []
        # start state, but its not really a state, arbitrary example
        state.append((-1, 0, d, droneBoard))
        max = 0
        # push every state

        # there is a possibility where no drone is placed in row 0
        # if d < n
        # how do we figure it out?
        # add first append
        # if stack is not empty, continue
        while state:
            temp = state.pop()
            row = temp[0]
            np = temp[1]
            nd = temp[2]
            # hard copy of stack
            dB = temp[3].copy()
            tempDB = dB.copy()
            if (row >= n-1 or nd == 0):
                if max < np and nd == 0:
                    max = np
                    # print(tempDB)
                # break
            # optimization - see if it can reduce time
            # only for sometimes
            if max == maxScore:
                print(maxScore)
                self.writeOutput(max)
                sys.exit()

            else:
                if row < n-1:
                    state.append((row + 1, np, nd, dB))
                    row = row + 1
                    for i in range(cols):
                        # tempDB = list(dB)

                        if self.isSafe(row, i, tempDB, n):
                            tempP = board[row][i]
                            package = np + tempP
                            newDB = tempDB.copy()
                            # coordinate using x*n + y
                            # does this help?
                            coor = row*n+i
                            newDB.append(coor)
                            # add new state
                            state.append((row, package, nd-1, newDB))
                            # print(state)
                        else:
                            pass
        if max == -1:
            print("unable to solve to problem")
        else:
            self.writeOutput(max)
    ###

    # check if it is safe to allocate drone
    # only the left side of the current row and col
    def isSafe(self, row, col, drone, n):
        # check the row
        if drone:
            for i in range(len(drone)):
                # using x*n + y
                num = drone[i]
                x = int(num/n)
                y = int(num%n)
                if abs(row - x) == abs(col - y):
                    return False
                if x == row or y == col:
                    return False
        return True

    def aSearch(self, n, d, a_dict, maxScore):
        # tuple(a_dict)

        # initialize priority queue
        q = PriorityQueue()
        # initialize comparison
        max = 0

        # adding all the states in queue that is sorted based on # of packages
        for i in range(n):
            for j in range(n):
                # setting weight/priority to number of packages on coordinates
                # using a negative priority
                # coordinates: i*n+j - slower
                coor = (i,j)
                nPackage = -1 * (a_dict.get(coor, 0))
                packageMap = (nPackage, coor,)
                q.put(packageMap)

        # iteration while there is stuff left in queue
        while not q.empty():
            # top of the queue
            # current state: #of package, drone placement
            currState = q.get()

            # base case check # of drones placed and check invalid coordinates to decrease runtime
            # renew
            dronesOnMap = 0
            invalid_x = set([])
            invalid_y = set([])
            for coor in currState[1:]:
                invalid_x.add(coor[0])
                invalid_y.add(coor[1])
                dronesOnMap += 1

            # if all drones are on the board, check max and terminate if possible
            # maxScore is limit that you can never go over
            if (dronesOnMap == d):
                currScore = -1 * (currState[0])

                if (currScore > max):
                    max = currScore

                    if max == maxScore:
                        # print(max)
                        self.writeOutput(max)
                        sys.exit()

            else:
                for i in range(n):
                    if i not in invalid_x:
                        for j in range(n):
                            if j not in invalid_y:
                                if self.isSafeA(i, j, currState[1:]):
                                    # h(n) = # of package on i,j + # of package gathered
                                    n_heur = -1 * (a_dict.get((i, j), 0)) + currState[0]
                                    currCoor = (i, j),
                                    n_list = currState + currCoor
                                    # list without h(n)
                                    l_without_h = n_list[1:]
                                    # cannot do +=
                                    childList = (n_heur,) + l_without_h
                                    q.put(childList)
                                    # print(childList)
        self.writeOutput(max)


    def isSafeA(self, row, col, coordinates):
        for xy in coordinates:
            if abs(row == xy[0] or col == xy[1]):
                return False
            if abs(row - xy[0]) == abs(col - xy[1]):
                return False
        return True


    def writeOutput(self, ans):
        try:
            print(ans)
            f = open('output.txt', 'w')
            f.write(str(ans))
        except IOError:
            print("unable to write output file")
        finally:
            f.close()


if __name__ == "__main__":
    sol = Drone()
