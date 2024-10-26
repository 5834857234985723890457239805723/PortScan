import os
import socket
import concurrent.futures
from pystyle import Colorate, Colors

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ascii_art():
    ascii_art = """
███████╗ ██████╗ ██╗  ██╗██╗████████╗ ██████╗ ██╗   ██╗     
╚══███╔╝██╔═══██╗██║ ██╔╝██║╚══██╔══╝██╔═══██╗╚██╗ ██╔╝     
  ███╔╝ ██║   ██║█████╔╝ ██║   ██║   ██║   ██║ ╚████╔╝     
 ███╔╝  ██║   ██║██╔═██╗ ██║   ██║   ██║   ██║  ╚██╔╝       
███████╗╚██████╔╝██║  ██╗██║   ██║   ╚██████╔╝   ██║   
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝    ╚═════╝    ╚═╝   
    """ 
    colored_ascii_art = Colorate.Horizontal(Colors.red_to_blue, ascii_art)
    print(colored_ascii_art)

def display_menu():
    ascii_art = """
=================================================
Scannneur de port | [+] By Ես գալիս եմ Կավկազից
================================================
\n Options
\n [1]  : Scanne les ports
\n [00] : Quitter
    """
    colored_ascii_art = Colorate.Horizontal(Colors.red_to_blue, ascii_art)
    print(colored_ascii_art)

def scan_port(ip, port, timeout=0.5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((ip, port))
            return port
        except (socket.timeout, socket.error):
            return None
        except Exception as e:
            print(f"Erreur lors du scan du port {port}: {e}")
            return None

def scan_ports(ip, port_range=range(1, 65536), max_workers=5000):
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in port_range}
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port is not None:
                open_ports.append(port)
                print(Colorate.Color(Colors.green, f"Port {port} ouvert"))
            else:
                print(Colorate.Horizontal(Colors.red_to_black, f"Port {futures[future]} fermé ou inaccessible"))

    return open_ports

if __name__ == "__main__":
    clear_terminal()
    display_ascii_art()

    while True:
        display_menu()
        choice = input(" [+] Choisisez votre option  : ").strip()
        
        if choice == '1':
            ip = input(Colorate.Horizontal(Colors.red_to_blue
    , "\nEntrez l'adresse IP à scanner : "))
            print(Colorate.Color(Colors.cyan, "Scanning tous les ports de 1 à 65535..."))
            open_ports = scan_ports(ip)
            if open_ports:
                print(Colorate.Color(Colors.cyan, f"Ports ouverts : {open_ports}"))
            else:
                print(Colorate.Color(Colors.cyan, "Aucun port ouvert détecté."))
            
            input(Colorate.Horizontal(Colors.red_to_blue
    , "\nAppuyez sur Entrée pour réinitialiser le terminal..."))
            clear_terminal()
            display_ascii_art()
        
        elif choice == '00':
            print()
        elif choice == '0':
            print()
            break
        
        else:
            print(Colorate.Horizontal(Colors.red_to_blue
    , "\nOption invalide. Veuillez réessayer."))
