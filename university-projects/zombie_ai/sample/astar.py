from queue import PriorityQueue


def a_star(start, goal, grid):
    open_set = PriorityQueue()
    start_tuple = (int(start.x), int(start.y))
    goal_tuple = (int(goal.x), int(goal.y))
    open_set.put((0, start_tuple))
    came_from = {}
    g_score = {node: float("inf") for node in grid}
    g_score[start_tuple] = 0
    f_score = {node: float("inf") for node in grid}
    f_score[start_tuple] = heuristic(start_tuple, goal_tuple)

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal_tuple:
            return reconstruct_path(came_from, current, grid)

        for neighbor in get_neighbors(current, grid):
            if not grid[neighbor]["walkable"]:
                continue

            tentative_g = g_score[current] + 1
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal_tuple)
                open_set.put((f_score[neighbor], neighbor))

    return None



def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def reconstruct_path(came_from, current, grid):
    path = []
    while current in came_from:
        if grid[current]["walkable"]:
            path.insert(0, current)
        current = came_from[current]
    return path


def get_neighbors(node, world):
    neighbors = []
    x, y = node
    possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for move in possible_moves:
        if move in world and world[move]["walkable"]:
            neighbors.append(move)

    return neighbors