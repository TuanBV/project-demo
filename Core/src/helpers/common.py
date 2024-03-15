# pylint: disable=broad-except
"""
Common function
"""

from copy import deepcopy
import platform
import os
import uuid
import boto3
import fitz
import helpers.const as env
from helpers import kbn
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from reportlab.pdfgen import canvas
from utils.date import (format_date_time, get_current_time_obj, get_object_date)
import time as time_
from fastapi.encoders import jsonable_encoder


# Add action store and sort list
# Params:
#   @lst_action: Data list action
#   @act_store: Visit store
#   @lst_point: Data list point
# Output:
#   return: List data sorted
def sort_list_action(lst_action, act_store, lst_point):
  for item in lst_point:
    item["action_types"] = act_store
    item["action_type_id"] = act_store["id"]
    item["delivery_time"] = item["changed_date"]
    item["action_type"] = act_store["name"]

  result = lst_action
  result.extend(lst_point)

  # Sort list by delivery_time
  data_sorted = sorted(result, key=lambda x: x["delivery_time"], reverse=True)
  return data_sorted


# Sort data
# Params:
#   @data: list data
#   @key: property to sort
#   @sort_type: sort type(ASC or DESC)
# Output:
#   return: data sorted
def sort_data(data, key, sort_type):
  reverse = False
  # Set sort type
  if sort_type == "desc":
    if key == "rank":
      reverse = False
    else:
      reverse = True
  elif sort_type == "asc":
    if key == "rank":
      reverse = True
    else:
      reverse = False
  # Case sort by action type name
  if key == "actionTypeName":
    data_sorted = sorted(
        data, key=lambda x: x["actionType"][key], reverse=reverse)
  # Case sort by age
  elif key == "age":
    data_sorted = sorted(
        data, key=lambda x: int(x[key]), reverse=reverse)
  # Default
  else :
    data_sorted = sorted(
        data, key=lambda x: x[key], reverse=reverse)

  return data_sorted


# Get Member's seniority
# Params:
#   @data: register date of member
#   @now: Current time
# Output:
#   return: Member's seniority
def member_history(data, now = None):
  if now is None:
    now = get_current_time_obj()

  # check registerDate == ""
  if data == "":
    return "0日"

  # registerDate != ""
  now_format =get_object_date(str(now)[0:10].replace("-", "/"), "%Y/%m/%d")
  time_data = get_object_date(data, "%Y/%m/%d")
  period = relativedelta(now_format, time_data)
  result = ""
  # In case the account was created in the current day
  if period.years > 0:
    result = str(period.years) + "年"
    if period.months > 0:
      result += str(period.months) + "か月"
  else:
    # In case the account creation history is less than 3 months
    if period.months >= 3:
      result = str(period.months) + "か月"
    else:
      # Calculate day
      process = abs(now_format-time_data).days
      # In case the number of days is greater than or equal to 90
      if process >= 90:
        result = "3か月"
      else:
        result = str(process) + "日"

  return result


# Calculate age of customer
# Params:
#   @data: birthday of customer
#   @date_now: Current time
# Output:
#   return: age of customer
def age(data, date_now = None):
  if date_now is None:
    date_now = get_current_time_obj().strftime("%Y/%m/%d")

  # pass customer's birthday
  # if current month is greater than birth month
  # and current date is greater than birthday
  data_number= int(data[5:10].replace("/", ""))
  date_now_number = int(date_now[5:10].replace("/", ""))

  if int(date_now[0:4]) <= int(data[0:4]):
    return "0"
  age_customer = int(date_now[0:4]) - int(data[0:4])
  age_customer = age_customer if date_now_number >= data_number else age_customer -1

  return str(age_customer)


# Get days of between 2 dates
# Params:
#   @data: date
# Output:
#   return: days of between 2 dates
def get_days_between_dates(data, now = None):
  if now is None:
    now = get_current_time_obj()

  # calculate number of days
  if data != "":
    y = int(data[0:4])
    m = int(data[5:7])
    d = int(data[8:10])
    date_convert = date(y, m, d)
    result = int(abs(now.date() - date_convert).days)
  else:
    result = 0

  return result


# Convert gender to string
# Params:
#   @data: data gender
# Output:
#   return: text of gender
def gender(data):
  result = ""
  for sex_type in kbn.GENDER.items():
    if sex_type[1].value == data:
      result = sex_type[1].text

  return result


# Setting rank for customer
# Params:
#   @rank: rank of customer  now
#   @data: data customer
#   @setting_rank: setting_rank of shop
# Output:
#   return: rank of customer
def convert_rank(data, setting_rank):
  result = kbn.Rank.BLANK.value
  range_date = f'{setting_rank["range_date"]}'
  # Setting rank by amount
  if setting_rank["kbn"] == kbn.SettingRankKbn.AMOUNT.value and setting_rank["range_date"] != 0:
    if int(data["amount"][range_date]) >= int(setting_rank["rank_s"]):
      result = kbn.RANK_CUSTOMER.RANK_S

    elif int(data["amount"][range_date]) >= int(setting_rank["rank_a"]):
      result = kbn.RANK_CUSTOMER.RANK_A

    elif int(data["amount"][range_date]) >= int(setting_rank["rank_b"]):
      result = kbn.RANK_CUSTOMER.RANK_B

    elif int(data["amount"][range_date]) >= int(setting_rank["rank_c"]):
      result = kbn.RANK_CUSTOMER.RANK_C

  # Setting rank by visit store
  elif setting_rank["kbn"] == kbn.SettingRankKbn.VISIT.value and setting_rank["range_date"] != 0:
    # check rank by amount
    if int(data["visit"][range_date]) >= int(setting_rank["rank_s"]):
      result = kbn.RANK_CUSTOMER.RANK_S
    elif int(data["visit"][range_date]) >= int(setting_rank["rank_a"]):
      result = kbn.RANK_CUSTOMER.RANK_A

    elif int(data["visit"][range_date]) >= int(setting_rank["rank_b"]):
      result = kbn.RANK_CUSTOMER.RANK_B

    elif int(data["visit"][range_date]) >= int(setting_rank["rank_c"]):
      result = kbn.RANK_CUSTOMER.RANK_C

  return result


# Generate list time weekly
# Params:
#   @loop_type: Rule of loop
#   @date_time_obj: Delivery full time
#   @date_only_obj: Delivery date
#   @weekly_number_add: Weekly number
# Output:
#   return: list time weekly of delivery action
def loop_weekly(loop_type, date_time_obj, date_only_obj, weekly_number_add):
  list_day_action_return = []
  # Loop weekly default
  # if have end date
  if loop_type["until"] != "":
    until_date_obj = get_object_date(loop_type["until"], "%Y/%m/%d")

    # compare dateSubmit and end date
    while date_only_obj <= until_date_obj:
      # add day to list
      list_day_action_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))
      # add 1 week to dateSubmit for next compare
      date_only_obj += timedelta(weeks=weekly_number_add)
      date_time_obj += timedelta(weeks=weekly_number_add)

  # if have number of repeat
  elif loop_type["count"] != "":
    count = int(loop_type["count"])
    i = 0

    # compare number of repetitions and index
    while i < count:
      # add day to list
      list_day_action_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))
      # add 1 week to dateSubmit
      date_time_obj += timedelta(weeks=weekly_number_add)
      i += 1
  # End loop weekly
  return list_day_action_return


# Loop type until a date
# Params:
#   @loop_type: Data loop
#   @date_time_obj: Object datetime
#   @date_only_obj: Object date
#   @monthly_number_add: Number of loop
# Output:
#   Return: List day of loop
def loop_until(loop_type, date_time_obj, date_only_obj, monthly_number_add):
  list_day_loop_return = []
  until_date_obj = get_object_date(loop_type["until"], "%Y/%m/%d")
  days_loop = date_only_obj.day
  # compare dateSubmit and end date
  while date_only_obj <= until_date_obj:
    if loop_type["interval"] == "" and loop_type["by_day"] == "":
      # add day to list
      list_day_loop_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))
      date_time_obj += relativedelta(months=monthly_number_add)

    elif loop_type["interval"] != "" and loop_type["by_day"] == "":
    # get day of dateSubmit
      days_next_month = monthrange(date_only_obj.year,date_only_obj.month)[1]
      # if day in dateSubmit <= last day in next month
      if days_loop <= days_next_month:
        # format this day and add to list
        day_add = datetime(date_only_obj.year, date_only_obj.month, days_loop).strftime("%Y/%m/%d %H:%M:%S")
        list_day_loop_return.append(day_add)

    elif loop_type["interval"] == "" and loop_type["by_day"] == "Lastofmonth":
      last_day_of_month = monthrange(date_only_obj.year,date_only_obj.month)[1]

      date_time_obj = date_time_obj.replace(day=last_day_of_month)
      list_day_loop_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))

      # add 1 month to dateSubmit for next compare
      date_time_obj += relativedelta(months=monthly_number_add)

    # add months by interval to dateSubmit for next compare
    date_only_obj += relativedelta(months=monthly_number_add)
  return list_day_loop_return


# Loop type count
# Params:
#   @loop_type: Data loop
#   @date_time_obj: Object datetime
#   @date_only_obj: Object date
#   @monthly_number_add: Number of loop
# Output:
#   Return: List day of loop
def loop_count(loop_type, date_time_obj, date_only_obj, monthly_number_add):
  list_day_loop_return = []
  count = int(loop_type["count"])
  i = 0
  days_loop = date_only_obj.day
  # compare number of repetitions and index
  while i < count:
    if loop_type["interval"] == "" and loop_type["by_day"] == "":
      # add day to list
      list_day_loop_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))

    elif loop_type["interval"] != "" and loop_type["by_day"] == "":
      days_next_month = monthrange(date_time_obj.year, date_time_obj.month)[1]

      # if day in dateSubmit <= last day in next month
      if days_loop <= days_next_month:
        # format this day and add to list
        day_add = datetime(date_time_obj.year,
          date_time_obj.month, days_loop,
          date_time_obj.hour,
          date_time_obj.minute).strftime("%Y/%m/%d %H:%M:%S")

        list_day_loop_return.append(day_add)

    elif loop_type["interval"] == "" and loop_type["by_day"] == "Lastofmonth":
      last_day_of_month = monthrange(date_time_obj.year, date_time_obj.month)[1]

      date_time_obj = date_time_obj.replace(day=last_day_of_month)

      # add day to list
      list_day_loop_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))

    # add 1 month to dateSubmit
    date_time_obj += relativedelta(months=monthly_number_add)
    i += 1
  return list_day_loop_return


# Generate list time Monthly
# Params:
#   @loop_type: Rule of loop
#   @date_time_obj: Delivery full time
#   @date_only_obj: Delivery date
#   @monthly_number_add: Monthly number
# Output:
#   return: list time Monthly of delivery action
def loop_monthly(loop_type, date_time_obj, date_only_obj, monthly_number_add):
  list_day_action_return = []
  # Loop monthly default
  # if have end date
  if loop_type["until"] != "":
    list_time_until = loop_until(loop_type, date_time_obj, date_only_obj, monthly_number_add)
    list_day_action_return += list_time_until

  # if have number of repeat
  if loop_type["count"] != "":
    list_time_count = loop_count(loop_type, date_time_obj, date_only_obj, monthly_number_add)
    list_day_action_return += list_time_count

  return list_day_action_return


# Generate list time year
# Params:
#   @loop_type: Rule of loop
#   @date_time_obj: Delivery full time
#   @date_only_obj: Delivery date
#   @year_number_add: year number
# Output:
#   return: list time year of delivery action
def loop_year(loop_type, date_time_obj, date_only_obj, year_number_add):
  list_day_action_return = []
  # if have end date
  if loop_type["until"] != "":
    until_date_obj = get_object_date(loop_type["until"], "%Y/%m/%d")

    # compare dateSubmit and end date
    while date_only_obj <= until_date_obj:
      # add day to list
      list_day_action_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))

      # add year by interval to dateSubmit for next compare
      date_only_obj += relativedelta(years=int(year_number_add))
      date_time_obj += relativedelta(years=int(year_number_add))

  # if have number of repeat
  if loop_type["count"] != "":
    count = int(loop_type["count"])
    i = 0

    # compare number of repetitions and index
    while i < count:
      # add day to list
      list_day_action_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))
      date_time_obj += relativedelta(years=int(year_number_add))
      i += 1
  return list_day_action_return


# Generate list time daily
# Params:
#   @loop_type: Rule of loop
#   @date_time_obj: Delivery full time
#   @date_only_obj: Delivery date
#   @daily_number_add: daily number
# Output:
#   return: list time daily of delivery action
def loop_daily(loop_type, date_time_obj, date_only_obj, daily_number_add):
  list_day_action_return = []
  # if have end date
  if loop_type["until"] != "":
    until_date_obj = get_object_date(loop_type["until"], "%Y/%m/%d")

    # compare dateSubmit and end date
    while date_only_obj <= until_date_obj:
      # add day to list
      list_day_action_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))

      # add day by interval for next compare
      date_only_obj += timedelta(days=int(daily_number_add))
      date_time_obj += timedelta(days=int(daily_number_add))

  # if have number of repeat
  if loop_type["count"] != "":
    count = int(loop_type["count"])
    i = 0

    # compare number of repetitions and index
    while i < count:
      # add day to list
      list_day_action_return.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))

      # add day by interval to dateSubmit
      date_time_obj += timedelta(days=int(daily_number_add))
      i += 1
  return list_day_action_return


# Generate list dates send action
# Params:
#   @loop_type: Rule of loop
#   @date_submit: Delivery time
# Output:
#   return: list dates of delivery action
def list_day_delivery(loop_type, date_submit):
  arr_date = date_submit.split()
  date_only = arr_date[0]
  date_only_obj = get_object_date(date_only, "%Y/%m/%d")
  date_time_obj = get_object_date(date_submit, "%Y/%m/%d %H:%M:%S")
  list_day_action = []
  interval_number_add = int(loop_type["interval"]) if loop_type["interval"] != "" else 1

  # Loop none
  if loop_type["freq"] == "":
    list_day_action.append(date_time_obj.strftime("%Y/%m/%d %H:%M:%S"))

  # Loop daily custom
  if loop_type["freq"] == "Daily" and loop_type["interval"] != "":
    list_time_daily = loop_daily(loop_type, date_time_obj, date_only_obj, interval_number_add)
    list_day_action += list_time_daily
  # End loop daily custom
  if loop_type["freq"] == "Weekly":
    list_time_weekly = loop_weekly(loop_type, date_time_obj, date_only_obj, interval_number_add)
    list_day_action += list_time_weekly
  # Loop weekly
  # Loop monthly
  if loop_type["freq"] == "Monthly":
    list_time_monthly = loop_monthly(loop_type, date_time_obj, date_only_obj, interval_number_add)
    list_day_action += list_time_monthly
  # End loop monthly

  # Loop yearly custom
  if loop_type["freq"] == "Yearly" and loop_type["interval"] != "":
    list_time_year = loop_year(loop_type, date_time_obj, date_only_obj, interval_number_add)
    list_day_action += list_time_year
  # End loop yearly custom

  return list_day_action


# Generate list month
# Params:
#   @month_start: month start
# Output:
#   return: list 12 month
def generate_calendar(month_start):
  # create year calendar by time
  date_from = month_start + "/01"
  obj_date_from = get_object_date(date_from, "%Y/%m/%d")
  obj_date_to = obj_date_from + relativedelta(months=12)
  result = []

  while obj_date_from < obj_date_to:
    result.append({"value": obj_date_from.strftime("%Y/%m/%d %H:%M")[5:7],
      "full_date": obj_date_from.strftime("%Y/%m/%d %H:%M")[:7]})

    obj_date_from += relativedelta(months=1)

  return result


# Format Zipcode
# Params:
#   @zipcode: Zipcode
# Output:
#   return: zipcode
def format_zipcode(zipcode):
  return zipcode[:3] + "-" + zipcode[3:]


# History of change password
# Params:
#   @day_change_pw: date of change password
#   @time_current: date now
# Output:
#   return: days of change password passed
def change_pw_history(day_change_pw, time_current):
  # Check day_change_pw
  if day_change_pw == "":
    return "0日"

  format_date = "%Y/%m/%d"

  # Format current time to Object
  time_current_format = get_object_date(time_current, format_date)

  # Get day of current day
  time_current_day = time_current_format.day

  # Format day_change_pw to Object
  day_change_pw_format = get_object_date(day_change_pw, format_date)

  # Get day of change_pw
  day_change_pw_day = day_change_pw_format.day

  # Calculate range of 2 timelines
  period = relativedelta(time_current_format, day_change_pw_format)

  result = ""
  if period.years == 0:
    # Set result is number of day
    result=str(period.days) + "日"
    # Period < day of 3 months
    if period.months < 3:
      # Calculate range of 2 timelines and get days
      process = abs(day_change_pw_format-time_current_format).days

      # Set result is 3 month
      if time_current_day==day_change_pw_day or process >= 90:
        result = "3か月"
      else:
        # Set result is number of day
        result = str(process) + "日"

    # period >= day of 3 month
    elif period.months != 0:
      # Set result is number of month
      result = str(period.months) + "か月"

  else:
    if period.months != 0:
      # Set result are number of year and number of month
      result = str(period.years) + "年" + str(period.months) + "か月"
    else:
      # Set result is number of year
      result = str(period.years) + "年"

  return result


# check data point customer
# Params:
#   @data_point_customer: data point default
#   @date_now: date now
#   @format_date: date format
#   @list_point: list data point
# Output:
#   return: data point customer has process
def check_data_point_customer(data_point_customer, date_now, format_date, list_point):
  now = date_now.strftime(format_date)
  one_month = (date_now + relativedelta(months=-1)).strftime(format_date)
  three_month = (date_now + relativedelta(months=-3)).strftime(format_date)
  six_month = (date_now + relativedelta(months=-6)).strftime(format_date)
  twelve_month = (date_now+ relativedelta(months=-12)).strftime(format_date)

  for item in list_point:
    data_point_customer["total_visit"] += 1
    data_point_customer["total_amount"] += item["payment"]
    data_point_customer["points"] += item["points"]
    if now >= item["changed_date"]:
      if one_month <= item["changed_date"]:
        data_point_customer["one_visits"] += 1
        data_point_customer["one_amount"] += int(item["payment"])

      if three_month <= item["changed_date"]:
        data_point_customer["three_visits"] += 1
        data_point_customer["three_amount"] += int(item["payment"])

      if six_month <= item["changed_date"]:
        data_point_customer["six_visits"] += 1
        data_point_customer["six_amount"] += int(item["payment"])

      if twelve_month <= item["changed_date"]:
        data_point_customer["twelve_visits"] += 1
        data_point_customer["twelve_amount"] += int(item["payment"])

  return data_point_customer

# Calculate amount and visit store
# Params:
#   @list_point: data point histories
#   @rank: rank
#   @rank_kbn: rank kbn
#   @setting_rank: Data setting rank
#   @date_now: Current time
# Output:
#   return: amount and number of visit store
def calculate_amount_and_visit(list_point, rank, rank_kbn, setting_rank, date_now = None):
  if date_now is None:
    date_now = get_current_time_obj()

  # check data point customer
  data_point_customer = {
    "one_amount": 0,
    "three_amount": 0,
    "six_amount": 0,
    "twelve_amount": 0,
    "one_visits": 0,
    "three_visits": 0,
    "six_visits": 0,
    "twelve_visits": 0,
    "total_amount": 0,
    "points": 0,
    "total_visit": 0,
  }

  if list_point:
    data_point_customer = check_data_point_customer(data_point_customer, date_now, env.FORMAT_DATE, list_point)

  # calculate rank customer
  rank_customer = rank
  if rank_kbn == kbn.RankKBN.YES.value:
    # rank by setting shop
    data_customer = {
      "visit": {
          "1": str(data_point_customer["one_visits"]),
          "2": str(data_point_customer["three_visits"]),
          "3": str(data_point_customer["six_visits"]),
          "4": str(data_point_customer["twelve_visits"]),
          "5": data_point_customer["total_visit"],
      },
      "amount": {
          "1": str(data_point_customer["one_amount"]),
          "2": str(data_point_customer["three_amount"]),
          "3": str(data_point_customer["six_amount"]),
          "4": str(data_point_customer["twelve_amount"]),
          "5": data_point_customer["total_amount"],
      },
    }

    rank_customer = convert_rank(data_customer, jsonable_encoder(setting_rank))

  data_return = {
    "customer": {
      "rank": rank_customer,
      "points": data_point_customer["points"],
      "total_amount": data_point_customer["total_amount"],
      "total_visits": data_point_customer["total_visit"]
    },
    "customer_informations": {
      "amount_1_month" : data_point_customer["one_amount"],
      "amount_3_month" : data_point_customer["three_amount"],
      "amount_6_month" : data_point_customer["six_amount"],
      "amount_12_month" : data_point_customer["twelve_amount"],
      "visited_1_month" : data_point_customer["one_visits"],
      "visited_3_month" : data_point_customer["three_visits"],
      "visited_6_month" : data_point_customer["six_visits"],
      "visited_12_month" : data_point_customer["twelve_visits"]
    }
  }

  return data_return


# Calculate list color by action type
# Params:
#   @list_act_type: list action type
#   @result_action_type: list data action type
# Output:
#   return: list color
def get_list_corlor_by_action_type(list_act_type, result_action_type):
  data_action_type_return = []
  for act_type in result_action_type:
    # If have same color will set orderKbn
    if act_type["id"] in list_act_type:
      order_kbn = act_type["sort_order_no"]

      action_type = {
        "color": act_type["color"],
        "order": order_kbn
      }

      # Add color to list if list not have this color
      if action_type not in data_action_type_return:
        data_action_type_return.append(action_type)
  return data_action_type_return


# Calculate action by month
# Params:
# Output:
#   return: list action
def calculate_action_by_month(list_act_delivery_by_customer_no, data_month, result_action_type):
  list_action = []
  for ful_month in data_month:
    # Filter data action by month
    data_filtered= list(filter(
      lambda row, month=ful_month["full_date"][5:7], year=ful_month["full_date"][:4] :
      (month == str(row["delivery_time"][5:7]))
      and (year == str(row["delivery_time"][0:4])), list_act_delivery_by_customer_no))

    # group actions by color
    data_action_type = []
    list_act_type = []

    for act in data_filtered:
      if act["action_types"]["id"] not in list_act_type:
        list_act_type.append(act["action_types"]["id"])

    list_color = get_list_corlor_by_action_type(list_act_type, result_action_type)
    data_action_type += list_color

    # Sort color by order column
    data_action_type = sort_data(data_action_type, "order", "asc")

    list_action.append({"month": deepcopy(ful_month), "action_type": data_action_type})

  return list_action


# Format telephone no
# Params:
#   @telephone: telephone no
# Output:
#   return: telephone no
def format_telephone(telephone):
  if len(telephone) == 10:
    return telephone[0:2]+"-"+telephone[2:6]+"-"+telephone[6:10]

  if len(telephone) == 11:
    return telephone[0:3]+"-"+telephone[3:7]+"-"+telephone[7:11]


# Output log check performance
# Params:
#   @process_description: description of process
#   @stop: stop time
#   @start: start time
# Output:
#   return: telephone no
def insert_log(process_description, stop, start):
  print(f"{process_description} elapsed time during: {str(stop-start)} ns")


# Create pdf thumbnail function
# Params:
#   @file_name_pdf: name of pdf file in s3
#   @file_name_thumb: name of thumbnail file
#   @directory: link folder in s3
# Output:
#   return: full name of thumbnail file in s3
def create_pdf_thumbnail(file_name_pdf, file_name_thumb, directory):
  try:
    # Create thumbnail of pdf
    pdf_file = "pdf_file.pdf"
    thumbnail_file = "thumbnail.png"
    canvas.Canvas(pdf_file)
    canvas.Canvas(thumbnail_file)
    s3 = boto3.resource("s3")
    s3.meta.client.download_file(env.S3.BUCKET.NAME, directory + file_name_pdf, pdf_file)
    doc = fitz.open(pdf_file)
    # Get first page
    page = doc.load_page(0)
    mat = fitz.Matrix(0.5, 0.5)
    pix = page.get_pixmap(matrix = mat)
    # Save data of image
    pix.save(thumbnail_file)
    doc.close()

    # Send to s3
    open_thumb_file = open(thumbnail_file, "rb")
    full_name_file = file_name_thumb + str(time_.time()) + ".png"
    obj = s3.Object(env.S3.BUCKET.NAME, directory + full_name_file)
    obj.put(Body=open_thumb_file, ContentType="images/png")
    open_thumb_file.close()

    # Remove file in folder
    if os.path.exists(pdf_file):
      os.remove(pdf_file)
    if os.path.exists(thumbnail_file):
      os.remove(thumbnail_file)
  except Exception as e:
    # Remove file in folder
    if os.path.exists(pdf_file):
      os.remove(pdf_file)
    if os.path.exists(thumbnail_file):
      os.remove(thumbnail_file)
    raise e

  return full_name_file


# Generate request id
# Output:
#   return: request id
def get_request_id():
  return uuid.uuid1()


# Generate log
# Params:
#   @level: log level
#   @user_agent: user agent request
#   @url: url request
#   @request_id: request id
#   @log_type: type request
#   @method: request method
#   @content: content log
#   @time: time log
# Output:
#   return: Output log
def generate_log(level="INFO", user_agent="", url="", request_id="", log_type="", method="", content="", time="", user_id="", shop_no="", role=""):
  log = {
        "ec2_name": platform.node(),
        "process_id": os.getpid(),
        "logName": "CRM",
        "type": log_type,
        "request_id": request_id,
        "url": url,
        "user_agent": user_agent,
        "method": method,
        "level": level,
        "message": content,
        "user_id": user_id,
        "shop_no": shop_no,
        "role": role,
  }
  if log_type == "RESPONSE":
    log["response_time"] = format_date_time(time, "%Y/%m/%d %H:%M:%S")
  elif log_type == "REQUEST":
    log["request_time"] = format_date_time(time, "%Y/%m/%d %H:%M:%S")
  else:
    log["time"] = format_date_time(time, "%Y/%m/%d %H:%M:%S")
  return log


# Convert print status of action to text
# Params:
#   @print_status: Print status
# Output:
#   return: Text of print status
def convert_code_print_status(print_status):
  result = ""
  for text_status in kbn.PRINT_STATUS.items():
    if text_status[1].value == print_status:
      result = text_status[1].text

  return result
