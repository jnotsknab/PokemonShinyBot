import datetime
import os

def set_system_time(year, month, day, hour, minute, second):
    # Create a datetime object with the desired date and time
    new_time = datetime.datetime(year, month, day, hour, minute, second)
    
    # Format the date into the required string format (mm-dd-yy)
    formatted_date = new_time.strftime('%m-%d-%y')
    
    # Format the time into the required string format (HH:MM:SS)
    formatted_time = new_time.strftime('%H:%M:%S')
    
    # Set the system date and time using the 'date' and 'time' commands
    os.system(f"date {formatted_date}")
    os.system(f"time {formatted_time}")

