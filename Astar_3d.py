# -*- coding: utf-8 -*-
'''
author: Lin Peng
create_time:2018.12.08 21:30
organization:Fudan University
introduction: use 3D map of Fudan Guanghua Tower and A* algorithm for path planing
tips:win64 OS 4G RAM may need 30 minutes for runing this code
'''
import numpy as np
from heapq import heappush, heappop


def heuristic_cost_estimate(neighbor, goal):
    x = neighbor[0] - goal[0]
    y = neighbor[1] - goal[1]
    z = neighbor[2] - goal[2]
    return abs(x) + abs(y) + abs(z)


def dist_between(a, b):
    return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2 + (b[2] - a[2]) ** 2


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path


# astar function returns a list of points (shortest path)
def astar(array, start, goal):
    #directions = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]  # 6个方向
    directions = [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1), (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
                  (-1, 1, -1), (-1, 1, 0), (-1, 1, 1), (0, -1, -1), (0, -1, 0), (0, -1, 1),
                  (0, 0, -1), (0, 0, 1), (0, 1, -1), (0, 1, 0), (0, 1, 1), (1, -1, -1),
                  (1, -1, 0), (1, -1, 1), (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 1, -1),
                  (1, 1, 0), (1, 1, 1)]  # 26个方向

    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic_cost_estimate(start, goal)}

    openSet = []
    heappush(openSet, (fscore[start], start))  # 往堆中插入一条新的值

    # while openSet is not empty
    while openSet:
        # current := the node in openSet having the lowest fScore value
        current = heappop(openSet)[1]  # 从堆中弹出fscore最小的节点

        if current == goal:
            return reconstruct_path(came_from, current)

        close_set.add(current)

        for i, j, k in directions:  # 对当前节点的 6 个相邻节点一一进行检查
            neighbor = current[0] + i, current[1] + j, current[2] + k

            ## 判断节点是否在地图范围内，并判断是否为障碍物
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if 0 <= neighbor[2] < array.shape[2]:
                        if array[neighbor[0]][neighbor[1]][neighbor[2]] == 0:  # 0为障碍物
                            continue
                    else:
                        # array bound z walls
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            # Ignore the neighbor which is already evaluated.
            if neighbor in close_set:
                continue

            #  The distance from start to a neighbor via current
            tentative_gScore = gscore[current] + dist_between(current, neighbor)

            if neighbor not in [i[1] for i in openSet]:  # Discover a new node
                heappush(openSet, (fscore.get(neighbor, np.inf), neighbor))
            elif tentative_gScore >= gscore.get(neighbor, np.inf):  # This is not a better path.
                continue

                # This path is the best until now. Record it!
            came_from[neighbor] = current
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tentative_gScore + heuristic_cost_estimate(neighbor, goal)

    return False


def add_obstacle(array1, init_3d, length_3d):
    for i in range(length_3d[0]):
        for j in range(length_3d[1]):
            for k in range(length_3d[2]):
                array1[init_3d[0]+i][init_3d[1]+j][init_3d[2]+k] = 0

    return array1


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    plt.xlim(0, 180)
    plt.ylim(0, 180)
    map = np.load('guanghua.npy')
    for i in range(0, 180, 3):
        for j in range(0, 50, 3):
            for k in range(0, 150, 3):
                if map[i][j][k] == 0:
                    ax.scatter(i, j, k, s=5, c='k', marker='o')

    path = astar(map, (1, 1, 5), (90, 14, 100))
    plt.plot([data[0] for data in path], [data[1] for data in path], [data[2] for data in path], '-r')
    for (px, py, pz) in path:
        ax.scatter(px, py, pz, s=10, c='b', marker='o')
    print(path)
    plt.show()
