import json

def format():
    try:
        with open("turnover.json", "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # If the file is empty or doesn't exist, use an empty list
        data = []

    # Convert the existing list to a set for faster operations
    data_set = set(data)

    with open("temp_turnover.json", "rb") as f:
        temp = json.load(f)

    tickers = temp["data"]["watch"]
    stocks = {t["security"].split(".")[0] for t in tickers}  # Use a set to store new stocks

    # Update the data set with new stocks, avoiding duplicates
    data_set.update(stocks)

    # Convert the set back to a list for JSON serialization
    data = list(data_set)

    print(data)

    with open("turnover.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    format()
