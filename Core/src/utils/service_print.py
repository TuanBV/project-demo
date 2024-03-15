"""
Service print utils
"""

from datetime import timedelta
from utils.date import format_date_time, get_current_time_obj, get_object_date
from helpers import kbn
from sqlalchemy import desc, asc
from models import ActionDetails, Actions, ActionTypes


# Sort data action by deadline with days_for_print
# Params:
#   @result_action_details: Data action details
#   @sort_type: Sort type
# Output:
#   Return: Data action details
def sort_data_by_deadline(result_action_details, sort_type):
  # Check data length
  # Sort by deadline
  for item_actions in result_action_details["item"]:
    # Get days_for_printing of shop
    dead_line = get_current_time_obj() + timedelta(days=int(item_actions["shops"]["days_for_printing"]))

    item_actions["flag_check_deadline"] = False
    # Action not reach deadline and status is NOT SEND
    if (get_object_date(item_actions["action_details"]["delivery_time"], "%Y/%m/%d %H:%M") <= dead_line
        and item_actions["action_details"]["print_status"] == kbn.PrintStatus.CONFIRM.value):
      item_actions["flag_check_deadline"] = True

  # sort_type empty
  if sort_type == "":
    # Data will sort by deadline
    result_action_details["item"] = sorted(result_action_details["item"], key=lambda item: item["flag_check_deadline"], reverse=True)

  return result_action_details


# Set sort value
# Params:
#   @sort_key: Sort key
#   @sort_type: Sort type
# Output:
#   Return: Sort value
def set_sort_value(sort_key, sort_type):
  column_name = ActionDetails.created_date

  # Set sort_key
  if sort_key == "act_type_name":
    column_name = ActionTypes.name
  elif sort_key == "action_name":
    column_name = Actions.name
  elif sort_key != "":
    column_name = ActionDetails.__table__.c[sort_key]

  if sort_type not in ["asc", "desc"]:
    sort_type = "desc"

  # Set query sort
  if sort_type == "asc":
    sort_value = asc(column_name)
  else:
    sort_value = desc(column_name)

  return sort_value


# Prepare list data
# Params:
#   @data_query_action_details: Data action detail
# Output:
#   Return: List data action
def prepare_list_data(data_query_action_details):
  data_action = []
  for item in data_query_action_details:
    item.action_details.delivery_time = format_date_time(item.action_details.delivery_time, "%Y/%m/%d %H:%M")
    data = {
      "actions": item.actions.__dict__,
      "action_details": item.action_details.__dict__,
      "action_types": item.action_types.__dict__,
      "shops": item.shops.__dict__
    }
    data_action.append(data)

  return data_action
