from datetime import date
import json
from escpos.printer import CupsPrinter, Dummy
from PIL import Image, ImageDraw, ImageFont


def print_template(data, printer_name=None):
    printer = None
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

        _date = date.today().strftime("%A, %dth %b")

        printer.set_with_default(align="center", width=1, height=1)

        # Header section: divider, title divider
        print_divider(printer)
        print_empty_line(printer)
        print_title(printer, title)
        print_empty_line(printer)
        print_divider(printer)
        
        # date section:
        print_empty_line(printer)
        print_text(printer, _date)
        print_empty_line(printer)
        print_divider(printer, "^")

        
        # Category section:
        

        
        
        printer.cut()

    finally:
        if printer:
            printer.close()



def print_divider(printer, shape: str = "*"):
    divider = shape * 48
    printer.set(bold=True)
    printer.text(divider)

def print_title(printer, title:str):
    printer.set(align="center", bold=True, double_width=True, double_height=True)
    printer.text(title + '\n')

def print_empty_line(printer):
    printer.set_with_default()
    printer.text(" "*48)

def print_text(printer, title:str):
    printer.set(align="center")
    printer.text(title + '\n')

def print_art(printer, _file):
    with open(_file, 'r', encoding='cp437') as design:
            art = design.read()
            printer.text(art)

if __name__ == "__main__":
    print_template('data.json', 'pos')
