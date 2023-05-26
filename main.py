from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch

dm = DataManager()
fd = FlightData()
fs = FlightSearch()

fs.member_registration()

# Update IATA codes
dm.save_iata(fs.get_iata())

# Get base flyTo/price pairs that are under budget
dest_prices = fd.strip_dest_price(fs.search_six_months())
deals = sorted(dm.compare_prices(dest_prices))

# Shortlist best price per destination
lowest = []
if len(deals) > 0:
    for code in deals:
        if len(lowest) < 1:
            lowest.append(code)
        elif code[0] not in lowest[len(lowest) - 1]:
            lowest.append(code)

# Send text alert
for code in lowest:
    fs.send_telegram_message(f'Flights to {code[0]} starting at {code[1]} euros!')
