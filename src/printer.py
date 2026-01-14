import json
from escpos.printer import CupsPrinter


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


if __name__ == "__main__":
    print_template("pos", "../print.txt", '../data.json')
