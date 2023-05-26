class FlightData:
    #This class is responsible for structuring the flight data.
    def strip_dest_price(self, response):
        full_res = response
        clean_response = []
        for item in full_res:
            if item == {'status': 'Bad Request',
                        'error': 'unknown partner provided - if you would like to cooperate with Kiwi.com, please register at tequila.kiwi.com'}:
                pass
            else:
                clean_response.append(item)
        data = [item["data"] for item in clean_response]
        flyto_price = []
        for inner_list in data:
            for d in inner_list:
                pair = [d["flyTo"], d["price"]]
                flyto_price.append(pair)
        return flyto_price
