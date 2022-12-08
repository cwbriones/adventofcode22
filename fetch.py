import os
import os.path
import sys

import datetime
from zoneinfo import ZoneInfo

import requests


def fetch(day):
    try:
        with open(os.path.expanduser("~/.aoc-session")) as f:
            session_cookie = f.read().strip()
    except FileNotFoundError as e:
        raise ValueError(f"Could not find session token") from e

    fname = f"{day}.in"
    if os.path.exists(fname):
        print(f"{fname} already exists, refusing to overwrite.")
        return
    url = f"https://adventofcode.com/2022/day/{day}/input"
    resp = requests.get(url, headers={"Cookie": f"session={session_cookie}"})
    if resp.status_code != 200:
        raise Exception(f"status was {resp.status_code}")
    with open(fname, "w+") as f:
        f.write(resp.text)


def main():
    today = datetime.datetime.now(tz=ZoneInfo("America/New_York"))
    if len(sys.argv) == 2:
        day = int(sys.argv[1])
        if day not in range(1, 26):
            raise ValueError("out of range")
        print(f"Fetching input for {day} Dec")
    elif len(sys.argv) == 1 and today.month == 12:
        day = today.day
        print(f"Using current date (EST): Dec {day}")
    else:
        print(
            f"""usage: {sys.argv[0]} [day]

Fetch the given day's input, using the current date if no argument is supplied.

Your session cookie is expected to be at ~/.aoc-session
        """
        )
        sys.exit(1)
    fetch(day)


if __name__ == "__main__":
    main()
