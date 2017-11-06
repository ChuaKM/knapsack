#!/usr/bin/python
# -*- coding: utf-8 -*-
# Dynamic Programming solution to knapsack problem

import numpy as np
from numba import jit, uint32, int32


from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def build_table(table, v, w):

    j = table.shape[0] - 1
    k = table.shape[1] - 1

    for j in range(j + 1):
        for k in range(k + 1):
            if j == 0:
                table[j, k] = 0
            elif w[j - 1] <= k:
                table[j, k] = max(table[j - 1, k], v[j - 1] + table[j - 1, k - w[j - 1]])
            else:
                table[j, k] = table[j - 1, k]
    return table

def traceback(table, j, k, w):
    taken = []
    for j in reversed(xrange(j+1)):
        if table[j, k] == table[j-1, k]:
            taken.append(0)
        else:
            taken.append(1)
            k -= w[j-1]
    taken = taken[::-1]
    del taken[0]
    return taken

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    j = int(firstLine[0])
    k = int(firstLine[1])

    v = []
    w = []

    for i in range(1, j + 1):
        line = lines[i]
        parts = line.split()

        v.append(int(parts[0]))
        w.append(int(parts[1]))

    v = np.array(v, dtype=np.int32)
    w = np.array(w, dtype=np.int32)
    table = np.zeros((j +1, k +1), dtype=np.int32)
    table_fast = jit(int32[:,:](int32[:,:],int32[:],int32[:]))(build_table)
    table = table_fast(table, v, w)
    taken = traceback(table, j, k, w)
    value = int(table[j, k])
    # # a trivial greedy algorithm for filling the knapsack
    # # it takes items in-order until the knapsack is full
    # value = 0
    # weight = 0
    # taken = [0]*len(items)
    #
    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        inputfile = open(file_location, 'r')
        input_data = ''.join(inputfile.readlines())
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

