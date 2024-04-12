import os
from datetime import datetime
import json
import matplotlib.pyplot as plt
import locale

data_filename = "data.json"
main_options = [
    "Add data point",
    "Create graphs",
    "Calculate current net worth",
    "Exit",
]
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


def parseAccountsData():
    if not os.path.exists(data_filename):
        print("Add some data and try again\n")
        return

    with open(data_filename) as f:
        data = json.load(f)

    dates = set()
    accounts_data = {}

    for account, balances in data.items():
        for date in balances.keys():
            dates.add(datetime.strptime(date, "%Y-%m-%d"))
    dates = sorted(dates)

    for account, balances in data.items():
        accounts_data[account] = []
        prev_balance = 0
        for date in dates:
            if date.strftime("%Y-%m-%d") in balances:
                prev_balance = balances[date.strftime("%Y-%m-%d")]
            accounts_data[account].append((date, prev_balance))

    return dates, accounts_data


def calculateRunningTotals(dates, accounts_data):
    running_totals = {}
    for date in dates:
        running_totals[date] = 0
        for _, balances in accounts_data.items():
            for _date, balance in balances:
                if _date == date:
                    running_totals[date] += balance
                    break
    _, values = zip(*sorted(running_totals.items()))
    return values


def createGraphs():
    try:
        dates, accounts_data = parseAccountsData()
    except TypeError:
        return
    plt.figure(dpi=300, figsize=(15, 7.5))
    for account, balances in accounts_data.items():
        _dates, _values = zip(*sorted(balances))
        plt.plot(_dates, _values, label=account)
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.title("Account Balances")
    plt.legend()
    plt.tight_layout()
    plt.savefig("account_balances")
    plt.close()

    values = calculateRunningTotals(dates, accounts_data)
    plt.figure(dpi=300, figsize=(15, 7.5))
    plt.plot(dates, values)
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Net Worth")
    plt.tight_layout()
    plt.savefig("net_worth")
    plt.close()


def calcNetWorth():
    try:
        dates, accounts_data = parseAccountsData()
    except TypeError:
        return
    values = calculateRunningTotals(dates, accounts_data)
    if values is None:
        print()
        return

    print(f"Current net worth: {locale.currency(values[-1], grouping=True)}\n")


locale.setlocale(locale.LC_ALL, "")
while True:
    match parseOption(main_options):
        case 0:
            addDataPoint()
        case 1:
            createGraphs()
        case 2:
            calcNetWorth()
        case 3:
            exit("Bye")
