import os
from datetime import datetime
import json

data_filename = "data.json"
main_options = ["Add data point", "Create graph", "Exit"]
account_selection_options = ["Select a tracked account", "Add a new account"]


def parseOption(options):
    print("Select one:")
    for n, i in enumerate(options):
        print(f"{n} - {i}")
    print()

    while True:
        try:
            val = int(input(f"Enter an integer between 0 and {len(options) - 1}: "))
            if val < 0 or val >= len(options):
                print("Not in range, try again")
                continue
            return val
        except KeyboardInterrupt:
            exit("\nBye")
        except ValueError:
            print("Not an integer, try again")


def parseFloat():
    while True:
        try:
            val = float(
                input("Enter a number: ").replace("$", "").replace(",", "").strip()
            )
            return val
        except KeyboardInterrupt:
            print("\nBye")
            exit()
        except ValueError:
            print("Not a number, try again")


def addAccount():
    return input("Enter account name: ")


def addDataPoint():
    if not os.path.exists(data_filename):
        data = {}
    else:
        with open(data_filename) as f:
            data = json.load(f)

    date = datetime.today().date().strftime("%Y-%m-%d")

    if len(data) > 0:
        match parseOption(account_selection_options):
            case 0:
                account = list(data.keys())[parseOption(data.keys())]

            case 1:
                account = addAccount()
    else:
        account = addAccount()

    print("Enter account value")
    value = parseFloat()

    if account not in data.keys():
        data[account] = {}

    if date in data[account]:
        print("Data already exists. Select which  to use")
        options = [f"existing - {data[account][date]}", f"new - {value}"]
        match parseOption(options):
            case 0:
                pass
            case 1:
                data[account][date] = value
    else:
        data[account][date] = value

    with open(data_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def createGraph():
    pass


while True:
    match parseOption(main_options):
        case 0:
            addDataPoint()
        case 1:
            createGraph()
        case 2:
            exit("Bye")
