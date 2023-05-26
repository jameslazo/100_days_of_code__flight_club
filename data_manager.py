# from pyexcel_ods3 import save_data, get_data
from flight_search import FlightSearch

class DataManager:
    def __init__(self):
        self.fs = FlightSearch()
        self.sheet = self.fs.gsheets_editor()
        self.data_list = self.sheet.get_all_values()
        self.data_response = [[i[1], i[2]] for i in self.data_list[1:]]

    def save_iata(self, iata):
        column = 2
        row = 2
        for item in iata:
            self.sheet.update_cell(row, column, item)
            row += 1

    def compare_prices(self, response):
        deals = []
        for item in response:
            for res in self.data_response:
                if float(item[1]) < float(res[1]) and item[0] == res[0]:
                    deals.append(item)
        return deals

    # def __init__(self):
    #     self.data = get_data("destinations.ods")
    #     self.data_list = self.data["Sheet1"]
    #     self.data_response = [[i[1], i[2]] for i in self.data_list[1:]]
    #
    # def save_iata(self, iata):
    #     column = 1
    #     row = 0
    #     for item in iata:
    #         row += 1
    #         self.data_list[row][column] = item
    #         self.data.update({"Sheet1": self.data_list})
    #     save_data("destinations.ods", self.data)
    #
    # def compare_prices(self, response):
    #     deals = []
    #     for item in response:
    #         for res in self.data_response:
    #             if float(item[1]) < float(res[1]) and item[0] == res[0]:
    #                 deals.append(item)
    #     return deals

# dm = DataManager()
# print(dm.data_tuples[0][1])