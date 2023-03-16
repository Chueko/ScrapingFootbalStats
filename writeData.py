from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

#To set all access to read
def update_spreadsheet_permission(drive_service, spreadsheet_id, type, role):
    new_file_permission = {
        'type': type,
        'role': role
    }

    permission_response = drive_service.permissions().create(
        fileId=spreadsheet_id, body=new_file_permission).execute()

    return permission_response

#Set titles and load data for reference
def setTitles():

    load_dotenv()
    KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    SPREADSHEET_ID=os.getenv('SPREADSHEET_ID')

    SCOPES=['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(KEY,scopes=SCOPES)
    service=build('sheets','v4',credentials=creds)
    try:
        spreadsheet = {
            'properties': {
                'title': 'SoccerStats'
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'Stats'
                    }
                }
            ]
        }
        sheet = service.spreadsheets().create(body=spreadsheet).execute()
        newId=sheet.get('spreadsheetId')
        sheet = service.spreadsheets()
        titles = [['Player','Mins','Goals','Assist','Yel','Red','Shoots','Pass','Aerials','MVP','Rating']]
        result = sheet.values().append(spreadsheetId=newId,range='Stats!A1',valueInputOption='USER_ENTERED',body={'values':titles}).execute()

        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = service_account.Credentials.from_service_account_file(KEY,scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        
        update_spreadsheet_permission(service, newId, 'anyone', 'reader')
        print(f"https://docs.google.com/spreadsheets/d/{newId}/edit#gid=0")
        return newId
    except HttpError as error:
        print('Error on create Spreadsheet: {0}'.format(error.content))
    

def writeData(values,newId):
    load_dotenv()
    KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    SPREADSHEET_ID=newId
    SCOPES=['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(KEY,scopes=SCOPES)
    service=build('sheets','v4',credentials=creds)
    sheet = service.spreadsheets()
    data = [values]
    result = sheet.values().append(spreadsheetId=newId,range='Stats!A1',valueInputOption='USER_ENTERED',body={'values':data}).execute()
        







    

