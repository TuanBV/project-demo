"""
Draw PDF Function
"""

import os
import qrcode
import gencbar
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from helpers.common import format_telephone
from textwrap import wrap
import base64

# Draw postcard pdf (BACKSIDE)
# Params:
#   @canvas: Canvas object
#   @customer_data: customer data
#   @act: action data
#   @folder_name: Name of folder print pdf
# Ouput:
#   Return: canvas object
def draw_post_card_pdf(canvas, customer_data, act, shop_mail, folder_name):
  qr_addr = folder_name+"/qr_"
  barcode_addr = folder_name+"/barcode_"
  # Create QR code
  data_qr = " ".join([str(elem) for elem in [customer_data.customers.customer_no, customer_data.customers.shop_no]])
  data_bytes = bytes(data_qr, "ascii")
  data_qr = base64.b64encode(data_bytes)
  qr_code = qrcode.make(data_qr)
  qr_code.save(qr_addr+ customer_data.customers.customer_no +".png")
  qr_image = qr_addr+ customer_data.customers.customer_no +".png"

  # Create Barcode
  gcbar = gencbar.GenCBar()
  barstr = customer_data.customers.address1 + "," + customer_data.customers.address2 + "," + customer_data.customers.address3
  img, barcode = gcbar.create_bar(barstr)
  img.save(barcode_addr+ customer_data.customers.customer_no +".png")
  barcode_image = barcode_addr+ customer_data.customers.customer_no +".png"

  # Fill customer data to pdf file
  # Set font, font size
  pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
  canvas.setFont("HeiseiMin-W3", 12)

  # Draw header of file
  # Draw middle text of header
  canvas.drawString(250, 800, "郵　便　は　が　き")

  # Draw stamping place
  canvas.circle(115, 750, 65)
  canvas.line(53, 770, 177, 770)

  canvas.drawString(90, 750, "料金別納")

  canvas.drawString(95, 730, "郵　便")

  # Draw information of customer place
  canvas.setFont("HeiseiMin-W3", 14)
  canvas.drawRightString(540, 700, "〒"+ (customer_data.customers.zip_code)[0:3] + "-" + (customer_data.customers.zip_code)[3:7])

  line = 680
  wraped_addr_1 = "\n".join(wrap(customer_data.customers.address1, 20))
  array_addr_1 = wraped_addr_1.splitlines()

  for line_text in array_addr_1:
    canvas.drawRightString(555, line, line_text)
    line -= 20

  wraped_addr_2 = "\n".join(wrap(customer_data.customers.address2, 20))
  array_addr_2 = wraped_addr_2.splitlines()

  for line_text in array_addr_2:
    canvas.drawRightString(545, line, line_text)
    line -= 20

  # Check if addressLine3 exist
  if customer_data.customers.address3:
    wraped_addr_3 = "\n".join(wrap(customer_data.customers.address3, 20))
    array_addr_3 = wraped_addr_3.splitlines()
    for line_text in array_addr_3:
      canvas.drawRightString(555, line, line_text)
      line -= 20

    line -= 20
    canvas.drawRightString(555, line, customer_data.customers.last_name + " " + customer_data.customers.first_name + " 様")
  else:
    line -= 20
    canvas.drawRightString(555, line, customer_data.customers.last_name + " " + customer_data.customers.first_name + " 様")

  canvas.setFont("HeiseiMin-W3", 12)
  # Draw qr_code of customer
  canvas.drawImage(qr_image, 30, 420, 130, 130)

  # Draw customerNo
  canvas.drawString(50, 400, "会員No.　" + customer_data.customers.customer_no)

  # Draw barcode of customer address
  canvas.drawImage(barcode_image, 75, 300, 450, 20)

  # Draw information of shop
  canvas.drawString(50, 250, "〒" + (act["shops"]["zip_code"])[0:3]+"-"+(act["shops"]["zip_code"])[3:7])

  line_shop = 235
  addr_shop = act["shops"]["address1"] + act["shops"]["address2"]
  wraped_addr_shop_1 = "\n".join(wrap(addr_shop, 35))
  array_addr_shop_1 = wraped_addr_shop_1.splitlines()

  for line_text in array_addr_shop_1:
    canvas.drawString(50, line_shop, line_text)
    line_shop -= 15

  # Check if addressLine3 exist
  if act["shops"]["address3"]:
    wraped_addr_shop_3 = "\n".join(wrap(act["shops"]["address3"], 35))
    array_addr_shop_3 = wraped_addr_shop_3.splitlines()

    for line_text in array_addr_shop_3:
      canvas.drawString(65, line_shop, line_text)
      line_shop -= 15

    line_shop -= 15
    canvas.drawString(50, line_shop, act["shops"]["corporate_name"])

    line_shop -= 15
    canvas.drawString(50, line_shop, "Tel　："+ format_telephone(act["shops"]["telephone_no"]))

    line_shop -= 15
    canvas.drawString(50, line_shop, "Mail： "+ shop_mail)
  else:
    line_shop -= 15
    canvas.drawString(50, line_shop, act["shops"]["corporate_name"])

    line_shop -= 15
    canvas.drawString(50, line_shop, "Tel　："+ format_telephone(act["shops"]["telephone_no"]))

    line_shop -= 15
    canvas.drawString(50, line_shop, "Mail： "+ shop_mail)
  # Page break
  canvas.showPage()

  if os.path.exists(qr_image):
    os.remove(qr_image)

  if os.path.exists(barcode_image):
    os.remove(barcode_image)

  return canvas


# Draw flyer pdf (BACKSIDE)
# Params:
#   @canvas: Canvas object
#   @customer_data: customer data
# Ouput:
#   Return: canvas object
def draw_flyer_pdf(canvas, customer_data, folder_name):
  qr_addr = folder_name+"/qr_"
  barcode_addr = folder_name+"/barcode_"
  # Create QR code
  data_qr = " ".join([str(elem) for elem in [customer_data.customers.customer_no, customer_data.customers.shop_no]])
  data_bytes = bytes(data_qr, "ascii")
  data_qr = base64.b64encode(data_bytes)
  qr_code = qrcode.make(data_qr)
  qr_code.save(qr_addr+ customer_data.customers.customer_no +".png")
  qr_image = qr_addr+ customer_data.customers.customer_no +".png"

  # Create Barcode
  gcbar = gencbar.GenCBar()
  barstr = customer_data.customers.address1 + "," + customer_data.customers.address2 + "," + customer_data.customers.address3
  img, barcode = gcbar.create_bar(barstr)
  img.save(barcode_addr+ customer_data.customers.customer_no + ".png")
  barcode_image = barcode_addr+ customer_data.customers.customer_no + ".png"

  # Set font, font size
  pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
  canvas.setFont("HeiseiMin-W3", 10)

  # Draw stamp place
  canvas.circle(115, 730, 50)
  canvas.line(69, 750, 161, 750)

  canvas.drawString(95, 730, "料金別納")

  canvas.drawString(100, 710, "郵　便")

  canvas.setFont("HeiseiMin-W3", 10)

  # Draw information of customer place
  canvas.drawString(200, 760, "〒"+ (customer_data.customers.zip_code)[0:3] + "-" + (customer_data.customers.zip_code)[3:7])

  line = 740
  text_addr = customer_data.customers.address1 + " " + customer_data.customers.address2 + " " + customer_data.customers.address3

  wraped_addr_1 = "\n".join(wrap(text_addr, 30))
  array_addr_1 = wraped_addr_1.splitlines()

  for line_text in array_addr_1:
    canvas.drawString(200, line, line_text)
    line -= 10

  canvas.setFont("HeiseiMin-W3", 14)

  canvas.drawCentredString(280, 615, customer_data.customers.last_name + " " + customer_data.customers.first_name + " 様")

  canvas.setFont("HeiseiMin-W3", 10)

  # Draw qr_code of customer
  canvas.drawImage(qr_image, 490, 530, 50, 50)

  canvas.drawString(450, 510, "会員No.　" + customer_data.customers.customer_no)

  # Draw barcode of customer address
  canvas.drawImage(barcode_image, 180, 565, 200, 10)

  if os.path.exists(qr_image):
    os.remove(qr_image)

  if os.path.exists(barcode_image):
    os.remove(barcode_image)

  return canvas
