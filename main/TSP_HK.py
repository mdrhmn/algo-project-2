import itertools
import random
import sys

cities_list = ["KUL", "JAK", "BKK", "HKG", "TPE", "TOK", "KOR", "PEK"]

def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = []
    path.append(0)

    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list((path))


def read_distances(filename):
    dists = []
    with open(filename, 'r') as f:
        for line in f:
            # Skip comments
            if line[0] == '#':
                continue

            dists.append(list(map(float, map(str.strip, line.split(' ')))))

    return dists


n = 8

arg = "/Users/muhdrahiman/Desktop/SE 18:19/S4/[WIA2005] (ALGORITHM DESIGN AND ANALYSIS)/GROUP ASSIGNMENT/QUESTION 2/test/input.txt"

dists = read_distances(arg)

shortest_route_dist = held_karp(dists)

print("HELD-KARP ALGORITHM:")
print("Shortest distance    : {} km".format(shortest_route_dist[0]))
print("Shortest path (index):", end=' ')
for i in range(n + 1):
    if (i + 1 < n + 1):
        print(shortest_route_dist[1][i], end=' -> ')
    else:
        print(shortest_route_dist[1][i], end=' (and vice versa)\n')

print("Shortest path (nodes):", end=' ')
for i in range(n + 1):
    if (i + 1 < n + 1):
        print(cities_list[shortest_route_dist[1][i]], end=' -> ')
    else:
        print(cities_list[shortest_route_dist[1][i]],
              end=' (and vice versa)\n')
