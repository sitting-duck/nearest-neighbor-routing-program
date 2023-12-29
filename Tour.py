import TimeUtils


class Tour:
    """
    A class representing a tour or a route taken by a delivery vehicle.

    Attributes:
    - hops (list): A list of nodes (hops) in the tour.
    - hop_times (list): A list of times taken to travel between consecutive hops.
    - total_cost (float): The total cost associated with the tour.
    - tour_cost (list): A list of costs associated with traveling between consecutive hops.
    - start_time (datetime): The start time of the tour.
    - avg_speed_mph (float): The average speed in miles per hour for the tour.
    """
    def __init__(self, hops, hop_times, total_cost, tour_cost, start_time):
        """
        Initialize a Tour object with tour details.

        Parameters:
        - hops (list): List of nodes (hops) in the tour.
        - hop_times (list): Times taken to travel between consecutive hops.
        - total_cost (float): Total cost of the tour.
        - tour_cost (list): Costs associated with traveling between consecutive hops.
        - start_time (datetime): Start time of the tour.
        """

        self.hops = hops
        self.hop_times = hop_times
        self.total_cost = total_cost
        self.tour_cost = tour_cost
        self.start_time = start_time
        self.avg_speed_mph = 18

    def get_mileage_at_time(self, query_time):
        """
        Calculate the mileage of the tour at a specific query time.

        Parameters:
        - query_time (datetime): The time at which the mileage is to be calculated.

        Returns:
        - float: The mileage of the tour at the given query time.
        """

        # if the tour hasn't started yet, then there are no miles on it to return
        if query_time < self.start_time:
            return 0

        current_mileage = 0
        current_cost = 0
        current_time = self.start_time
        for i in range(len(self.hop_times)):
            current_time = TimeUtils.get_time_plus_hours(current_time, self.hop_times[i])
            if query_time > current_time:
                current_mileage += self.tour_cost[i]
            else:
                # now we start at current hop time and add the mileage per hour until we reach the query time
                time_diff = current_time - query_time
                # Convert timedelta to hours (as a float)
                hours_diff = time_diff.total_seconds() / 3600
                current_mileage += hours_diff * self.avg_speed_mph
                break
        return current_mileage

    def get_total_mileage(self):
        """
        Calculate the total mileage of the tour.

        Returns:
        - float: The total mileage of the tour.
        """
        current_mileage = 0
        for i in range(len(self.hop_times)):
            current_mileage += self.tour_cost[i]
        return current_mileage
