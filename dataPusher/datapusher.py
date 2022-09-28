import gspread
import numpy as np
#authorization
service_account = gspread.service_account(filename = 'capstone-362722-f3745d9260b7.json' )
worksheet = service_account.open('TeamLiftCyberPhysical').sheet1
rows = worksheet.row_count

print(rows)
def addData(rowEntry):
    worksheet.append_row(rowEntry)
def updateData(columntype,columnval,rowdata):
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

    
    for k in range(0,num_rows):
        # print((worksheet.row_values(k))[index])
        if((full_data[k])[index] == columnval):
            # print("yes")
            worksheet.update_cell(k+1,1,rowdata[0])
            worksheet.update_cell(k+1,2,rowdata[1])
            worksheet.update_cell(k+1,3,rowdata[2])

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

    
    for k in range(0,num_rows):
        # print((worksheet.row_values(k))[index])
        if((full_data[k])[index] == columnval):
            # print("yes")
            print(full_data[k])
            return k


   
# addData([55,45,22])         
# updateData('pressure','8',[1,7,0])
getRecord('pumpvelocity','1')



