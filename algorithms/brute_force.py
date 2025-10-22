import itertools
import math

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def brute_force(cities):
    """Метод полного перебора для задачи коммивояжера"""
    if len(cities) < 2:
        return None, float('inf')

    n = len(cities)
    start = 0
    D = [[distance(cities[i], cities[j]) for j in range(n)] for i in range(n)]

    best_route = None
    best_distance = float('inf')

    for perm in itertools.permutations([i for i in range(n) if i != start]):
        route = [start] + list(perm) + [start]
        dist = sum(D[route[i]][route[i + 1]] for i in range(len(route) - 1))
        if dist < best_distance:
            best_distance = dist
            best_route = route

    return best_route, best_distance
