from dotenv import load_dotenv
# from data_manager import DataManager
import json
import os
import requests
from datetime import datetime as dt
import gspread
from google.oauth2 import service_account

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        load_dotenv("F:/random/.env")
        self.data_list = self.gsheets_editor().get_all_values()
        # self.data_manager = DataManager()
        self.query_list = [item[0] for item in self.data_list]
        self.query_codes = [item[1] for item in self.data_list]
        self.flight_para = {}
        self.today = dt.now()

    def gsheets_editor(self):
        credentials_path = os.getenv("credentials_path")
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
        gc = gspread.authorize(credentials)
        spreadsheet_id = "1Oo0NumRtTr2sobo4N6Ob38xU7cqKoLzjvDaKCeI8xG0"
        sheet = gc.open_by_key(spreadsheet_id).sheet1
        return sheet

    def member_registration(self):
        credentials_path = os.getenv("credentials_path")
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
        gc = gspread.authorize(credentials)
        spreadsheet_id = "1Oo0NumRtTr2sobo4N6Ob38xU7cqKoLzjvDaKCeI8xG0"
        spreadsheet = gc.open_by_key(spreadsheet_id)
        sheet = spreadsheet.worksheet("members")
        existing_data = sheet.get_all_values()
        next_row_index = len(existing_data) + 1
        email = "a"
        verify_email = "b"
        while email != verify_email:
            email = input("What is your email? ")
            verify_email = input("Enter your email again: ")
            if verify_email != email:
                print("Sorry, email does not match. Try again.")
        data_to_append = [
            email,
            input("What's your first name? "),
            input("What's your last name? "),
            input("What's your departure city? "),
            # input("Enter your destination-budget pairs separated by commas like so: Tokyo-700, Sydney-600, Cairo-400 ")
            ]
        sheet.append_row(data_to_append, value_input_option='USER_ENTERED', insert_data_option='INSERT_ROWS',
                     table_range=f"A{next_row_index}")
        print("Welcome to the club!")

    def get_iata(self):
        tequila_api = os.getenv("tequila_api")
        url = "https://api.tequila.kiwi.com/locations/query"
        self.header = {
            "apikey": tequila_api,
        }
        iata_codes = []
        for query in self.query_list[1:]:
            self.flight_para = {
                "term": query,
                "location_types": "airport",
                "limit": "10",
                "active_only": "true",
            }
            iata_codes.append(requests.get(url=url, params=self.flight_para, headers=self.header).json()
                              ["locations"][0]["id"])
        return iata_codes

    def search_six_months(self):
        tequila_api = os.getenv("tequila_api")
        url = "https://api.tequila.kiwi.com/v2/search"
        self.header = {
            "apikey": tequila_api,
        }
        response = []
        tomorrow = int(self.today.strftime("%d")) + 1
        next_month = int(self.today.strftime("%m")) + 1
        for query in self.query_codes[1:]:
            self.flight_para = {
                "fly_from": "airport:PHX",
                "fly_to": f'airport:{query}',
                "dateFrom": self.today.strftime(f'{str(tomorrow)}/%m/%Y'),
                "dateTo": self.today.strftime(f'{str(tomorrow)}/0{str(next_month)}/%Y'),
            }
            response.append(requests.get(url=url, params=self.flight_para, headers=self.header).json())
        return response

    def send_telegram_message(self, message):
        chat_id = os.getenv("chat_id")
        telegram_api = os.getenv("telegram_weather_api")
        send_text = 'https://api.telegram.org/bot' + telegram_api + '/sendMessage?chat_id=' + chat_id + \
                    '&parse_mode=Markdown&text=' + message
        return requests.get(send_text)




    def print_json_structure(self, json_response):
        formatted_response = json.dumps(json_response, indent=2)
        print(formatted_response)


# api = FlightSearch()
# api.gsheets_editor()
# api.print_json_structure(api.get_iata())
# print(api.search_six_months())
