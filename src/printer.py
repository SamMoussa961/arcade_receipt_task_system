from datetime import date
import json
from escpos.printer import CupsPrinter, Dummy


def printer_init(printer_name=None):
    printer = None
    try:
        if printer_name:
            printer = CupsPrinter(printer_name)
        else:
            printer = Dummy()

        printer.open()
        printer.set_with_default(align="center", width=1, height=1)
        return printer
    except Exception as e:
        raise e


def print_template(data, printer_name=None):
    printer = None
    
    try:
        printer = printer_init(printer_name)
        if printer:
            
            with open(data, 'r', encoding='utf-8') as data_file:
                receipt_data = json.load(data_file)

            title = receipt_data["title"]
            category = receipt_data["category"]
            tasks = receipt_data["tasks"]
            points = receipt_data["points"]
            deadline = receipt_data["deadline"]

            print_header(printer, title)
 
            
    except Exception as e:
        raise e

    finally:
        if printer:
            printer.cut()
            printer.close()

def print_header(printer, title):
    ASSIGNMENTS = "█▌     ASSIGNMENTS    ▐█"
    MAINTENANCE = "█▌     MAINTENANCE    ▐█"
    WELLNESS =    "█▌       WELLNESS     ▐█"
    ERRANDS =     "█▌       ERRANDS      ▐█"
    FOCUS =       "█▌        FOCUS       ▐█"
    TOP_BORDER = "████████████████████████\n█▌                    ▐█\n"
    BOTTOM_BORDER = "█▌                    ▐█\n████████████████████████"

    values = {
        "assignments": ASSIGNMENTS,
        "maintenance": MAINTENANCE,
        "wellness": WELLNESS,
        "errands": ERRANDS,
        "focus": FOCUS
    }
    
    result = values.get(title)
    
    print_empty_line(printer)
    printer.set(align="center", bold=True, double_width=True, double_height=True)
    printer.text(TOP_BORDER)
    printer.text(result + "\n")
    printer.text(BOTTOM_BORDER)
    print_empty_line(printer)
    printer.set(align="center", bold=False, double_width=True, double_height=True)
    printer.text(date.today().strftime("%A, %dth %b") + "\n")
    print_empty_line(printer)


def print_empty_line(printer):
    printer.set_with_default()
    printer.text(" "*48)


