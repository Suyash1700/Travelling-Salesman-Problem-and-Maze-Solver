"""Simple travelling salesman problem between cities."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math


def create_data_model(grid):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = grid  # yapf: disable
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print("Objective: {} miles".format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += " {} ->".format(manager.IndexToNode(index)+1)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += " {}\n".format(manager.IndexToNode(index)+1)
    print(plan_output)
    plan_output += "Route distance: {}miles\n".format(route_distance)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
#     N=25
#     grid=[[12, 100, 11, 85, 62, 58, 37, 12, 32, 5, 88, 40, 37, 49, 67, 90, 39, 70, 33, 77, 86, 30, 4, 20, 83], [83, 98, 82, 67, 75, 91, 50, 67, 65, 29, 33, 75, 68, 74, 88, 15, 29, 20, 72, 89, 58, 17, 73, 3, 4], [82, 34, 49, 4, 36, 9, 55, 96, 79, 70, 88, 91, 74, 47, 3, 31, 21, 47, 22, 48, 21, 75, 40, 76, 32], [93, 19, 70, 85, 85, 21, 32, 39, 51, 73, 7, 59, 5, 91, 87, 32, 52, 28, 10, 47, 91, 46, 52, 47, 40], [13, 41, 81, 85, 5, 32, 59, 43, 44, 48, 97, 10, 50, 87, 74, 62, 96, 78, 7, 80, 91, 21, 94, 48, 31], [48, 88, 59, 52, 20, 53, 89, 73, 6, 82, 83, 24, 65, 61, 56, 2, 76, 35, 39, 16, 31, 41, 46, 41, 93], [36, 11, 56, 21, 88, 46, 50, 70, 50, 47, 16, 31, 2, 3, 100, 29, 21, 88, 65, 53, 38, 5, 13, 
# 62, 86], [98, 46, 83, 28, 56, 41, 54, 15, 62, 79, 8, 100, 85, 16, 82, 60, 86, 19, 88, 77, 89, 41, 5, 17, 39], [85, 71, 19, 26, 17, 56, 67, 88, 97, 98, 78, 75, 30, 73, 53, 53, 74, 53, 79, 11, 7, 94, 37, 31, 59], [66, 24, 83, 41, 80, 75, 30, 96, 29, 97, 88, 54, 40, 47, 65, 19, 85, 90, 94, 52, 55, 13, 97, 99, 13], [45, 38, 35, 20, 86, 16, 19, 73, 
# 88, 98, 93, 82, 78, 11, 15, 30, 37, 34, 8, 41, 10, 96, 96, 65, 17], [53, 55, 52, 23, 41, 49, 27, 87, 55, 30, 28, 24, 11, 88, 92, 20, 78, 4, 46, 90, 53, 41, 12, 25, 42], [4, 
# 45, 59, 87, 47, 10, 42, 23, 53, 29, 41, 42, 30, 100, 94, 50, 32, 67, 67, 64, 62, 72, 79, 99, 35], [65, 41, 5, 85, 54, 35, 88, 21, 50, 47, 62, 48, 20, 71, 52, 53, 2, 95, 13, 
# 45, 37, 6, 1, 39, 9], [15, 53, 36, 57, 19, 8, 85, 35, 58, 13, 94, 20, 73, 9, 23, 3, 37, 33, 7, 10, 60, 50, 84, 15, 1], [7, 41, 46, 65, 74, 3, 38, 13, 90, 22, 2, 33, 76, 95, 
# 78, 31, 55, 56, 62, 65, 3, 36, 28, 25, 76], [97, 32, 24, 23, 78, 17, 37, 61, 79, 82, 52, 38, 39, 61, 89, 100, 30, 4, 81, 49, 43, 87, 41, 35, 59], [86, 94, 23, 53, 26, 23, 79, 17, 46, 39, 21, 12, 13, 22, 46, 11, 22, 55, 35, 58, 55, 93, 92, 72, 84], [56, 75, 82, 39, 38, 91, 15, 50, 59, 74, 17, 61, 45, 54, 20, 41, 9, 43, 30, 53, 53, 25, 57, 74, 86], [69, 17, 48, 41, 33, 93, 33, 55, 70, 97, 97, 95, 18, 35, 62, 37, 56, 9, 58, 55, 66, 86, 79, 69, 96], [48, 11, 53, 53, 7, 32, 18, 2, 38, 22, 85, 91, 43, 92, 81, 40, 52, 58, 94, 69, 57, 94, 5, 86, 3], [4, 86, 70, 57, 34, 6, 92, 13, 62, 93, 62, 96, 98, 88, 78, 58, 22, 55, 48, 57, 13, 51, 76, 23, 90], [86, 100, 47, 100, 54, 35, 35, 78, 33, 5, 7, 39, 96, 49, 43, 30, 42, 100, 10, 40, 63, 85, 30, 60, 62], [37, 94, 52, 30, 45, 63, 33, 38, 61, 56, 74, 13, 28, 55, 26, 20, 46, 35, 24, 38, 53, 64, 61, 10, 54], [24, 60, 39, 75, 46, 83, 13, 32, 58, 77, 68, 51, 67, 83, 18, 94, 17, 7, 10, 69, 50, 50, 96, 99, 16]]
    file = open("./TSPinput.txt", "r")
    N = int(file.readline())
    grid = []
    for _ in range(N):
        grid.append(list(map(int, file.readline().split())))


    data = create_data_model(grid)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    # search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.first_solution_strategy = (
    #     routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    # )
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 20
    # search_parameters.log_search = True
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == "__main__":
    main()
