import argparse
import os
from tqdm import tqdm

import utils
from modules import lookup, free_scraping, reputation
from lib import amazon, instagram


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def parse_args():
    parser = argparse.ArgumentParser(description='OSINT tool for phone number tracking.')
    parser.add_argument('phonenumber', nargs='?', help='Phone number (e.g.: +34123456789)')
    args = parser.parse_args()
    if not args.phonenumber:
        args.phonenumber = input("Enter the phone number (e.g.: +34123456789): ")
    return args

def main():
    """Main function that runs the tool."""
    clear_screen()
    print(utils.Banner)
    
    args = parse_args()
    phone_number = args.phonenumber.strip()
    phone_format = phone_number.replace("+33", "")  # format country
    free_format = phone_number.replace("+", "")

    lookup.Look(phone=phone_number)

    print(f"\n{utils.Green}> {utils.White}Ignorant Modules\n{utils.Green}{'-'*51}{utils.White}\n")
    try:
        amazon.main(phone=phone_format)
        instagram.main(phone=phone_format)
    except Exception as e:
        print(f"Error in ignorant modules: {e}")

    print(f"\n[{utils.Red}-{utils.White}] = No account, [{utils.Green}+{utils.White}] = Linked account, [{utils.Black}x{utils.White}] = Ratelimit")

    print(f"\n\n{utils.Green}> {utils.White}Free-lookup.net\n{utils.Green}{'-'*51}{utils.White}\n")
    try:
        free_scraping.Main(phone=free_format)
        reputation.Main(phone=phone_format)
    except Exception as e:
        print(f"Error in free-lookup modules: {e}")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n[!] KeyboardInterrupt ...")
        exit(1)