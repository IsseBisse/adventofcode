from bs4 import BeautifulSoup
from datetime import datetime
import os
import requests
import shutil

URL = "https://adventofcode.com/2024/day"
COOKIE = "_ga=GA1.2.1110782972.1732633656; _gid=GA1.2.562086225.1732633656; session=53616c7465645f5f8e1c3dc033b3082dd4b5fff99b3ffd116fc25c093a7c49440e3b871c2b78c32dca498833f8da030ab499c7af2e9a004dad58127d8d24fed5; _gat=1; _ga_MHSNPJKWC7=GS1.2.1732633656.1.1.1732635132.0.0.0"


def get_new_days() -> list[int] | None:
    today = datetime.now()
    if today.month < 12:
        return None

    max_day = min(today.day, 25)
    new_days = [day for day in range(1, max_day + 1) if not os.path.exists(f"{day}/")]

    return new_days


def get_input(session: requests.Session, day: int):
    resp = session.get(f"{URL}/{day}/input", headers={"Cookie": COOKIE})
    return resp.text


def get_small_input(session: requests.Session, day: int):
    resp = session.get(f"{URL}/{day}", headers={"Cookie": COOKIE})

    # Small input is hidden in the first <pre><code> tagged block
    soup = BeautifulSoup(resp.text)
    pre = soup.find("pre")
    code = pre.next

    return code.text


def initialize(session: requests.Session, day: int):
    os.mkdir(f"{day}")

    input_text = get_input(session, day)
    with open(f"{day}/input.txt", "w") as file:
        file.write(input_text)

    small_input_text = get_small_input(session, day)
    with open(f"{day}/smallInput.txt", "w") as file:
        file.write(small_input_text)

    shutil.copyfile("template.py", f"{day}/main.py")


def main():
    new_days = get_new_days()

    session = requests.session()
    for day in new_days:
        initialize(session, day)


if __name__ == "__main__":
    main()
