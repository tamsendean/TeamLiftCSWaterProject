import gspread
import numpy as np
#authorization
service_account = gspread.service_account(filename = 'capstone-362722-f3745d9260b7.json' )
worksheet = service_account.open('TeamLiftCyberPhysical').sheet1
rows = worksheet.row_count

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
        addData(line)



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


   
# addData([55,45,22])         
# updateData('pressure','8',[1,7,0])
# getRecord('pumpvelocity','1')
sendFile()


