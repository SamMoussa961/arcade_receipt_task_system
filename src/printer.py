from datetime import date
import json

from escpos import printer
from escpos.printer import CupsPrinter, Dummy


def print_template(printer_name, template_file, data):
    printer = None
    try:
        printer = CupsPrinter(printer_name)
        printer.open()

        with open(data, 'r', encoding='utf-8') as data_file:
            receipt_data = json.load(data_file)

        with open(template_file, encoding="utf-8") as template:
            receipt = template.read()

        text = receipt.format(**receipt_data)
        printer.text(text)
        printer.qr("test")
        printer.cut()

    finally:
        if printer:
            printer.close()

def dummy_print_template(data):
    printer = None
    primary_divider = "=" * 48
    secondary_divider = "-" * 48
    body = ''

    try:
        printer = Dummy()

        with open(data, 'r', encoding='utf-8') as data_file:
            receipt_data = json.load(data_file)

        title = receipt_data["title"]
        #date = receipt_data["date"]
        category = receipt_data["category"]
        tasks = receipt_data["tasks"]
        points = receipt_data["points"]
        deadline = receipt_data["deadline"]

        _date = date.today().strftime("%A, %d %M")


        body += primary_divider + '\n'
        body += title + '\n'
        body += secondary_divider + '\n'
        body += _date + '\n'
        body += secondary_divider + '\n'
        body += category + '\n'
        body += secondary_divider + '\n'
        body += tasks + '\n'
        body += ("deadline: " + deadline) + '\n'
        body += secondary_divider + '\n'
        body += ("Possible Score: " + points) + '\n'
        body += secondary_divider + '\n'
        body += "Good Luck" + '\n'
        body += primary_divider + '\n'

        printer.text(body)
        print(printer.output.decode("utf-8"))

    except FileNotFoundError:
        pass

    finally:
        if printer:
            printer.close()

if __name__ == "__main__":
    #print_template("pos", '../print.txt', '../data.json')
    dummy_print_template('../data.json')
