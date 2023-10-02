
class NearestNeighbor:
    def __init__(self, avg_speed_mph):
        self.avg_speed_mph = avg_speed_mph

    def run(self, adj_matrix, start_node=0):
        """
        Nearest Neighbor algorithm for TSP.
        Note: this algorithm is pretty inefficient for the routing problem as described, this simple implementation
        merely seeks to visit all the nodes in the adjacency matrix with no regard for if the packages in the truck
        need to visit each location

        :param adj_matrix: 2D list representing the adjacency matrix.
                           adj_matrix[i][j] is the distance from node i to node j.
        :param start_node: Node to start the tour.
        :return: List representing the tour and the total cost of the tour.

        # Example usage:
            adj_matrix = [
                [0, 29, 20, 21],
                [29, 0, 15, 17],
                [20, 15, 0, 28],
                [21, 17, 28, 0]
            ]

            tour, cost = nearest_neighbor(adj_matrix)
            print(f"Tour: {tour}")
            print(f"Total Cost: {cost}")
        """
        num_nodes = len(adj_matrix)
        unvisited = set(range(num_nodes))
        current_node = start_node
        tour = [current_node]
        time_traveled = [0]
        total_cost = 0
        tour_cost = []

        unvisited.remove(current_node)

        while unvisited:
            nearest_node = min(unvisited, key=lambda node: adj_matrix[current_node][node])
            current_cost = adj_matrix[current_node][nearest_node]
            total_cost += current_cost
            time_traveled.append(current_cost/self.avg_speed_mph)
            current_node = nearest_node
            tour.append(current_node)
            tour_cost.append(current_cost)
            unvisited.remove(current_node)

        # Return to the start node to complete the tour
        last_cost = adj_matrix[current_node][start_node]
        total_cost += last_cost
        time_traveled.append(last_cost/self.avg_speed_mph)
        tour.append(start_node)
        tour_cost.append(last_cost)

        return tour, total_cost, time_traveled, tour_cost
