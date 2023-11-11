import TimeUtils


class Tour:
    def __init__(self, hops, hop_times, total_cost, tour_cost, start_time):
        self.hops = hops
        self.hop_times = hop_times
        self.total_cost = total_cost
        self.tour_cost = tour_cost
        self.start_time = start_time
        self.avg_speed_mph = 18

    def get_mileage_at_time(self, query_time):

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
        current_mileage = 0
        for i in range(len(self.hop_times)):
            current_mileage += self.tour_cost[i]
        return current_mileage

    def __lt__(self, other):
        return self.hop_times[0] < other.hop_times[0]
