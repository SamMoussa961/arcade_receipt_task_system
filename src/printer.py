from escpos.printer import Dummy


def print_to_printer():
    try:

        printer = Dummy()
        with open("../print.txt") as f:
            for line in f:
                printer.text(line)

            print(printer.output.decode("ascii"))
            printer.clear()

    except Exception as e:
        print(f"ERROR printing to thermal printer: {str(e)}")

print_to_printer()