from datetime import datetime, timedelta


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
    arrival_times = [start_time]
    for hop_time in hop_times:
        delta = timedelta(hours=hop_time)
        new_time = arrival_times[-1] + delta
        # print(f"hop_time: {hop_time} delta: {delta} new_time: {get_time_string(new_time)}")
        arrival_times.append(new_time)

    arrival_times_str = [get_time_string(time) for time in arrival_times]
    # arrival_times_str = arrival_times_str[1:]
    return arrival_times, arrival_times_str
