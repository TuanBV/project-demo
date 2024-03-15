"""
Service mana utils
"""

# Get list action of month
# Params:
#   @list_action: Data action
# Output:
#   Return: Data action group by month
def get_act_of_month(list_action):
  data_act_monthly = []
  for item in list_action:
    dct = {"action_type": item["action_type"], "delivery_time": item["delivery_time"][0:10]}
    if dct not in data_act_monthly:
      data_act_monthly.append(dct)

  return data_act_monthly


# Create action calendar
# Params:
#   @action_by_month: Data action by month
#   @list_action: Data action
# Output:
#   Return: Data calendar of action
def create_act_calendar(action_by_month, list_action):
  calendar_action = []
  for item in action_by_month:
    row = {}
    for act in list_action:
      if act["delivery_time"][5:7] == item["month"]["value"] and act["action_types"] not in item["action_type"]:
        item["action_type"].append(act["action_types"])
    row["month"] = item["month"]["value"]
    row["year"] = item["month"]["full_date"][0:4]
    row["action_type"] = item["action_type"]
    calendar_action.append(row)

  return calendar_action
