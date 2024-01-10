
class NearestNeighbor:
    """
    A class implementing the Nearest Neighbor algorithm for solving the Traveling Salesman Problem (TSP).

    The algorithm starts at a given node and repeatedly visits the nearest unvisited node until all nodes have been visited.
    Note that this implementation is a simple heuristic and may not find the most efficient route for complex graphs.
    """
    def __init__(self, avg_speed_mph):
        """
        Initialize the NearestNeighbor with the average speed of travel.

        Parameters:
        - avg_speed_mph (float): Average speed in miles per hour.
        """
        self.avg_speed_mph = avg_speed_mph

    def run(self, adj_matrix, start_node=0):
        """
        Run the Nearest Neighbor algorithm on a given adjacency matrix starting from a specified node.

        Parameters:
        - adj_matrix (list of lists): A 2D list representing the adjacency matrix where adj_matrix[i][j]
                                      is the distance from node i to node j.
        - start_node (int, optional): The starting node for the tour. Defaults to 0.

        Returns:
        - tuple: A tuple containing the tour (list of nodes visited in order), the total cost of the tour,
                 a list of time traveled between each node, and a list of costs between each node.

        Example usage:
        adj_matrix = [
            [0, 29, 20, 21],
            [29, 0, 15, 17],
            [20, 15, 0, 28],
            [21, 17, 28, 0]
        ]
        tour, cost = nearest_neighbor.run(adj_matrix)
        print(f"Tour: {tour}")
        print(f"Total Cost: {cost}")
        """
        num_nodes = len(adj_matrix)
        unvisited = set(range(num_nodes))
        current_node = start_node
        tour = [current_node]
        time_traveled = [0] # Time traveled between nodes
        total_cost = 0  # Total cost of the tour
        tour_cost = [] # Cost of traveling between nodes

        # Remove the start node from the set of unvisited nodes
        unvisited.remove(current_node)

        # Iterate over unvisited nodes to find the nearest node and traverse to it
        while unvisited:
            # Find the nearest unvisited node
            nearest_node = min(unvisited, key=lambda node: adj_matrix[current_node][node])

            current_cost = adj_matrix[current_node][nearest_node]

            # Update total cost and time traveled
            total_cost += current_cost
            time_traveled.append(current_cost/self.avg_speed_mph)

            # Update the current node and tour tracking
            current_node = nearest_node
            tour.append(current_node)
            tour_cost.append(current_cost)

            # Mark the current node as visited
            unvisited.remove(current_node)

        # Return to the start node to complete the tour
        last_cost = adj_matrix[current_node][start_node]
        total_cost += last_cost
        time_traveled.append(last_cost/self.avg_speed_mph)
        tour.append(start_node)
        tour_cost.append(last_cost)

        # Remove the initial placeholder from time_traveled list
        time_traveled.pop(0)

        return tour, total_cost, time_traveled, tour_cost
