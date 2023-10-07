import os
import json
import getmsg
from apiclient import discovery
from google.oauth2 import service_account
from datetime import datetime

# Read configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

spreadsheet_id = config.get('spreadsheet_id')

# Predifine credentials and service
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
secret_file = os.path.join(os.getcwd(), 'service_account.json')
credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=scopes)
service = discovery.build('sheets', 'v4', credentials=credentials)

def get_sheet_titles():
    # Call the Sheets API to fetch spreadsheet metadata
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_titles = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
    # return sheet_titles
    # Filter out only the 2023 sheets
    sheet_titles = [title for title in sheet_titles if "2023" in title or " 23" in title]
    # print(sheet_titles)
    return sheet_titles

# Get the most recent sheet title from the list of sheet titles, by converting the list to a dictionary and sorting the dictionary by key
def get_most_recent_sheet_title():
    sheets = get_sheet_titles()
    # Updated mapping for common month name variations
    month_mapping = {
        "jan": "Jan", "feb": "Feb", "mar": "Mar", "apr": "Apr", "may": "May",
        "jun": "Jun", "june": "Jun", "jul": "Jul", "july": "Jul",
        "aug": "Aug", "sept": "Sep", "sep": "Sep", "oct": "Oct",
        "nov": "Nov", "dec": "Dec"
    }
    
    # Helper function to parse and convert sheet name to date
    def convert_to_date(sheet):
        month, year = sheet.split()
        month = month_mapping.get(month.lower(), month)  # Map to correct month name if needed
        if len(year) == 2:  # Convert 2-digit year to 4-digit
            year = '20' + year
        # Convert to date using abbreviated month format
        return datetime.strptime(f"{month} {year}", '%b %Y')
    
    # Convert all sheet names to dates
    dates = [convert_to_date(sheet) for sheet in sheets]
    
    # Return the sheet corresponding to the most recent date
    return sheets[dates.index(max(dates))]

# Get data from the spreadsheet
def get_data(sheet):

    # Define the range of cells to retrieve
    range_name = '%s!A3:G1500' % sheet

    # Get all data from the spreadsheet
    data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    
    # Get the values from the spreadsheet
    values = data.get('values', [])
    
    # return getmsg.data_cleaning(values)
    return values

# 7 columns
def data_cleaning(values):
    # Extend the list to 7 columns
    # padded_data = get_data(values)
    padded_data = values
    for row in values:
        while len(row) < 7:
            row.append("")  
    

    # for row in padded_data:
    #     while row[1] == "":
    #         row.pop(0)

    return padded_data

# Filtering out rows that have a value in the 7th column with a safer approach and return a list of lists
def filter_data(i):
    
    filtered_data = [row for row in i if len(row) < 7 or not row[6]]

    return filtered_data

# Normalize Room Number to all lower case and no space for matching
def normalize_string(s):
    for row in s:
        row[1] = row[1].lower().replace(" ", "")
    return s


# When calling getdata.py, it will return a list of lists using functions above to get data from the spreadsheet using the most recent sheet title
def get_data_from_most_recent_sheet():
    sheet = get_most_recent_sheet_title()
    # return get_data(sheet)
    data = get_data(sheet)
    padded_data = data_cleaning(data)
    # return padded_data
    filtered_data = filter_data(padded_data)
    # return filtered_data
    s = normalize_string(filtered_data)
    return s

