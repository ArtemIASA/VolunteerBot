import pygsheets
import logging

logger = logging.getLogger(__name__)

class Sheets:

    def __init__(self, help_type, table_id):
        logger.info(f'Help type is: {help_type}')
        self.gc = pygsheets.authorize(service_file='client_secret.json')
        self.sh = self.gc.open_by_key(table_id)
        self.wks = self.sh.worksheet('title', help_type)

    def open_wks(self, region):
        self.region = region
        self.wks = self.sh.worksheet('title', region)

    def get_empty_row(self):
        col = self.wks.get_col(2, include_tailing_empty=False)
        empty_row = len(col) + 1
        return empty_row

    def add_newlines(self, text:str):
        text_list = text.split()
        text = ' '.join(l + '\n' * (n % 2 == 1) for n, l in enumerate(text_list))
        return text

    def add_help_info(self, help_info, empty_row):
        help_info = self.add_newlines(help_info)
        self.wks.update_value(f'B{empty_row}', help_info)

    def add_name(self, name, empty_row):
        name = self.add_newlines(name)
        self.wks.update_value(f'D{empty_row}', name)

    def add_phone(self, phone, empty_row):
        wks_cell = self.wks.cell(f'E{empty_row}')
        format_type = pygsheets.custom_types.FormatType.TEXT
        wks_cell.set_number_format(format_type)
        wks_cell.set_value(phone)

    def add_address(self, address, empty_row):
        address = self.add_newlines(address)
        self.wks.update_value(f'C{empty_row}', address)

    def change_added_cells(self, row):
        cols = ['B', 'D', 'E', 'C', 'F']
        cells = [i + str(row) for i in cols]
        for cell in cells:
            wks_cell = self.wks.cell(cell)
            wks_cell.set_text_format('fontFamily', 'Calibri')
            wks_cell.set_text_format('fontSize', 11)

    def add_all(self, chat_data):
        row = self.get_empty_row()
        self.add_help_info(chat_data['help'], row)
        self.add_name(chat_data['name'], row)
        self.add_phone(chat_data['phone'], row)
        self.add_address(chat_data['address'], row)
        #self.change_added_cells(row)
