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