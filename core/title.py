from colorama import Fore, Style, init

init(autoreset=True)

def show_title():
    print(Fore.CYAN + Style.BRIGHT + "╔" + "═" * 78 + "╗")
    print(Fore.CYAN + Style.BRIGHT + "║" + " " * 78 + "║")
    
    lineas_titulo = [
        "  ██████╗██╗  ██╗ █████╗ ██████╗  █████╗  ██████╗████████╗███████╗██████╗",
        " ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗",
        " ██║     ███████║███████║██████╔╝███████║██║        ██║   █████╗  ██████╔╝",
        " ██║     ██╔══██║██╔══██║██╔══██╗██╔══██║██║        ██║   ██╔══╝  ██╔══██╗",
        " ╚██████╗██║  ██║██║  ██║██║  ██║██║  ██║╚██████╗   ██║   ███████╗██║  ██║",
        "  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝",
        "",
        "           ██████╗ ███████╗███╗   ██╗",
        "          ██╔════╝ ██╔════╝████╗  ██║",
        "          ██║  ███╗█████╗  ██╔██╗ ██║",
        "          ██║   ██║██╔══╝  ██║╚██╗██║",
        "          ╚██████╔╝███████╗██║ ╚████║",
        "           ╚═════╝ ╚══════╝╚═╝  ╚═══╝"
    ]
    
    for i, linea in enumerate(lineas_titulo):
        if i < 6:
            color = Fore.MAGENTA
        else:
            color = Fore.YELLOW
        print(Fore.CYAN + "║ " + color + Style.BRIGHT + linea.ljust(76) + Fore.CYAN + " ║")
    
    print(Fore.CYAN + Style.BRIGHT + "║" + " " * 78 + "║")
    print(Fore.CYAN + Style.BRIGHT + "╚" + "═" * 78 + "╝")