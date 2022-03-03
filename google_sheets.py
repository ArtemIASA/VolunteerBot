import pygsheets
import logging
import re

logger = logging.getLogger(__name__)

class Sheets:

    def __init__(self, region):
        self.gc = pygsheets.authorize(service_file='client_secret.json')
        self.sh = self.gc.open_by_url("https://docs.google.com/spreadsheets/d/1AdJO-HpdM9p0dj1is0oYV7Xv3GPTauLzJ074LX-tqIY/edit?usp=sharing")
        self.wks = self.sh.worksheet('title', region)
        self.region = region

    def open_wks(self, region):
        self.region = region
        self.wks = self.sh.worksheet('title', region)

    def get_empty_row(self):
        col = self.wks.get_col(2, include_tailing_empty=False)
        empty_row = len(col) + 1
        return empty_row

    def validate_name(self, text):
        return re.fullmatch("^[А-Яа-яЁёЇїІіЄєʼ ,.'-]+$", text)

    def validate_address(self, text):
        return re.fullmatch("^[А-Яа-я0-9ЁёЇїІіЄєʼ ,.'-]+$", text)

    def validate_phone(self, text):
        return re.fullmatch("^[0-9]+$", text)

    def add_help_info(self, help_info):
        empty_row = self.get_empty_row()
        self.wks.update_value(f'B{empty_row}', help_info)


    def add_name(self, name):
        empty_row = self.get_empty_row()
        self.wks.update_value(f'D{empty_row - 1}', name)

    def add_phone(self, phone):
        empty_row = self.get_empty_row()
        self.wks.update_value(f'E{empty_row - 1}', phone)


    def add_address(self, address):
        empty_row = self.get_empty_row()
        self.wks.update_value(f'C{empty_row - 1}', address)
