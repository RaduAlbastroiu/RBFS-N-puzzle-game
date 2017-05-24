#!/usr/bin/env python

import sys
from optparse import OptionParser
import math
from struct import pack
import heapq
from random import randint

class Solver:
    def __init__(self, n):
        self.N = n
        self.L = n * n

        self.GOAL = range(1, self.L)
        self.GOAL.append(0)

        # slide rules
        self.SR = {}
        for i in range(self.L):
            s = []
            if i - self.N >= 0:
                s.append(i - self.N)
            if (i % self.N) - 1 >= 0:
                s.append(i - 1)
            if (i % self.N) + 1 < self.N:
                s.append(i + 1)
            if i + self.N < self.L:
                s.append(i + self.N)
            self.SR[i] = s

        # queue
        self.queue = []
        self.enqueued = {}

    def is_solvable(self, tiles):
        x = 0
        for p in range(len(tiles)):
            a = tiles[p]
            if a < 2 :
                continue
            for b in tiles[p:]:
                if b == 0:
                    continue
                if a > b:
                    x = x + 1
        return (x & 1) == 0

    def neighbors(self, tiles):
        n = []
        a = tiles.index(0)
        for b in self.SR[a]:
            n.append(self.swap(list(tiles), a, b))
        return n

    def swap(self, tiles, a, b):
        tiles[a], tiles[b] = tiles[b], tiles[a]
        return tiles

    def display(self, tiles):
        for i in range(self.L):
            if tiles[i]:
                print '%(n)#2d' % {'n': tiles[i]},
            else:
                print '  ',
            if i % self.N == self.N - 1:
                print

    def enqueue(self, state):
        (tiles, parent, h, g) = state

        heapq.heappush(self.queue, (h, state))

    def dequeue(self):
        if len(self.queue) <= 0:
            return None
        (f, state) = heapq.heappop(self.queue)
        return state

    def manhattan(self, tiles):
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n == 0:
                continue
            h += int(abs(n - 1 - i) / self.N) + (abs(n - 1 - i) % self.N)
        return h

    def solve(self, initial):
        if not self.is_solvable(initial):
            return None

        state = (initial, None, self.manhattan(initial), 0);
        if initial == self.GOAL:
            return state

        self.enqueue(state)

        while True:
            state = self.dequeue()
            if (not state):
                break

            (tiles, parent, h, g) = state
            neighbors = self.neighbors(tiles)
            for n_tiles in neighbors:
                if n_tiles == self.GOAL:
                    return (n_tiles, state, 0, g + 1)

                packed = pack(self.L*'B', *n_tiles)
                if (packed in self.enqueued):
                    continue;
                self.enqueued[packed] = True

                n_state = (n_tiles, state, self.manhattan(n_tiles), g + 1)
                self.enqueue(n_state)

def main():

    # i have to generate this
    initial = [15,14,13,12,11,10,9,8,7,6,5,4,3,1,2,0]
    initial2 = [8,7,6,5,4,3,2,1,0]

    succes = 0
    total = 10000
    sir = []
    for i in range(total):
        n = randint(2, 3)
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

    nr = 0
    maxSol = 0
    for initial in sir:
        nr = nr + 1
        #print
        #print " #", nr
        #print " matrice ", len(initial)
        #print initial

        solver = Solver(int(math.sqrt(len(initial))))

        state = solver.solve(initial)
        if not state:
            #print "No solution possible"
            continue

        # reconstruct the solution
        solution = []
        nrStates = 0;
        while state:
            (tiles, parent, h, g) = state
            solution.insert(0, tiles)
            nrStates = nrStates + 1
            state = parent

        #print "Number of states enqueued =", nrStates
        if nrStates > maxSol:
            maxSol = nrStates
        succes = succes + 1

    print "succes rate =", succes, "/", total
    print "max ", maxSol
    return 0

if __name__ == '__main__':
    sys.exit(main())
