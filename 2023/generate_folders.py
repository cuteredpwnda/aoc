import os
import shutil
import sys

from datetime import datetime
import requests
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def pad_date(date: int):
   if date < 10:
       return f"0{date}"
   elif date > 25:
       return None
   else:
       return f"{date}"

def main(today:(int|None)=None):
    if not today:
        today = datetime.now().day
    day_pad = pad_date(today)

    days_to_generate = [day_pad]
    for day in days_to_generate:
        if day is None:
            pad = "01"
        elif int(day) > 25:
            pad = "25"
            baseurl = "https://adventofcode.com/2022/day"
        else:
            pad = day
            baseurl = "https://adventofcode.com/2023/day"

        templates = os.path.join(os.path.dirname(__file__), "templates")
        if pad is not None:
            folder_template = f"day_{pad}"
            if not os.path.isdir(folder_template):
                os.makedirs(folder_template)
                shutil.copy(os.path.join(templates, "day_xx.py"), os.path.join(folder_template, f"day_{pad}.py"))
            else:
                print(f"Folder for day{pad} already exists.")
            if int(pad) == today:
                input_folder = os.path.join(folder_template, "input")
                if not os.path.isdir(input_folder):
                    os.makedirs(input_folder)
                url = f"{baseurl}/{int(pad)}/input"
                cookie = os.getenv("AOC_COOKIE")
                user_agent = os.getenv("AOC_USER_AGENT")
                if not os.path.isfile(os.path.join(input_folder, "input.txt")):
                    response = requests.get(url, cookies={"session": cookie}, headers={"User-Agent": user_agent})
                    if "Please don't" in response.text:
                        print("Not time yet!")
                        sys.exit(1)
                    with open(os.path.join(input_folder, "input.txt"), 'w') as f:
                        f.write(response.text)
                else:
                    print("Input already exists.")
        else:
            print(f"No folder created, day ({pad}) is not in range")

# pass in the day as an argument
if __name__ == '__main__':

    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main()
