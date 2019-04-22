''' Using https://www.alphavantage.co to retrieve stock prices.  Requires a unique key, freely availalble.
    Sample request: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=INX&apikey=0KEDXOP6GN0KTIY5
    Return result:
    {
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "INX",
        "3. Last Refreshed": "2019-02-01",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
         "2019-02-01": {
            "1. open": "2702.3201",
            "2. high": "2716.6599",
            "3. low": "2696.8799",
            "4. close": "2706.5300",
            "5. volume": "3759270000"
        },
        "2019-01-31": {
            "1. open": "2685.4900",
            "2. high": "2708.9500",
            "3. low": "2678.6499",
            "4. close": "2704.1001",
            "5. volume": "4917650000"
        },
        "2019-01-30": {
            "1. open": "2653.6201",
            "2. high": "2690.4399",
            "3. low": "2648.3401",
            "4. close": "2681.0500",
            "5. volume": "3857810000"
        },
        ....
    }
'''

import sys
import certifi
import urllib3
import requests



# free api key from https://alphavantage.co
api_key='0KEDXOP6GN0KTIY5'
site_url = 'https://www.alphavantage.co/'
db_url = 'https://market.hamzazafar.co'
#db_url = 'http://172.17.0.3'
#db_url = 'http://market_api'

# Example to pull what's available in db
collections_url = db_url + "/symbols"
print(collections_url)
response = requests.get(collections_url)
print("response: " + str(response))
print(response.text)

# one symbol per line
# Current format is "stock_symbol:collection name"
for sym in response.json():
    print(sym)

    request_url = site_url + 'query?function=TIME_SERIES_DAILY&symbol=' + \
        sym + '&apikey=' + api_key
    print('request_url = ' + request_url)

    # ignore certificate validation in request (risky for production code)
    urllib3.disable_warnings()

    try:

        response  = requests.get(request_url, verify = False)

    except Exception as e:
        # request failed.  need to log appropriately
        print('Exception requesting stock info: ' + str(e))
        sys.exit(1)

    if response.status_code == 200:
        # extract data
        try:
            result = response.json()
            daily_data = result['Time Series (Daily)']
        except Exception as e:
            # probably a bad symbol lookup.  again, logging here
            print(str(e))

        # this requires python3.7, which introduced ordered dictionaries.
        # otherwise we have to construct date key (YYYY-MM-DD), which
        # is a pain - have to track weekends/holidays
        try:
            most_recent_date = list(daily_data.keys())[0]
            first_val = list(daily_data.values())[0]
            most_recent_open = first_val['1. open']
            most_recent_high = first_val['2. high']
            most_recent_low = first_val['3. low']
            most_recent_close = first_val['4. close']
            most_recent_volume = first_val['5. volume']

            print('Date: ' + most_recent_date + ' Stock: ' + stock_symbol + ' Open: ' + str(
                most_recent_open) + ' High: ' + str(most_recent_high) + ' Low: ' + str(most_recent_close) +
                ' Close: ' + str(most_recent_close) + ' Volume: ' + str(most_recent_volume))
        except:
            print('Exception accessing data')

        try:
            insert_url = db_url + "/insert/" + sym + "?date=" + most_recent_date + "&close=" + most_recent_close + \
    		"&open=" + most_recent_open + "&low=" + most_recent_low + "&high=" + most_recent_high

            print(insert_url)
            response = requests.post(insert_url)

            if response.status_code == 409:
                print('db insert error: conflict')
            elif response.status_code == 405:
                print('db insert error: method not allowed')
                print('response.txt = ' + response.text)
            elif response.status_code != 201:
                print('db insert error =' + str(response.status_code))
                print('response.text = ' + response.text)
            else:
                print('database insert success')
        except Exception as e:
            print('Exception posting to DB ' + str(e))


    else:
        print('request error: ' + str(response.status_code))

