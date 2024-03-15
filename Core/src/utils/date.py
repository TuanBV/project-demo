"""
Date Function
"""

from datetime import datetime
import helpers.const as env

# Get current time
# Params:
#  @day: date object
#  @type_format: day format
# Output:
#   return: a current time string
def format_date_time(day, type_format):
  date_time_string = day.strftime(type_format)
  return date_time_string


# Get current time OBJECT
# Output:
#  return: an object of current time
def get_current_time_obj():
  time_current = datetime.now(env.TIMEZONE)
  return time_current


# Convert string to date
# Params:
#  @time: date string
#  @type_format: day format
# Output:
#  return: an object of date
def get_object_date(time, type_format):
  date_object = env.TIMEZONE.localize(datetime.strptime(time, type_format))
  return date_object
