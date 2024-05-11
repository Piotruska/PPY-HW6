import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# this function retrieves the current exchange rate for a given currency.
# input : valid currency code
# returns : the data of the rate
def get_current_exchange_rate(currency):
    tables = ['A', 'B']
    for table in tables:
        try:
            url = f"https://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/?format=json"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
            data = response.json()
            if 'rates' in data:
                return data['rates'][0]['mid']
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error ({e.response.status_code}): {e.response.reason}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    print("Error: Unable to fetch current exchange rate. Please check your input.")
    return None


# this function retrieves exchange rates for a currency over the last specified number of days.
# input : valid currency code, amount of days
# - calculates the date to which we want to go back to (start_date)
# returns : the rates (list of touples) amount and date
def get_exchange_rate_for_last_days(currency, days):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    return get_exchange_rate_for_period(currency, start_date_str, end_date_str)

# this function plots a graph showing the exchange rates over the last days.
# input : valid currency code, rates (list of touples)
# returns : N/A
# displays plot
def plot_exchange_rate_over_days(currency, rates):
    dates = [rate[0] for rate in rates]
    exchange_rates = [rate[1] for rate in rates]
    plt.plot(dates, exchange_rates)
    plt.xlabel('Date')
    plt.ylabel(f'{currency} to PLN')
    plt.title(f'{currency} to PLN Exchange Rate Over Last {len(rates)} Days')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# this function retrieves exchange rates for a currency within a specified period.
# input : valid currency code, start date, end date
# returns : the rates (list of touples) amount and date
def get_exchange_rate_for_period(currency, start_date, end_date):
    tables = ['A', 'B']
    for table in tables:
        try:
            url = f"https://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{start_date}/{end_date}/?format=json"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404)
            data = response.json()
            if 'rates' in data:
                rates = [(datetime.strptime(rate['effectiveDate'], '%Y-%m-%d').date(), rate['mid']) for rate in data['rates']]
                return rates
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error ({e.response.status_code}): {e.response.reason}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    print("Error: Unable to fetch exchange rates. Please check your input.")
    return []


# this function plots exchange rates for a currency within a specified period.
# input : valid currency code, list of touples amount and date
# returns : N/A
# displays plot
def plot_exchange_rate_over_period(currency, rates):
    dates = [rate[0] for rate in rates]
    exchange_rates = [rate[1] for rate in rates]
    plt.plot(dates, exchange_rates)
    plt.xlabel('Date')
    plt.ylabel(f'{currency} to PLN')
    plt.title(f'{currency} to PLN Exchange Rate Over Period')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# this function retrieves a list of available currencies supported by the NBP API
# input : N/A
# returns : list of stirngs
def get_available_currencies():
    tables = ['A', 'B']
    currencies = set()
    for table in tables:
        url = f"https://api.nbp.pl/api/exchangerates/tables/{table}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            currencies.update(currency['code'] for currency in data[0]['rates'])
        else:
            print(f"Failed to fetch currencies for table {table}.")
    return list(currencies)


# this function Checks if a given currency code is valid or not.
# input : any type of string that could be a currency code
# returns : bool
def is_valid_currency(currency):
    available_currencies = get_available_currencies()
    code = currency.upper()
    if code in available_currencies:
        return True
    else:
        return False


exit_flag = False
while not exit_flag:
    print("1. Get current exchange rate")
    print("2. Get exchange rate for last days")
    print("3. Get exchange rate for a period")
    print("4. Display all available currencies")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        currency = input("Enter the currency code: ").upper()
        if is_valid_currency(currency):
            exchange_rate = get_current_exchange_rate(currency)
            print(f"Current exchange rate for 1 {currency} is {exchange_rate} PLN")
        else:
            print("Invalid currency code.")
    elif choice == '2':
        currency = input("Enter the currency code (e.g., USD): ").upper()
        if is_valid_currency(currency):
            days = int(input("Enter the number of days: "))
            rates = get_exchange_rate_for_last_days(currency, days)
            plot_exchange_rate_over_days(currency, rates)
        else:
            print("Invalid currency code. Please try again.")
    elif choice == '3':
        currency = input("Enter the currency code (e.g., USD): ").upper()
        if is_valid_currency(currency):
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            rates = get_exchange_rate_for_period(currency, start_date, end_date)
            plot_exchange_rate_over_period(currency, rates)
        else:
            print("Invalid currency code. Please try again.")
    elif choice == '4':
        currencies = get_available_currencies()
        print("Available currencies:")
        for currency in currencies:
            print(currency)
    elif choice == '5':
        print("Exiting...")
        exit_flag = True
    else:
        print("Invalid choice. Please try again.")
