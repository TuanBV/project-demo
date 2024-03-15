"""
Csv utils
"""

import csv
import os
from utils.aws import upload_file_to_s3
from core import get_logger

logger = get_logger()

# Write data csv file
# Params:
#   @header_csv: Header of column
#   @rows: Data row
#   @file_name: File name
#   @directory: Directory of file
#   @content_type: File type
#   @encoding: Encoding type
# Output:
#   return: Path file in s3
def write_data_csv_file(header_csv, rows, file_name, directory, content_type, encoding=None):
  try:
    # Write data to csv file
    with open(f"{file_name}", "w", newline="", encoding="Shift_JIS", errors="replace") as f:
      write = csv.writer(f)
      write.writerow(header_csv)
      write.writerows(rows)

    s3_file_key = upload_file_to_s3(file_name, open(f"{file_name}", "rb"), directory, content_type, encoding)
    return s3_file_key

  except Exception as e:
    logger.info("Error create csv file")
    raise e

  finally:
    # Delete csv file
    if os.path.exists(f"{file_name}"):
      os.remove(f"{file_name}")
