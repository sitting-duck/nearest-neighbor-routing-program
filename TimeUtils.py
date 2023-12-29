from datetime import datetime, timedelta

def get_time_plus_hours(time, hours):
    """
    time: a datetime object
    hours: an integer representing the number of hours to add to the time
    """
    return time + timedelta(hours=hours)
def get_time(str):
    """
    str: a string in the format: "9:00am", "5:30pm" etc. Use civilian time and am/pm, not military time.
    Once you have datetime objects, you can easily compare them using standard comparison operators (<, >, ==, etc.).
    """
    time_format = "%I:%M%p"
    time = datetime.strptime(str, time_format)
    return time


def get_time_string(time):
    """
    Convert a datetime object to a string representation of the time in the format "9:00am", "5:30pm", etc.

    Parameters:
    - time (datetime): A datetime object representing the time.

    Returns:
    - str: A string representation of the provided time in the format "HH:MMam/pm".
    """
    time_format = "%I:%M%p"
    return time.strftime(time_format)


def input_valid_time():
    """
    Prompt the user to enter a valid time and keep asking until a valid time is provided.
    Return the datetime object representing the time.
    """
    while True:
        user_time = input("Enter the time in the format (e.g., '9:00am', '5:30pm'): ")
        try:
            valid_time = get_time(user_time)
            return valid_time
        except ValueError:
            print("Invalid time format. Please enter the time in the specified format.")

def get_arrival_times(hop_times, start_time):
    """
    Calculate the arrival times at each hop in a delivery route.

    This function takes a list of times (in hours) between each hop in the delivery route and a start time,
    then calculates the arrival time at each subsequent hop.

    Parameters:
    - hop_times (list of float): A list where each element represents the time taken to travel from one hop to the next.
    - start_time (datetime): The time when the journey starts.

    Returns:
    - tuple: A tuple containing two lists:
        1. arrival_times (list of datetime): The arrival times at each hop in the route.
        2. arrival_times_str (list of str): The string representations of the arrival times.

    Example usage:
        hop_times = [1.5, 0.75, 2.25]  # times in hours
        start_time = datetime.datetime(2021, 1, 1, 8, 0, 0)  # 8 AM on Jan 1, 2021
        arrival_times, arrival_times_str = get_arrival_times(hop_times, start_time)
    """

    # Initialize the list of arrival times with the start time
    arrival_times = [start_time]

    # Loop through each hop time and calculate the arrival time for each hop
    for hop_time in hop_times:
        delta = timedelta(hours=hop_time) # Convert hop time to a timedelta object
        new_time = arrival_times[-1] + delta # Calculate the new time by adding the delta to the last time
        # print(f"hop_time: {hop_time} delta: {delta} new_time: {get_time_string(new_time)}")
        arrival_times.append(new_time)

    # Convert the datetime objects to their string representations
    arrival_times_str = [get_time_string(time) for time in arrival_times]

    # Return the list of datetime objects and their string representations
    return arrival_times, arrival_times_str
