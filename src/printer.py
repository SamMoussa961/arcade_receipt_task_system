import json
from datetime import date
from escpos.printer import CupsPrinter, Dummy
from objects.project import Project
from objects.task import Task


def printer_init(printer_name=None):
    printer = None
    try:
        if printer_name:
            printer = CupsPrinter(printer_name)
            printer._raw(b'\x1c\x2e')      # Cancel Chinese mode
            #printer._raw(b'\x1b\x74\x00')  # CP437
        else:
            printer = Dummy()

        printer.open()
        printer.set_with_default(align="center", width=1, height=1)
        return printer
    except Exception as e:
        raise e


def print_template(printer_name=None, printer = None):
    owns_printer = printer is None
    try:
        if owns_printer:
            printer = printer_init(printer_name)
        
        project = get_data()
        print_header(printer, project.category)
        print_task_table(printer, project)
    except Exception as e:
        raise e
    finally:
        if owns_printer and printer:
            printer.cut()
            printer.close()
        return project.total_points


def print_header(printer, category):
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
    
    result = values.get(category)
    
    print_divider(printer)
    printer.set(align="center", bold=True, double_width=True, double_height=True)
    printer.text(TOP_BORDER)
    printer.text(result)
    printer.text("\n")
    printer.text(BOTTOM_BORDER)
    print_divider(printer)
    printer.set(align="center", bold=False, double_width=True, double_height=True)
    printer.text(date.today().strftime("%A, %dth %b") + "\n")
    print_divider(printer)
    print_divider(printer, "*")
    print_divider(printer)


def print_divider(printer, filler = " "):
    printer.set_with_default()
    printer.text(f"{filler * 48}\n")


def print_task_table(printer, project):
    table_head = "  Tasks                                 |  Pts  \n"

     # print table header
    printer.text(table_head)
    print_divider(printer, "-")

    for task in project.tasks:
        # print table rows
        row = f" [ ] {task.name.ljust(37)} +{task.points}  \n"
        printer.text(row)
    
    print_divider(printer, "=")
    printer.text(f" Deadline: {project.deadline} \n".rjust(48))
    print_divider(printer, "=")
    print_divider(printer)

        
def get_data(data = 'data.json'):
    with open(data, 'r', encoding='utf-8') as data_file:
        raw = json.load(data_file)        
    
    project = Project(
        category = raw["category"],
        tasks = [Task(**task) for task in raw["tasks"]],
        deadline = raw["deadline"]
    )

    return project

print_template("pos1")