import os
import asyncio
import requests
from json import dumps as dp
import json
import time
from colorama import init, Fore, Style
import cloudscraper

init(autoreset=True)

# Define color variables
RED = Fore.RED + Style.BRIGHT
GREEN = Fore.GREEN + Style.BRIGHT
YELLOW = Fore.YELLOW + Style.BRIGHT
BLUE = Fore.BLUE + Style.BRIGHT
MAGENTA = Fore.MAGENTA + Style.BRIGHT
CYAN = Fore.CYAN + Style.BRIGHT
WHITE = Fore.WHITE + Style.BRIGHT

def proses(init_data, index):
    print(f"{YELLOW}Starting info retrieval for account {index}")
    print(f"{CYAN}Generating wallet")
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
        "telegramRawData": init_data,
        "Accept": "*/*",
        "Origin": "https://pocketfi.app",
        "X-Requested-With": "org.telegram.messenger",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://pocketfi.app/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7"
    }
    url = "https://bot.pocketfi.org/tgUserWallets"
    while True:
        try:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url=url, headers=headers)
            print(f"Response: {response.text}")
            if response.status_code == 200:
                response_data = response.json()
                if response_data[0]['address'] is not None:
                    address = response_data[0]['address']
                    ton_address = response_data[0]['tonUnbouncableAddress']
                    print(f"{GREEN}Wallet generation for account {index} succeeded: Address: {address} -- Ton Address: {ton_address}")
                    file_path = 'wallet_pocketfi.txt'
                    with open(file_path, 'w') as file:
                        file.write(f"Address: {address} -- Ton Address: {ton_address}\n")
                    getproses(init_data, index)
                    break
                else:
                    print(f'{RED}Wallet generation for account {index} FAILED... RETRYING...')
                    time.sleep(5)
            else:
                print(f'{RED}Wallet generation for account {index} FAILED... RETRYING...')
                time.sleep(5)
        except Exception as e:
            print(f'{RED}Wallet generation for account {index} FAILED... ERROR: {e} -- RETRYING...')
            time.sleep(5)

def getproses(init_data, index):
    print(f"{CYAN}Checking if user is new or existing")
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
        "telegramRawData": init_data,
        "Accept": "*/*",
        "Origin": "https://pocketfi.app",
        "X-Requested-With": "org.telegram.messenger",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://pocketfi.app/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,id-ID;q=0.9,id;q=0.8,en-US;q=0.7"
    }
    url = "https://gm.pocketfi.org/mining/getUserMining"
    while True:
        try:
            scraper = cloudscraper.create_scraper()
            response = scraper.get(url=url, headers=headers)
            print(f"Response: {response.text}")
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('userMining') == None:
                    print(f"{GREEN}User is fresh, creating user mining")
                    url2 = "https://gm.pocketfi.org/mining/createUserMining"
                    ress = scraper.post(url=url2, headers=headers)
                    if ress.status_code == 200:
                        ressponse_data2 = ress.json()
                        if ressponse_data2.get('userMining') is not None:
                            print(f"{GREEN}User mining creation for account {index} succeeded!")
                        else:
                            print(f'{RED}User mining creation for account {index} FAILED... SKIPPING...')
                    break
                else:
                    print(f"{GREEN}User is not fresh, skipping...")
                    break
            else:
                print(f'{RED}User check for account {index} FAILED... RETRYING...')
                time.sleep(5)
        except Exception as e:
            print(f'{RED}User check for account {index} FAILED... ERROR: {e} -- SKIPPING...')

async def run_all_functions():
    print("- DOR -")
    
    data = "query.txt"
    
    with open(data, "r", encoding="utf-8") as file:
        for index, line in enumerate(file, start=1):
            init_data = line.strip()
            proses(init_data, index)

if __name__ == "__main__":
    asyncio.run(run_all_functions())
