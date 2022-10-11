import gspread
import numpy as np
from datetime import date
from datetime import datetime
import pytz
from oauth2client.service_account import ServiceAccountCredentials
import requests
#authorization
service_account = gspread.service_account(filename = 'capstone-362722-f3745d9260b7.json' )
worksheet = service_account.open('TeamLiftCyberPhysical').sheet1
rows = worksheet.row_count

scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
credentials = ServiceAccountCredentials.from_json_keyfile_name('capstone-362722-f3745d9260b7.json', scope)
gc = gspread.authorize(credentials)
wb = gc.open_by_url('https://docs.google.com/spreadsheets/d/10g0fkjjrK0k9sa_ynw3O0Stdfp3leNJiJWS0MOM_b94/edit#gid=0')

#this function gets the last time the spreadsheet was updated
def getLastTimeModified():
    revisions_uri = f'https://www.googleapis.com/drive/v3/files/{wb.id}/revisions'
    headers = {'Authorization': f'Bearer {credentials.get_access_token().access_token}'}
    response = requests.get(revisions_uri, headers=headers).json()
    return response['revisions'][-1]['modifiedTime']
#this global contsant refers to the last time the spreadhseet was updated
last_mod_time = getLastTimeModified()

#this function simulates receiving an acknowledgement of the spreadsheets file being updated
def receiveAck():
    global last_mod_time
    current_time = getLastTimeModified()
    print("last  ",  last_mod_time)
    print("last  ",  current_time)
#compares the last time spreadsheet was updated, to the newly obtained value of the last updated time
#if these two values differ, that means spreadsheet has been updated
    if(current_time != last_mod_time):
        last_mod_time = current_time
        print("Modified at ",  current_time)
    


print(rows)
#this function adds data row to spreadsheets with given params
def addData(rowEntry):
    worksheet.append_row(rowEntry)
   

#sends a csv file line by line to the spreadhseets file on the cloud
def sendFile():

    data_file = open('data.txt','r+')
    lines= data_file.readlines()
    for line in lines:
        line = line.split(',')
        for iterator in range(len(line)):
            line[iterator] = float(line[iterator])
        addData(line)
    receiveAck()
    
    



        # timezone_oregon = pytz.timezone('US/Pacific')
        # time_now = (datetime.now(timezone_oregon)).strftime('%Y-%m-%d %H:%M:%S')
        # print("Data Was Updated at " + str(time_now) )





#this function updates a row in the spreadsheets file, by looking up the value of a column
#parameter columtype is the column of the data we are updating
#column val is the value of the column to look for
#rowdata is the new data that we are updating it to
def updateData(columntype,columnval,rowdata):
    #gets all the tabulated data is a 2D array
    full_data = worksheet.get_all_values()
   
    # print(full_data)
    num_rows = len(full_data)
    index = 0
    #depending on the columntype, we assign an index, 
    #this index tells us which column to look inside of
    if(columntype == 'pumpvelocity'):
        index = 0
    if(columntype == 'pressure'):
        index = 1

    if(columntype == 'timestamp'):
        index = 2

    #iterates through data
    for k in range(0,num_rows):
        # print((worksheet.row_values(k))[index])
        #finds the row with the target value
        #updates that row's data with new values
        if((full_data[k])[index] == columnval):
            # print("yes")
            worksheet.update_cell(k+1,1,rowdata[0])
            worksheet.update_cell(k+1,2,rowdata[1])
            worksheet.update_cell(k+1,3,rowdata[2])
    receiveAck()

   




#this method fetches a data point given the value of a certain column
#for example it might search the data point where flow is equal to 55
def getRecord(columntype,columnval):
    full_data = worksheet.get_all_values()
   
    # print(full_data)
    num_rows = len(full_data)
    index = 0
    if(columntype == 'pumpvelocity'):
        index = 0
    if(columntype == 'pressure'):
        index = 1

    if(columntype == 'timestamp'):
        index = 2

    #iterates through data and returns data point that has certain value
    for k in range(0,num_rows):
        # print((worksheet.row_values(k))[index])
        if((full_data[k])[index] == columnval):
            # print("yes")
            print(full_data[k])
            return k




def start(): 
    # addData([55,45,22])         
    # updateData('pumpvelocity','44',[11,11,11])
    # getRecord('pumpvelocity','1')
    sendFile()
    sendFile()
    # getLastTimeModified()
    # receiveAck()
start()
