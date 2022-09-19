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
    index = 0
    if(columntype == 'pumpvelocity'):
        index = 0
    if(columntype == 'pressure'):
        index = 1

    if(columntype == 'timestamp'):
        index = 2

    
    for k in range(1,worksheet.row_count+1 ):
        # print((worksheet.row_values(k))[index])
        if((worksheet.row_values(k))[index] == columnval):
            # print("yes")
            worksheet.update_cell(k,1,rowdata[0])
            worksheet.update_cell(k,2,rowdata[1])
            worksheet.update_cell(k,3,rowdata[2])

def getRecord(columntype,columnval):
    index = 0
    if(columntype == 'pumpvelocity'):
        index = 0
    if(columntype == 'pressure'):
        index = 1

    if(columntype == 'timestamp'):
        index = 2

    
    for k in range(1,worksheet.row_count+1 ):
        # print((worksheet.row_values(k))[index])
        if((worksheet.row_values(k))[index] == columnval):
            print(worksheet.row_values(k))
            return k
            


addData([55,45,22])      
updateData('timestamp','33',[11,11,11])
getRecord('timestamp','17')


