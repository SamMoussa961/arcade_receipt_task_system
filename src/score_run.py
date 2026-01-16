from printer import printer_init, print_header

def speed_run_wrapper(printer_name, function):
    TOP_ART = "(             )   (          (              ) \n )\ )   (   ( /(   )\ )       )\ )        ( /( \n(()/(   )\  )\()) (()/( (    (()/(    (   )\())\n /(_))(((_)((_)\   /(_)))\    /(_))   )\ ((_)\ \n(_))  )\___  ((_) (_)) ((_)  (_))  _ ((_) _((_)\n/ __|((/ __|/ _ \ | _ \| __| | _ \| | | || \| |\n\__ \ | (__| (_) ||   /| _|  |   /| |_| || .` |\n|___/  \___|\___/ |_|_\|___| |_|_\ \___/ |_|\_|\n"
    BOTTOM_ART = "\  )\  )\  )\  )\  )\  )\  )\  )\  )\  )\  )\  )\n \(  \(  \(  \(  \(  \(  \(  \(  \(  \(  \(  \( "
    try:
        printer = printer_init(printer_name)
        if printer:
            printer.set(align="center", bold=True)
            printer.text(TOP_ART)
            function(printer)
            printer.set(align="center", bold=True)
            printer.text(BOTTOM_ART)
            printer.cut()
            printer.close()
            
    except Exception as e:
        raise e

speed_run_wrapper('pos', print_header)