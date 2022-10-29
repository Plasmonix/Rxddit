import os, json
from colorama import Fore

__config__ = json.load(open('./data/config.json', 'r+'))

class Console:
    @staticmethod
    def debug(content: str) -> None:
        if __config__['debug']:
            print(f'[DEBUG] {content}{Fore.RESET}'.replace('[+]', f'[{Fore.GREEN}+{Fore.RESET}]').replace('[*]', f'[{Fore.YELLOW}*{Fore.RESET}]').replace('[>]', f'[{Fore.CYAN}>{Fore.RESET}]').replace('[-]', f'[{Fore.RED}-{Fore.RESET}]'))

    @staticmethod
    def printf(content: str) -> None:
        print(content.replace('[+]', f'[{Fore.GREEN}+{Fore.RESET}]').replace('[*]', f'[{Fore.YELLOW}*{Fore.RESET}]').replace('[>]', f'[{Fore.CYAN}>{Fore.RESET}]').replace('[~]', f'[{Fore.RED}~{Fore.RESET}]'))
    
    @staticmethod
    def print_logo() -> None:
        os.system('cls & mode 140,24 && title Rxddit - github.com/Plasmonix' if os.name == 'nt' else 'clear')
        print(Fore.RED + '''
            ____           __    ___ __ 
           / __ \_  ______/ /___/ (_) /_
          / /_/ / |/_/ __  / __  / / __/
         / _, _/>  </ /_/ / /_/ / / /_  
        /_/ |_/_/|_|\__,_/\__,_/_/\__/...  
                                                           
        ''' + Fore.RESET)