from datetime import date
import json
from escpos.printer import CupsPrinter, Dummy


def print_template(data, printer_name=None):
    printer = None
    primary_divider = "=" * 48
    secondary_divider = "-" * 48
    body = ''
    try:
        if printer_name:
            printer = CupsPrinter(printer_name)
        else:
            printer = Dummy()

        #profile = printer.profile()

        printer.open()

        with open(data, 'r', encoding='utf-8') as data_file:
            receipt_data = json.load(data_file)

        title = receipt_data["title"]
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
        printer.qr("test")
        printer.cut()

    finally:
        if printer:
            printer.close()


if __name__ == "__main__":
    print_template('../data.json')
