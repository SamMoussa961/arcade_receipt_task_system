from printer import printer_init, print_template



def speed_run_wrapper(printer_name, function):
    TOP_ART = "(             )   (          (              ) \n )\ )   (   ( /(   )\ )       )\ )        ( /( \n(()/(   )\  )\()) (()/( (    (()/(    (   )\())\n /(_))(((_)((_)\   /(_)))\    /(_))   )\ ((_)\ \n(_))  )\___  ((_) (_)) ((_)  (_))  _ ((_) _((_)\n/ __|((/ __|/ _ \ | _ \| __| | _ \| | | || \| |\n\__ \ | (__| (_) ||   /| _|  |   /| |_| || .` |\n|___/  \___|\___/ |_|_\|___| |_|_\ \___/ |_|\_|\n"
    BOTTOM_ART = "\  )\  )\  )\  )\  )\  )\  )\  )\  )\  )\  )\  )\n \(  \(  \(  \(  \(  \(  \(  \(  \(  \(  \(  \( "
    SCORE_RUN_PART1 = ">>>>>>>>>>>>>>>>>> SCORE RUN >>>>>>>>>>>>>>>>>>>"
    SCORE_RUN_PART3= ">" * 48

    try:
        printer = printer_init(printer_name)
        if printer:
            printer.set(align="center", bold=True)
            printer.text(TOP_ART)

            current_score = function(printer_name, printer)

            printer.set(align="center", bold=True)
            printer.text(SCORE_RUN_PART1)

            printer.set(align="left", bold=True, double_height=True, double_width=True)
            # score bar comes here
            printer.text("score bar\n")

            printer.set_with_default(align="center", bold=True)
            printer.text(SCORE_RUN_PART3)
            printer.text(BOTTOM_ART)
                                                                                
    except Exception:
        if printer:
            printer.cut()
        raise 

    finally:
        if printer:
            printer.cut()
            printer.close()


def speed_run_fail_wrapper(printer_name, function):
    RUN_FAILED = "@@@@@@@   @@@  @@@  @@@  @@@      \n@@@@@@@@  @@@  @@@  @@@@ @@@      \n@@!  @@@  @@!  @@@  @@!@!@@@      \n!@!  @!@  !@!  @!@  !@!!@!@!      \n@!@!!@!   @!@  !@!  @!@ !!@!      \n!!@!@!    !@!  !!!  !@!  !!!      \n!!: :!!   !!:  !!!  !!:  !!!      \n:!:  !:!  :!:  !:!  :!:  !:!      \n::   :::  ::::: ::   ::   ::      \n :   : :   : :  :   ::    :       \n                                  \n                                  \n@@@@@@@@   @@@@@@   @@@  @@@      \n@@@@@@@@  @@@@@@@@  @@@  @@@      \n@@!       @@!  @@@  @@!  @@!      \n!@!       !@!  @!@  !@!  !@!      \n@!!!:!    @!@!@!@!  !!@  @!!      \n!!!!!:    !!!@!!!!  !!!  !!!      \n!!:       !!:  !!!  !!:  !!:      \n:!:       :!:  !:!  :!:   :!:     \n ::       ::   :::   ::   :: :::: \n :         :   : :  :    : :: : : \n"
    try:
        printer = printer_init(printer_name)
        if printer:
            printer.set(align="center", bold=True)
            printer.text(RUN_FAILED)
            printer.set_with_default()
            function(printer_name, printer)
            
    except Exception:
        if printer:
            printer.cut()
        raise 
    finally:
        if printer:
            printer.cut()
            printer.close()
    
def score_bar(score: int) -> str:
    total_length = 24
    score_str = f"{score} PTS"
    
    bar_length = total_length - len(score_str) - 1
    
    max_score = 250
    
    filled_length = int((min(score, max_score) / max_score) * bar_length)
    
    filled_length = min(filled_length, bar_length)
    
    empty_length = bar_length - filled_length
    bar = "█" * filled_length
    
    if empty_length >= 3:
        gradient = "▓▒░"
        gradient = gradient[:empty_length]
    else:
        gradient = " " * empty_length
    
    return f"{bar}{gradient} {score_str}\n"