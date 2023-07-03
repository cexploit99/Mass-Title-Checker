import random
import requests
import threading
from bs4 import BeautifulSoup
from colorama import Fore, Style
import re
import os

os.system('clear' if os.name == 'posix' else 'cls')

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    ]
    return random.choice(user_agents)

def print_header():
    print(Fore.GREEN + "[+] Mass Scan Website Title Checker [+]")
    print(Fore.GREEN + "[+] Faster With Threading [+]")
    print(Style.RESET_ALL)

def add_protocol(website):
    if not re.match(r"^https?://", website):
        return "http://" + website
    return website

def scan_title(website):
    try:
        headers = {
            "User-Agent": get_random_user_agent()
        }
        response = requests.get(website, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string.strip() if soup.title else 'Title not found'

        result = f"Website: {website} – "
        restitle = Fore.GREEN + title
        print(Fore.WHITE + result + restitle)
        print()

        with open('result-title.txt', 'a') as file:
            file.write(result + '\n')

    except requests.exceptions.RequestException as e:
        result = f"Website: Can't Check {website}\n"
        print(Fore.RED + result)
        pass
        
    except:
        pass
      

def scan_titles(websites):
    threads = []

    for website in websites:
        website = add_protocol(website)
        thread = threading.Thread(target=scan_title, args=(website,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print_header()

    file_path = input("Input file domain (.txt): ")
    print()
    with open(file_path, "r") as file:
        websites = [line.strip() for line in file.readlines()]

    scan_titles(websites)
    print(Fore.WHITE + "Results have been saved to result-title.txt")
