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
    time_format = "%I:%M%p"
    return time.strftime(time_format)