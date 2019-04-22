symbol_check

Simple python script that uses a REST API exposed by alphavantage.co.  
Have been running with python 3.7.
Usage:  "python3.7 symbol_check.py <stock symbol>"
Prints last opn, high, low, close, and volume details.
Pulls list of stock symbols from market_api REST API.  Requests open, high, low, close and volume
details from alphavantage.co RESTAPI and pushes those results to market_api.

If docker is installed and running, ./build.sh creates a docker container with the script. After running 
the build script, run with "docker run symbol_check <stock symbol>" 
