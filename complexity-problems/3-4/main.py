import random
import numpy as np
import collections
import matplotlib.pyplot as plt

SIZE = 20

def create_lattice(p,size):


    matrix = []


    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(0)
            ran_choice = random.uniform(0,1)
            if (ran_choice <= p):
                matrix[i][j] = 1

    return matrix


def get_adjacent(pos, size):
    queue = []

    row = pos[0]
    col = pos[1]

    row_up = row-1
    row_down = row+1
    col_right=col+1
    col_left = col-1

    if (row_up >= 0):
        queue.append((row_up, col))

        if (col_right<size):
            queue.append((row_up,col_right))
        if (col_left>=0):
            queue.append((row_up,col_left))

    if (row_down < size):
        queue.append((row_down, col))

        if (col_right<size):
            queue.append((row_down,col_right))
        if (col_left>=0):
            queue.append((row_down,col_left))

    if (col_right < size):
        queue.append((row, col_right))


    if (col_left >= 0):
        queue.append((row, col_left))


    return queue

def BFS(g, pos,size):
    visited = set()
    queue = collections.deque()

    # pos is (row,col)

    queue.appendleft(pos)


    while len(queue) > 0:


        pos = queue.popleft()

        visited.add(pos)

        for adj in get_adjacent(pos, size):
            if adj not in visited and g[adj[0]][adj[1]] == 1:
                queue.appendleft(adj)



    return visited

def find_largest_component(g, size):

    largest = 0
    global_visited = set()

    largest_path = []

    for row in range(size):
        for col in range(size):
            if g[row][col] == 1 and ((row, col) not in global_visited):
                pos = (row, col)
                
                new_search = BFS(g, pos, size)
                global_visited.update(new_search)
                if len(new_search) > largest:
                    largest = len(new_search)
                    largest_path = new_search

    return largest, largest_path

def print_matrix(g, size):
    for i in range(size):
        print(g[i])


def vary_p():
    results = {}
    for p in np.arange(0,1,0.1):   
        print(p)
        mat = create_lattice(p, SIZE)
        largest_comp_size, largest_comp = find_largest_component(mat, SIZE)
        results[p] = largest_comp_size

    print(results)
    return results

results = vary_p()
plt.plot(results.keys(), results.values())
plt.xlabel("p")
plt.ylabel("Largest Connected Component Size")
plt.show()
                




