"""
JungBok lee
6896785721
CS360_intro_AI_PA1

"""


class masterChef:
    # initialization
    def __init__(self):
        inputFile = "input6.txt"
        numContestant, minimax, contestants = self.readInput(inputFile)
        mmn = MinMaxNode(numContestant, minimax, contestants)
        ans = mmn.getId()
        self.writeOutput(ans)
    '''
      First line: strictly positive 32-bit integer n, number of contestants 
      Second line: algorithms to use(minimax or ab)
      next n lines: ID, Capacity[0.0, 200.0], Happy_A[0.0, 1.0], Happy_B[0.0, 1.0], Pick State(0, 1, 2)
     '''
    def readInput(self, inputFile):
        minimax = True
        fp = open(inputFile, 'r')
        # # of contestants
        fl = fp.readline()
        c = int(fl)
        # Algorithms to use
        forl = fp.readline()
        forl = forl.strip()
        # print
        ##########################################################
        if forl != "minimax":
            minimax = False

        # store contestants' info
        contestants = {}
        nalines = fp.readlines()
        for line in nalines:
            # person = np.zeros(4)
            l1, l2, l3, l4, l5 = line.split(",", 5)
            id = int(l1)
            # person[0] = float(l2)
            # person[1] = float(l3)
            # person[2] = float(l4)
            # person[3] = int(l5)
            # added last digit in the tuple by id%10
            lastDigit = id%10
            person = (float(l2), float(l3), float(l4), int(l5), lastDigit)
            contestants[id] = person
        #except IOError:
            #print("Unable to open the file")
        #finally:
        fp.close()
        # print(contestants)
        return c, minimax, contestants



    def writeOutput(self, ans):
        try:
            # print(ans)
            f = open('output.txt', 'w')
            f.write(str(ans))
        except IOError:
            print("unable to write output file")
        finally:
            f.close()




class MinMaxNode(object):
    # n = number of contestants alg = "algorithm to use" contestants: dictionary of players where player id is key
    # and player (Capacity[0.0, 200.0], Happy_A[0.0, 1.0], Happy_B[0.0, 1.0], Pick State(0, 1, 2), lastDigit) as val
    def __init__(self, n, alg, contestants):
        self.unpicked, self.myTeam, self.bobsTeam= self.getTeamlists(contestants)
        self.id = 0
        #print("myTeam")
        #print(self.myTeam)
        #print("Bob's team")
        #print(self.bobsTeam)
        #print("unpicked")
        #print(self.unpicked)

        if alg:
            adv, id = self.minmax(n, self.myTeam, self.bobsTeam, self.unpicked, True)
            # print(adv)
            self.id = id
            print(id)


        else:
            # sort unpicked
            # print(self.unpicked)
            # print("after sorted")
            # ascendingOrder = sorted(self.unpicked.keys())
            ascendingOrder = {id:self.unpicked[id] for id in sorted(self.unpicked.keys())}
            # print(ascendingOrder)
            alpha = float("-inf")
            beta = float("inf")
            adv, id = self.alphaBeta(n, self.myTeam, self.bobsTeam, ascendingOrder, alpha, beta, True)
            self.id = id
            # print(id)


    def getTeamlists(self, contestants):
        unpicked = {}
        myteam = {}
        bobsTeam = {}
        for id in contestants:
            data = contestants[id]
            if data[3] == 0:
                unpicked[id] = data
            elif data[3] == 1:
                myteam[id] = data
            else:
                bobsTeam[id] = data

        return unpicked, myteam, bobsTeam

    def minmax(self, n, max_contestants, min_contestants, unpicked_contestants, myTeamMember):
        # base case
        picked = self.getSelectedContestants(max_contestants, min_contestants)
        if picked == n or picked == 10:
            adv = self.calcAdvantage(max_contestants, min_contestants)
            # print(adv)
            return adv, 0

        if myTeamMember:
            maxVal = float("-inf")
            max_contestant_id = 0
            tempCopy = unpicked_contestants.copy()
            for unpickedId in unpicked_contestants:

                unpickedData = tempCopy.pop(unpickedId)
                max_contestants[unpickedId] = unpickedData
                advantage, _ = self.minmax(n, max_contestants, min_contestants, tempCopy, False)

                if advantage > maxVal:
                    maxVal = advantage
                    max_contestant_id = unpickedId
                # tie breaker
                elif advantage == maxVal and max_contestant_id > unpickedId:
                    max_contestant_id = unpickedId

                tempCopy[unpickedId] = max_contestants.pop(unpickedId)
                # unpicked_contestants[unpickedId] = max_contestants.pop(unpickedId)

            return maxVal, max_contestant_id
        else:
            minVal = float("inf")
            min_contestant_id = 0
            tempCopy = unpicked_contestants.copy()
            for unpickedId in unpicked_contestants:

                unpickedData = tempCopy.pop(unpickedId)
                min_contestants[unpickedId] = unpickedData
                advantage, _ = self.minmax(n, max_contestants, min_contestants, tempCopy,
                                               True)

                if advantage < minVal:
                    minVal = advantage
                    min_contestant_id = unpickedId
                # tie breaker
                elif advantage == minVal and min_contestant_id > unpickedId:
                    min_contestant_id = unpickedId

                tempCopy[unpickedId] = min_contestants.pop(unpickedId)
                # unpicked_contestants[unpickedId] = min_contestants.pop(unpickedId)

            return minVal, min_contestant_id


    def alphaBeta(self, n, max_contestants, min_contestants, unpicked_contestants, alpha, beta, myTeamMember):
        # base case
        picked = self.getSelectedContestants(max_contestants, min_contestants)
        if picked == n or picked == 10:
            adv = self.calcAdvantage(max_contestants, min_contestants)
            return adv, 0

        if myTeamMember:
            maxVal = float("-inf")
            max_contestant_id = 0
            tempCopy = unpicked_contestants.copy()
            for unpickedId in unpicked_contestants:

                unpickedData = tempCopy.pop(unpickedId)
                max_contestants[unpickedId] = unpickedData
                advantage, _ = self.alphaBeta(n, max_contestants, min_contestants, tempCopy, alpha, beta, False)

                if advantage > maxVal:
                    maxVal = advantage
                    max_contestant_id = unpickedId
                    # alpha = maxVal

                # tie breaker
                elif advantage == maxVal and max_contestant_id > unpickedId:
                    max_contestant_id = unpickedId

                tempCopy[unpickedId] = max_contestants.pop(unpickedId)
                alpha = max(maxVal, alpha)

                if beta <= alpha:
                    break

            return maxVal, max_contestant_id
        else:
            minVal = float("inf")
            min_contestant_id = 0
            tempCopy = unpicked_contestants.copy()
            for unpickedId in unpicked_contestants:

                unpickedData = tempCopy.pop(unpickedId)
                min_contestants[unpickedId] = unpickedData
                advantage, _ = self.alphaBeta(n, max_contestants, min_contestants, tempCopy, alpha, beta,
                                           True)

                if advantage < minVal:
                    minVal = advantage
                    min_contestant_id = unpickedId
                    # beta = minVal

                # tie breaker
                elif advantage == minVal and min_contestant_id > unpickedId:
                    min_contestant_id = unpickedId

                tempCopy[unpickedId] = min_contestants.pop(unpickedId)
                beta = min(minVal, beta)
                if beta <= alpha:
                    break

            return minVal, min_contestant_id





    def getSelectedContestants(self, max_contestants, min_contestants):
        return len(max_contestants) + len(min_contestants)


    def calcAdvantage(self, max_contestants, min_contestants):

        myTeamPower = self.calcPower(max_contestants, 1)
        bobsTeamPower = self.calcPower(min_contestants, 2)
        return (myTeamPower - bobsTeamPower)



    # team is dictionary of team members, captain is int val indicating myself or bob (1, 2)
    def calcPower(self, team, captain):
        teamPower = 0
        lastDigits = []

        for id in team:
            data = team[id]
            # data (Capacity[0.0, 200.0], Happy_A[0.0, 1.0], Happy_B[0.0, 1.0], Pick State(0, 1, 2)(INT), last digit(INT))
            teamPower = teamPower + (data[0]*data[captain])
            lastDigits.append(data[4])

        bp = self.calcBonusPoints(lastDigits)
        teamPower = teamPower + bp

        return teamPower


    def calcBonusPoints(self, digits):
        bp = 0.0
        flag = len(set(digits)) == len(digits)
        # if list contains all unique elements, bp = 120
        if (flag) :
            bp = 120.0

        return bp

    def getId(self):
        return self.id

if __name__ == "__main__":
    #print(timeit.timeit("masterChef()", setup="from __main__ import masterChef"))
    sol = masterChef()
