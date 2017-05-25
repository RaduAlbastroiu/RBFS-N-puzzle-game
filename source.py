#!/usr/bin/env python

import sys
from optparse import OptionParser
import math
from struct import pack
import heapq
from random import randint
from datetime import datetime
import argparse

class Solver:
    def __init__(self, n):
        self.N = n
        self.L = n * n
        
        # setting the goal state
        self.GOAL = range(1, self.L)
        self.GOAL.append(0)

        # number of steps to first solution
        self.numberSteps = 0

        
        # slide rules
        self.SR = {}
        for i in range(self.L):
            s = []
            # if i is not on the first lane
            if i - self.N >= 0:
                s.append(i - self.N)
            
            # if i is not on the first column
            if (i % self.N) - 1 >= 0:
                s.append(i - 1)

            # if i is not on the last column
            if (i % self.N) + 1 < self.N:
                s.append(i + 1)

            # if i is not on the last line
            if i + self.N < self.L:
                s.append(i + self.N)

            # rule
            self.SR[i] = s

        # queue
        self.queue = []
        self.enqueued = {}

    # if initial state could transform in a goal state
    def is_solvable(self, tiles):
        x = 0

        # a n-puzzle game is solvable if the sum
        # of all inversions between a lower number
        # and a bigger number is even
        # reference:
        # https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
        for p in range(len(tiles)):
            a = tiles[p]
            if a < 2 :
                continue
            for b in tiles[p:]:
                if b == 0:
                    continue
                if a > b:
                    x = x + 1
        return x % 2 == 0

    # gets all the states tha can derive
    # from the current set of tiles
    def neighbors(self, tiles):
        n = []
        a = tiles.index(0)
        for b in self.SR[a]:
            n.append(self.swap(list(tiles), a, b))
        return n

    # changes two tiles in between them
    def swap(self, tiles, a, b):
        tiles[a], tiles[b] = tiles[b], tiles[a]
        return tiles

    # enqueues the current state in a priority queue
    # with the value calculated by manhattan dist
    def enqueue(self, state):
        (tiles, parent, heuristic) = state

        heapq.heappush(self.queue, (heuristic, state))

    # pop first element from priority queue
    def dequeue(self):
        if len(self.queue) <= 0:
            return None
        (f, state) = heapq.heappop(self.queue)
        return state

    # computes the total manhattan distance between
    # current state and the goal state
    def manhattan(self, tiles):
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n == 0:
                continue
            h += int(abs(n - 1 - i) / self.N) + (abs(n - 1 - i) % self.N)
        return h

    # returns the goal state or a null
    def solve(self, initial):
        
        # check if initial state si solvable
        if not self.is_solvable(initial):
            return None

        # first state 
        # initial set of tiles
        # parrent is null
        # heuristic for the initial state of tiles
        # 0 steps
        state = (initial, None, self.manhattan(initial));
        if initial == self.GOAL:
            return state

        # put first state into priority queue
        self.enqueue(state)

        # recursion
        while True:
            # take top of priority queue
            # state is the best state 
            # based on my heuristic method
            state = self.dequeue()
            if (not state):
                break

            # counting number of steps
            self.numberSteps = self.numberSteps + 1
            (tiles, parent, h) = state
            
            # taking the neighbors of this state
            neighbors = self.neighbors(tiles)
            
            for n_tiles in neighbors:
                # check if a neighbor is a goal state
                if n_tiles == self.GOAL:
                    return (n_tiles, state, 0)

                # check if this state is already
                # in the priority queue
                # if it is then skip
                packed = pack(self.L*'B', *n_tiles)
                if (packed in self.enqueued):
                    continue;
    
                # put the new state into priority queue
                self.enqueued[packed] = True
                n_state = (n_tiles, state, self.manhattan(n_tiles))
                self.enqueue(n_state)

def main():

    # print to file
    f = open('raport.txt', 'w')

    total = 1000

    succes2 = 0
    succes3 = 0

    # setting all variables
    minimumNrMoves2 = 999999
    maximumNrMoves2 = 0
    nrMoves2 = 0

    minimumNrMoves3 = 999999
    maximumNrMoves3 = 0
    nrMoves3 = 0    


    minimumNrSteps2 = 999999
    maximumNrSteps2 = 0
    nrSteps2FirstSolution = 0

    minimumNrSteps3 = 999999
    maximumNrSteps3 = 0
    nrSteps3FirstSolution = 0

    sir = []
    #generate 2X2 puzzle
    for i in range(total):
        n = 2
        # position of zero in the matrix
        pozZero = randint(0, n * n - 1)
        s = []
        for j in range(n*n):
            if j == pozZero:
                s.append(0)
            else:
                nr = randint(1, n * n - 1)
                while nr in s:
                    nr = randint(1, n * n - 1)
                s.append(nr)    
        sir.append(s)

    #generate 3X3 puzzle
    for i in range(total):
        n = 3
        # position of zero in the matrix
        pozZero = randint(0, n * n - 1)
        s = []
        for j in range(n*n):
            if j == pozZero:
                s.append(0)
            else:
                nr = randint(1, n * n - 1)
                while nr in s:
                    nr = randint(1, n * n - 1)
                s.append(nr)
        sir.append(s)

    # start time
    start = datetime.now()
    for initial in sir:
        nr = nr + 1
        #print
        print " #", nr, " dimension ", len(initial)
        #print " matrice ", len(initial)
        #print initial
        
        if len(initial) < 5:
            finish2 = datetime.now()

        solver = Solver(int(math.sqrt(len(initial))))

        # solve method call
        state = solver.solve(initial)

        if not state:
            #print "No solution possible"
            continue

        # reconstruct the solution
        solution = []
        nrMoves = 0
        while state:
            (tiles, parent, h) = state
            solution.insert(0, tiles)
            nrMoves = nrMoves + 1
            state = parent

        # initial state doesn't count as a move
        nrMoves = nrMoves - 1

        # for each size of input
        if len(initial) > 5:
            # size 3X3
            succes3 = succes3 + 1

            nrSteps3FirstSolution = nrSteps3FirstSolution + solver.numberSteps
            if solver.numberSteps > maximumNrSteps3:
                maximumNrSteps3 = solver.numberSteps
            if solver.numberSteps < minimumNrSteps3:
                minimumNrSteps3 = solver.numberSteps

            nrMoves3 = nrMoves3 + nrMoves
            if nrMoves < minimumNrMoves3:
                minimumNrMoves3 = nrMoves
            if nrMoves > maximumNrMoves3:
                maximumNrMoves3 = nrMoves

        else:
            # size 2X2
            succes2 = succes2 + 1

            nrSteps2FirstSolution = nrSteps2FirstSolution + solver.numberSteps
            if solver.numberSteps > maximumNrSteps2:
                maximumNrSteps2 = solver.numberSteps
            if solver.numberSteps < minimumNrSteps2:
                minimumNrSteps2 = solver.numberSteps

            nrMoves2 = nrMoves2 + nrMoves
            if nrMoves < minimumNrMoves2:
                minimumNrMoves2 = nrMoves
            if nrMoves > maximumNrMoves2:
                maximumNrMoves2  = nrMoves

    # take finish time
    finish3 = datetime.now()
    totalDuration = finish3 - start
    duration2 = finish2 - start
    duration3 = totalDuration - duration2

    print(" See raport.txt ")

    # printing raport
    f.write("\n Number of tests: " + str(total) + "\n\n")

    f.write(" Solve rate for 2X2 = " + str(succes2) + "/" + str(total) + "\n")
    f.write(" Solve rate for 3X3 = " + str(succes3) + "/" + str(total)+ "\n\n")

    f.write(" Average number of steps for first solution 2X2: " + str(nrSteps2FirstSolution / succes2) + "\n")
    f.write(" Miniumum number of steps for first solution 2X2: " + str(minimumNrSteps2) + "\n")
    f.write(" Maxiumum number of steps for first solution 2X2: " + str(maximumNrSteps2) + "\n\n")

    f.write(" Average number of moves for first solution 2X2: " + str(nrMoves2 / succes2) + "\n")
    f.write(" Miniumum number of moves for first solution 2X2: " + str(minimumNrMoves2) + "\n")
    f.write(" Maxiumum number of moves for first solution 2X2: " + str(maximumNrMoves2) + "\n\n")

    f.write(" Average number of steps for first solution 3X3: " + str(nrSteps3FirstSolution / succes3) + "\n")
    f.write(" Miniumum number of steps for first solution 3X3: " + str(minimumNrSteps3) + "\n")
    f.write(" Maxiumum number of steps for first solution 3X3: " + str(maximumNrSteps3) + "\n\n")

    f.write(" Average number of moves for first solution 3X3: " + str(nrMoves3 / succes3) + "\n")
    f.write(" Miniumum number of moves for first solution 3X3: " + str(minimumNrMoves3) + "\n")
    f.write(" Maxiumum number of moves for first solution 3X3: " + str(maximumNrMoves3) + "\n\n")

    f.write(" Average time in h:mm:ss.ms for first solution 2X2: " + str(duration2 / succes2) + "\n")
    f.write(" Total time in h:mm:ss.ms for all 2X2 solutions: " + str(duration2) + "\n\n")

    f.write(" Average time in h:mm:ss.ms for first solution 3X3: " + str(duration3 / succes3) + "\n")
    f.write(" Total time in h:mm:ss.ms for all 3X3 solutions: " + str(duration3) + "\n\n")

    f.write(" Total time of execution in h:mm:ss.ms : " + str(totalDuration))
    
    return 0

if __name__ == '__main__':

    sys.exit(main())