import matplotlib   #The information for matplotlib can be found here - https://www.w3schools.com/python/matplotlib_pyplot.asp
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 # The information for sqlite3 can be found here - https://docs.python.org/3/library/sqlite3.html
from appJar import gui #The information for appJar can be found here - http://appjar.info/
import time #The information for the time library  can be found here - https://docs.python.org/3/library/time.html
import time as mytime
import calendar  #The information for the calendar library  can be found here - https://docs.python.org/3/library/calendar.html#module-calendar 
import datetime #The information for the datetime library - https://docs.python.org/3/library/datetime.html#module-datetime
#from datetime import date
con=sqlite3.connect('PatientTransferAudit.db') # creates a new file 
cur=con.cursor()


app=gui("PatientTransferAudit")


def setupDB():
   
    #This creates the nurse table in the DB
    cur.execute("""CREATE TABLE IF NOT EXISTS "tbl_Nurse" (
                "NurseID"	INTEGER NOT NULL UNIQUE,
                "username"	TEXT NOT NULL UNIQUE,
                "password"	TEXT NOT NULL,
                PRIMARY KEY("NurseID" AUTOINCREMENT)
    )""")
               
    con.commit()
    #This creates the Daily audit table in the DB
    cur.execute("""CREATE TABLE "tbl_Daily" (
	"ConsultantID"	TEXT NOT NULL,
	"WardID"	TEXT NOT NULL,
	"RoomID"	TEXT NOT NULL,
	"TimeOfAdmission"	time NOT NULL,
	"TransferDate"	date NOT NULL,
	"TransferTime"	time NOT NULL,
	"ReasonForTransfer"	INTEGER NOT NULL,
	"Comments"	TEXT NOT NULL,
	"Month"	TEXT NOT NULL


    )""")

    con.commit()
                
    #This creates the CurrentMonth table in the DB
    cur.execute("""CREATE TABLE "tbl_CurrentMonth" (
	"ConsultantID"	TEXT NOT NULL,
	"wardID"	TEXT NOT NULL,
	"RoomNo"	INTEGER NOT NULL,
	"TimeOfAdmission"	time NOT NULL,
	"TransferDate"	date NOT NULL,
	"TransferTime"	time NOT NULL,
	"ReasonsforTransfer"	INTEGER NOT NULL,
	"Comments"	TEXT,
	"Month"	TEXT NOT NULL






    )""")
    con.commit()



    #This creates the RoomNo table in the DB
    cur.execute("""CREATE TABLE IF NOT EXISTS  "tbl_RoomNo" (
                    "RoomNo"	INTEGER NOT NULL UNIQUE,
                    "ConsultantID"	TEXT NOT NULL,
                    "NurseID"	INTEGER NOT NULL UNIQUE,
                    PRIMARY KEY("RoomNo"),
                    FOREIGN KEY("ConsultantID") REFERENCES "tbl_Consultant"("ConsultantID"),
                    FOREIGN KEY("NurseID") REFERENCES "tbl_Nurse"("NurseID")
    )""")
    con.commit()



    #This creates the Ward table in the DB 
    cur.execute("""CREATE TABLE IF NOT EXISTS  "tbl_Ward" (
                    "WardID"	TEXT NOT NULL,
                    "ConsultantID"	TEXT NOT NULL,
                    "wardName"	TEXT NOT NULL UNIQUE,
                    PRIMARY KEY("WardID"),
                    FOREIGN KEY("ConsultantID") REFERENCES "tbl_RoomNo"("ConsultantID")
    )""")
    con.commit()



    #This creates the Admission table in the DB
    cur.execute("""CREATE TABLE IF NOT EXISTS  "tbl_Admission" (
                "WardID"	TEXT NOT NULL,
                "RoomNo"	INTEGER NOT NULL UNIQUE,
                "TransferDate"	date NOT NULL,
                "TransferTime"	time NOT NULL,
                "ReasonForTransfer"	INTEGER NOT NULL,
                FOREIGN KEY("RoomNo") REFERENCES "tbl_RoomNo"("RoomNo"),
                FOREIGN KEY("WardID") REFERENCES "tbl_Ward"("WardID")
    )""")
    con.commit()

    #This creates the Consultant table in the DB
    cur.execute("""CREATE TABLE IF NOT EXISTS  "tbl_Consultant" (
                "ConsultantID"	TEXT NOT NULL,
                "Speciality "	TEXT NOT NULL,
                "RoomNo"	INTEGER NOT NULL,
                PRIMARY KEY("ConsultantID")
                )""")
    con.commit()





    #populates Nurse table with logins
    NurseCredentialsFile=open("NurseCredentials.csv","r")#Information added from NurseCrendentials csv file
    for line in NurseCredentialsFile:
        line=line.strip()#removes \n
        userName,passWord=line.split(",")
        cur.execute("INSERT INTO tbl_Nurse (username,password) VALUES (?,?)",[userName,passWord])


        con.commit()#all changes are commited
        print("Database Setup Complete")



    #populates Consultant table with their initials and their speciality
    ConsultantDetailsFile=open("ConsultantDetails.csv","r")#Information added from ConsultantDetails csv file
    for line in ConsultantDetailsFile:
        line=line.strip()#removes\n
        cID,Speciality,roomNo=line.split(",")
        cur.execute("INSERT INTO tbl_Consultant VALUES (?,?,?)",[cID,Speciality,roomNo])

        con.commit()#all changes are commited
        print("Database Setup Complete")




#setupDB()







#creates functions for each of my buttons on every page of my program
def press(button):

    if button=="Login":
        validLogin()#runs subroutine to check if username and password is valid
    
      
        
    elif button=="Forgot Login":
        app.infoBox("Help","Contact 216298@kingsmead.org for more information or any quieries reqarding your credentials")

    elif button=="ButtonPD":
        app.hideSubWindow("MainMenu")#hides main menu
        app.showSubWindow("YearDisplayPD")#shows YearPD page
        retrive_tbl_Daily()
        
       
        
 
        

    elif button=="ButtonAG":
        app.hideSubWindow("MainMenu")#hides main menu
        app.showSubWindow("YearDisplayAG")


    elif button=="backYPD":
        app.hideSubWindow("YearDisplayPD")#hides YearPD page
        app.showSubWindow("MainMenu")#shows main menu
       


    elif button=="backYAG":
        app.hideSubWindow("YearDisplayAG")#hides YearAG page 
        app.showSubWindow("MainMenu")#shows main menu

    elif button=="backMAG":
        app.hideSubWindow("MonthDisplayAG")#hides MonthAG page
        app.showSubWindow("YearDisplayAG")#shows YearAG page

        
#Allows each year selected to direct to the same month page of Patient Data
    elif button=="PD_2023" or button=="PD_2024" or button=="PD_2025" or button=="PD_2026":
        app.hideSubWindow("YearDisplayPD")#hides YearPD page
        app.showSubWindow("MonthDisplayPD")#shows MonthPD page
        
       
    
#Allows each year selected to direct to the same month page of audit graphs 
    elif button=="AG_2023" or button=="AG_2024" or button=="AG_2025" or button=="AG_2026":
        app.hideSubWindow("YearDisplayAG")#hides YearAG page
        app.showSubWindow("MonthDisplayAG")#shows MonthPD page

        
    elif button=="backMPD":
        app.hideSubWindow("MonthDisplayPD")#hides MonthPD page
        app.showSubWindow("YearDisplayPD")#shows YearPD page


    elif button=="backMAG":
        app.hideSubWindow("MonthDisplayAG")#hides MonthAG page
        app.showSubWindow("YearDisplayAG")#shows YearAG page



    elif button=="PD_January" or button=="PD_February" or button=="PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December":
        app.hideSubWindow("MonthDisplayPD")
        app.showSubWindow("PatientTransferDatabases")
        set_month_to_add_row(button)#sets row[8] of grids ro the month of the button clicked
        month_check(button)#checks if row[8] in grid already has the month name
        AuditGraph()#calculates graph summaries
        ConsultantGraph()#Calculates consultant graph data
        
    
        
    

    elif button=="Daily":
        app.hideSubWindow("PatientTransferDatabases")
        app.showSubWindow("DailyDatabase")

    

    
    elif button=="Current Month Database":
        app.hideSubWindow("PatientTransferDatabases")
        app.showSubWindow("CurrentMonthDatabase")
        

    elif button=="BackPTD":
        app.hideSubWindow("PatientTransferDatabases")
        app.showSubWindow("MonthDisplayPD")# switch back to previous subwindow

    elif button=="BackDD":
        app.hideSubWindow("DailyDatabase")
        app.showSubWindow("PatientTransferDatabases")# switch back to previous subwindow

    elif button=="BackCD":
        app.hideSubWindow("CurrentMonthDatabase")
        app.showSubWindow("PatientTransferDatabases")# switch back to previous subwindow

    elif button=="BackAGP":
        app.hideSubWindow("AuditGraphs")
        app.showSubWindow("MonthDisplayAG")# switch back to previous subwindow

    elif button=="VGS":
        GraphSummary()#shows graph summaries
        app.hideSubWindow("AuditGraphs")
        app.showSubWindow("GraphSummary")

    elif button=="CG":
        app.hideSubWindow("AuditGraphs")
        PlotConsultantGraph()#plots consultant graph
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow
    

    elif button=="BackGS":
        app.hideSubWindow("GraphSummary")
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="January":
        app.hideSubWindow("AuditGraphs")
        MonthlyGraph()
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="February":
        app.hideSubWindow("AuditGraphs")
        MonthlyGraph()
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="March":
        app.hideSubWindow("AuditGraphs")
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="April":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="May":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="June":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="July":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="August":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="September":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="October":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="November":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow

    elif button=="December":
        MonthlyGraph() 
        app.showSubWindow("AuditGraphs")# switch back to previous subwindow
        

#Allows the month clicked on the selection page to display the button required to present that graph
def monthGraph(button):

    if  button=="AG_January":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.setPadding([40,40])
        app.addNamedButton("January's graph","January",press,1,0)
        app.setButtonBg("January", "lightblue")
        

    elif button=="AG_February":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("February's graph","February",press,1,0)
        app.setButtonBg("February", "lightblue")

    elif button=="AG_March":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("March's graph","March",press,1,0)
        app.setButtonBg("March", "lightblue")


    elif button=="AG_April":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("April's graph","April",press,1,0)
        app.setButtonBg("April", "lightblue")
        
    elif button=="AG_May":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("May's graph","May",press,1,0)
        app.setButtonBg("May", "lightblue")


    elif button=="AG_June":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("June's graph","June",press,1,0)
        app.setButtonBg("June", "lightblue")


    elif button=="AG_July":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("July's graph","July",press,1,0)
        app.setButtonBg("July", "lightblue")

    elif button=="AG_August":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("August's graph","August",press,1,0)
        app.setButtonBg("August", "lightblue")

    elif button=="AG_September":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("September's graph","September",press,1,0)
        app.setButtonBg("September", "lightblue")


    elif button=="AG_October":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("October's graph","October",press,1,0)
        app.setButtonBg("October", "lightblue")


    elif button=="AG_Novemeber":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("November's graph","November",press,1,0)
        app.setButtonBg("November", "lightblue")


    elif button=="AG_December":
        app.hideSubWindow("MonthDisplayAG")
        app.showSubWindow("AuditGraphs")
        app.setSticky("w")#sets the months button to the left side of the screen
        app.addNamedButton("December's graph","December",press,1,0)
        app.setButtonBg("December", "lightblue")

        
        app.stopSubWindow()#stops subwindow


    
        

#creates a function so the user can logout         
def logout(leave):

    leave = app.questionBox("Log Out","Are you sure you want to log out?")
    if leave==True:#checks if conditon is true and then open the MainMenu subwindow
        app.hideSubWindow("MainMenu")
        app.showSubWindow("Login")
        

    else:
        app.showSubWindow("MainMenu")


#isalnum = alphabet and number
#is alpha = checks all characters is alphabet
#is digit = checks digit only

#mypassword[0].isupper()
#Allows user to only login if they enter valid inputs that match the value stored in the database
def validLogin():
    global hidden_password
    username = app.getEntry("Username :")#sets username variable to the username entered by the user
    #password can be written in either hidden or visible mode
    hidden_password = app.getEntry("hiddenPassword")#hidden  password
    visible_password = app.getEntry("visiblePassword")#visible password 
    cur.execute("SELECT password FROM tbl_Nurse WHERE username=?", [username])#selects password from the database associated with the  entered username 
    result=cur.fetchone()#fetches the passwords from the queried username in the database and stores it in the variable result 
    print(result,hidden_password,visible_password)
    if len(hidden_password)==0 and len(visible_password)!=0:
        hidden_password=visible_password#if hidden password is empty visible password can be stored as the hidden password
    if len(visible_password)==0 and len(hidden_password)!=0:
        visible_password=hidden_password#if visible password is empty hidden password can be stored as the visible password

#Checks username or password field is empty 
    if len(username)== 0 or (len(hidden_password)== 0 or len(visible_password)== 0):
        app.errorBox("Access denied","Username or Password not present")
#Checks username is 6 characters long 
    elif len(username)!=6:
        app.errorBox("Access denied","Username not 6 characters long")
#If either password entry box is not 8 characters long user is denied
    elif len(hidden_password)!=8 and len(visible_password)!=8:
        app.errorBox("Access denied","Password not 8 characters long")

#Checks either password entry boxes have a capital letter 

    elif hidden_password[0].islower() or visible_password[0].islower():
        app.errorBox("Access denied","Password not in correct format")

#Makes sure the only way to login is if the username and password matches exactly
    elif result==None or (result[0]==username or (result[0]!=hidden_password  or result[0]!=visible_password)):
         app.errorBox("Access denied","Username or Password is incorrect")
        
#if credentials are valid user can login successfully     
    else:
        if result[0]==hidden_password  or result[0]==visible_password:
            app.hideSubWindow("Login")#User may login as details are correct
            app.clearEntry("visiblePassword")#clears password entry when user logs in 
            app.clearEntry("hiddenPassword")
            app.showSubWindow("MainMenu")#Shows the MainMenu
            app.unbindKey("Return")
            


def set_month_to_add_row(button):
    global month_in_new_row#makes global variable for each month from press(button)
    if button == "PD_January":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns    
        month_in_new_row[8] = "January"#sets index[8] column to "January"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)

    if button == "PD_February":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns  
        month_in_new_row[8] = "February"#sets index[8] column to "February"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)
        
    if button == "PD_March":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "March"#sets index[8] column to "March"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)
        
    if button == "PD_April":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "April"#sets index[8] column to "April"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)

    if button == "PD_May":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "May"#sets index[8] column to "May"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)

    if button == "PD_June":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "June"#sets index[8] column to "June"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)
 
    if button == "PD_July":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "July"#sets index[8] column to "July"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)
     
    if button == "PD_August":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "August"#sets index[8] column to "August"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)


    if button == "PD_September":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "September"#sets index[8] column to "September"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)


    if button == "PD_October":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "October"#sets index[8] column to "October"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)

    if button == "PD_November":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "November"#sets index[8] column to "November"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)

    if button ==  "PD_December":
        month_in_new_row = [""] * 9#create a list with empty strings for all columns   
        month_in_new_row[8] = "December"#sets index[8] column to "December"
        btn = True#set btn = true so addGridRow() can now take place
        addGridRowg1(btn)



def check_Row_Inputs_g1(btn):

    data = app.getGridRow("g1", btn)#gets inputs from the row and stores it in the variable data
    print(data)
    if data is None:
            print("No data")#prints no data if row is empty
    else:
        for row in data:
            print(row)
            if any(row):#for any row in the table
                    consultant_id = data[0]#assigns each row index to the corresponding field name
                    ward_id = data[1]
                    Room_ID = data[2]
                    Time_Of_Admission = data[3]
                    transfer_date = data[4]
                    transfer_time = data[5]
                    reason_for_transfer = data[6]
                    comments = data[7]
                    Month = data[8]

#isalnum = alphabet and number

    if  consultant_id == ""  or (not consultant_id.isalnum()):#print error message if ConsultantID cell is empty or contains a symbol
         app.errorBox("Cannot save","ConsultantID is empty or contains erroneous data")
         return False#sets subroutine to false

    elif ward_id == "" or (not ward_id.isdigit()):#print error message if wardID cell is empty or not an integer
         app.errorBox("Cannot save","WardID is not a number")
         return False#sets subroutine to false

    elif Room_ID == "" or (not Room_ID.isdigit()) or len(Room_ID)>3:#print error message if RoomID cell is empty or not an integer or there is more than 3 integers
         app.errorBox("Cannot save","Room ID is not a number")
         return False#sets subroutine to false

    elif reason_for_transfer == "" or (not reason_for_transfer.isdigit()):#print error message if ReasonForTransfer cell is empty or not an integer
        app.errorBox("Cannot save","Reason for transfer is not a number")
        return False#sets subroutine to false

    elif int(reason_for_transfer)<1 or int(reason_for_transfer)>6 :#print error message if ReasonForTransfer cell value is not between 1 and 6
        app.errorBox("Cannot save","Reason for transfer integer is out of the key's range")
        return False#sets subroutine to false
    
    try:
        datetime.datetime.strptime(Time_Of_Admission, '%H:%M')#print error message if Time_Of_Admission is empty or the time is not in HH/MM format
    except ValueError:#if right type but inappropiate value used run except clause 
        app.errorBox("Cannot save","TimeOfAdmission is not in HH:MM format")
        return False#sets subroutine to false

    try:
        datetime.datetime.strptime(transfer_date, '%d/%m/%y')#print error message if TransferDate is empty or the date is not in DD/MM/YY format
    except ValueError:#if right type but inappropiate value used run except clause 
        app.errorBox("Cannot save","TransferDate is not in DD/MM/YY format")
        return False#sets subroutine to false

    try:
        datetime.datetime.strptime(transfer_time, '%H:%M')#print error message if TransferTime is empty or the time is not in HH/MM format
    except ValueError:#if right type but inappropiate value used run except clause 
        app.errorBox("Cannot save","TransferTime is not in HH:MM format")#sets subroutine to false
        return False


    return True 



def check_Row_Inputs_g2(btn):

    data = app.getGridRow("g2", btn)#gets inputs from the row and stores it in the variable data
    print(data)
    if data is None:
            print("No data")#prints no data if row is empty
    else:
        for row in data:
            print(row)
            if any(row):#for any row in the table
                    consultant_id = data[0]#assigns each row index to the corresponding field name
                    ward_id = data[1]
                    Room_ID = data[2]
                    Time_Of_Admission = data[3]
                    transfer_date = data[4]
                    transfer_time = data[5]
                    reason_for_transfer = data[6]
                    comments = data[7]
                    Month = data[8]




#isalnum = alphabet and number

    if  consultant_id == ""  or (not consultant_id.isalnum()):
         app.errorBox("Cannot save","ConsultantID is empty or contains erroneous data")#print error message if ConsultantID cell is empty or contains a symbol
         return False#sets subroutine to false
 
    elif ward_id == "" or (not ward_id.isdigit()):#print error message if wardID cell is empty or not an integer
         app.errorBox("Cannot save","WardID is not a number")
         return False#sets subroutine to false
    
    elif Room_ID == "" or (not Room_ID.isdigit()) or len(Room_ID)>3:#print error message if RoomID cell is empty or not an integer or there is more than 3 integers
         app.errorBox("Cannot save","Room ID is not a number")
         return False#sets subroutine to false

    elif reason_for_transfer == "" or (not reason_for_transfer.isdigit()):#print error message if ReasonForTransfer cell is empty or not an integer
        app.errorBox("Cannot save","Reason for transfer is not a number")
        return False#sets subroutine to false


    elif int(reason_for_transfer)<1 or int(reason_for_transfer)>6 :#print error message if ReasonForTransfer cell value is not between 1 and 6
        app.errorBox("Cannot save","Reason for transfer integer is out of the key's range")
        return False#sets subroutine to false

    try:
        datetime.datetime.strptime(Time_Of_Admission, '%H:%M')#print error message if Time_Of_Admission is empty or the time is not in HH/MM format
    except ValueError:#if right type but inappropiate value used run except clause 
        app.errorBox("Cannot save","TimeOfAdmission is not in HH:MM format")
        return False#sets subroutine to false

    try:
        datetime.datetime.strptime(transfer_date, '%d/%m/%y')#print error message if TransferDate is empty or the date is not in DD/MM/YY format
    except ValueError:#if right type but inappropiate value used run except clause 
        app.errorBox("Cannot save","TransferDate is not in DD/MM/YY format")
        return False#sets subroutine to false

    try:
        datetime.datetime.strptime(transfer_time, '%H:%M')#print error message if TransferTime is empty or the time is not in HH/MM format
    except ValueError:#if right type but inappropiate value used run except clause 
        app.errorBox("Cannot save","TransferTime is not in HH:MM format")#sets subroutine to false
        return False


    return True 
 
def addGridRowg1(btn):
    
    rows = app.getGridRowCount("g1")
    for i in range(rows):
        row = app.getGridRow("g1", i)
        row[8] = month_in_new_row[8] # set the 9th column (index 8) to the value of month_in_new_row
        app.replaceGridRow("g1", i, row)#replace original row with updated version 





    rows = app.getGridRowCount("g1")#count number of rows in g1  
    if rows == 0:
        app.addGridRow("g1", month_in_new_row)#add current month to row[8] if theres no rows at all
    else:
        for i in range(rows):
            row = app.getGridRow("g1", i)#gets each individual row
            if not any(row):#checks if each field row is empty
                continue#if the row is not empty then continue
            if row[8] != month_in_new_row[8]:#checks if row[8] already contains the current month
                row[8] = month_in_new_row[8]#if not assign row[8] to the current month
                app.replaceGridRow("g1", i, row)#Replaces the row with the updated changes

             
        else:
            app.addGridRow("g1", month_in_new_row)#if no rows have an empty row[8] add new row to grid with the corresponding month


def addGridRowg2(btn):
    
    rowsg2 = app.getGridRowCount("g2")#count number of rows in g2
    row = app.getGridRow("g2", 0)#gets the first row in g2
    if row[8] != month_in_new_row[8] or row[8] == month_in_new_row[8]:#checks if row[8] already contains the current month or if it does not 
               row[8] = month_in_new_row[8]#if not assign row[8] to value in month_in_new_row
               app.addGridRow("g2", month_in_new_row)#add grid row containing displaying the value in month_in_new_row in row[8]    




    


def SaveTableg1(btn):

    if not check_Row_Inputs_g1(btn):#if the check_Row_Inputs_g1(btn) subroutine is false this function will not execute the following code
        return 
    save = app.yesNoBox("Save transfer", "Are you sure you want to add this patient transfer? ALL CHANGES ARE FINAL!!",)

    if save==True:
        data = app.getGridRow("g1", btn)#gets inputs from the row and stores it in the variable data
        print(data)
        if data is None:
            print("No data")#prints no data if row is empty
        else:
            for row in data:
                print(row)
                if any(row):#for any row in the table
                        consultant_id = data[0]#assigns each row index to the corresponding field name
                        ward_id = data[1]
                        Room_No = data[2]
                        Time_Of_Admission = data[3]
                        transfer_date = data[4]
                        transfer_time = data[5]
                        reason_for_transfer = data[6]
                        comments = data[7]
                        Month = data[8]




        
        conn = sqlite3.connect('PatientTransferAudit.db')#connect db
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl_Daily (ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)", (consultant_id, ward_id, Room_No, Time_Of_Admission, transfer_date, transfer_time, reason_for_transfer, comments,Month))
        conn.commit()#commits all changes into the tbl_Daily in my database 
        print("complete")
    else:
        
        app.showSubWindow("DailyDatabase")



def SaveTableg2(btn):

    if not check_Row_Inputs_g2(btn):#if the check_Row_Inputs_g2(btn) subroutine is false this function will not execute the following code
        return
    save = app.yesNoBox("Save transfer 2", "Are you sure you want to add this patient transfer to this month? ALL CHANGES ARE FINAL!!",)

    if save==True:
        data = app.getGridRow("g2", btn)#gets inputs from the row and stores it in the variable data
        print(data)
        if data is None:
            print("No data")#prints no data if row is empty
        else:
            for row in data:
                print(row)
                if any(row):#for any row in the table
                        consultant_id = data[0]#assigns each row index to the corresponding field name
                        ward_id = data[1]
                        Room_No = data[2]
                        Time_Of_Admission = data[3]
                        transfer_date = data[4]
                        transfer_time = data[5]
                        reason_for_transfer = data[6]
                        comments = data[7]
                        Month = data[8]
        conn = sqlite3.connect('PatientTransferAudit.db')#connect db
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl_CurrentMonth (ConsultantID, WardID, RoomNo, TimeOfAdmission, TransferDate, TransferTime, ReasonsforTransfer, Comments, Month) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)", (consultant_id, ward_id, Room_No, Time_Of_Admission, transfer_date, transfer_time, reason_for_transfer, comments,Month))
        conn.commit()#commits all changes into the tbl_CurrentMonth in my database 
        print("complete")

    else:
        
        app.showSubWindow("CurrentMonthDatabase")

    
    


    
def retrive_tbl_Daily():
    conn = sqlite3.connect('PatientTransferAudit.db')#connect db
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tbl_daily")#counts all the rows in the table
    row_count = cur.fetchone()[0]#stores number of rows in the variable row_count
    if row_count != 0:
        today = datetime.date.today()#gets todays date
        print(today)
        if today.month == 1:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='January'")#selects all rows with data from the table with the month January
        elif today.month == 2:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='February'")#selects all rows with data from the table with the month February
        elif today.month == 3:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='March'")#selects all rows with data from the table with the month March
        elif today.month == 4:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='April'")#selects all rows with data from the table with the month April
        elif today.month == 5:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='May'")#selects all rows with data from the table with the month May
        elif today.month == 6:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='June'")#selects all rows with data from the table with the month June
        elif today.month == 7:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='July'")#selects all rows with data from the table with the month July
        elif today.month == 8:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='August'")#selects all rows with data from the table with the month August
        elif today.month == 9:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='September'")#selects all rows with data from the table with the month September
        elif today.month == 10:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='October'")#selects all rows with data from the table with the month October
        elif today.month == 11:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='November'")#selects all rows with data from the table with the month November
        elif today.month == 12:
            cur.execute("SELECT ConsultantID, WardID, RoomID, TimeOfAdmission, TransferDate, TransferTime, ReasonForTransfer, Comments, Month FROM tbl_Daily WHERE Month='December'")#selects all rows with data from the table with the month Decem

    

        
    else:
            print("table is empty")



    rows = cur.fetchall()
    headers = ["ConsultantID", "WardID","RoomID", "TimeOfAdmission","TransferDate","TransferTime","ReasonForTransfer","Comments","Month"]#assigns all the titles for each column in the grid to the variable headers
    app.replaceAllGridRows("g1",rows)#replaces all the rows in my grid with the retrived data 
    first_row = app.getGridRow("g1",-1)#stores the first row that is currently in the header in the variable first_row
    app.setGridHeaders("g1",headers)#set the grid headers to the headers of the Daily grid
    app.addGridRow("g1",first_row)#adds the first row to the end of the existing grid
    print(rows)


def month_check(button):
   rowsg1 = app.getGridRowCount("g1")
   today = datetime.date.today() #gets today's date
   print(today)
   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and (today.month ==1):#checks if the current month is january
           for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "January":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!=January
               else:
                   return TransferDailyTable(button)
                   
                   
   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 2:#checks if the current month is February
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "February":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!=February
               else:
                    return TransferDailyTable(button)

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 3:#checks if the current month is March
             print("printing",rowsg1)
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                continue # skip empty rows
               if row[8] != "March":
                   print("creating blank rows")
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!=March
               else:
                     return TransferDailyTable(button)
                  
                
                      
                

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 4:#checks if the current month is April
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "April":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!=April
               else:
                   #pass
                   return TransferDailyTable(button)
                   
                  
                    

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 5:#checks if the current month is May
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "May":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!=May
               else:
                   return TransferDailyTable(button)
                          


   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 6:#checks if the current month is June
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "June":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!=June
               else:
                   return TransferDailyTable(button)
                  



   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 7:#checks if the current month is July
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "July":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!=July
               else:
                   return TransferDailyTable(button)
                   

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 8:#checks if the current month is August
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "August":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!= August
               else:
                   return TransferDailyTable(button)
                   

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 9:#checks if the current month is September 
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "September":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!= September
               else:
                   return TransferDailyTable(button)
                  

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 10:#checks if the current month is October
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "October":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#add empty rows to the grid if the row[8]!= October
               else:
                    return TransferDailyTable(button)

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 11:#checks if the current month is November
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "November":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!= November
               else:
                    return TransferDailyTable(button)

   if (button == "PD_January" or button == "PD_February" or button == "PD_March" or button=="PD_April" or button=="PD_May" or button=="PD_June" or button=="PD_July" or button=="PD_August" or button=="PD_September" or button=="PD_October" or button=="PD_November" or button=="PD_December") and today.month == 12:#checks if the current month is December
             for i in range(rowsg1):
               row = app.getGridRow("g1", i)#gets each row in the grid
               print(row)
               if all(val == "" for val in row):
                  continue # skip empty rows
               if row[8] != "December":
                   empty_row = [""] * 9#creates an empty list of 9 values 
                   app.replaceGridRow("g1", i, empty_row)#adds the empty rows to the grid if the row[8]!= December
               else:
                   return TransferDailyTable(button)
                                                           


        
def TransferDailyTable(button):
    seconds = time.time()#gets the current time in seconds
    local_time = time.ctime(seconds)#converts the time in seconds into a readable format
    print("Local time:", local_time)#prints the readable time
    current_time = time.localtime()#gets the struct_time function in format(year, month, day, hour, minute, second, weekday, day of the year, daylight saving)
    today = datetime.date.today() #gets today's date
    print(today)
    hour = time.strftime("%H:%M:%S",current_time)#puts the current time in H/M/S format
    str_hour = (str(hour))#makes hour variable a string
    str_hour=str_hour.strip()
    hour,minute,second=str_hour.split(":")#splits the time into single integers of hour,minute and second
    if hour >="19" and hour <"20":#if hour is between 7pm and 8pm run the funtion
        print("hey")
        rows = app.getGridRowCount("g1")#gets number of rows with data
        for i in range(rows):
            row = app.getGridRow("g1", i)
            print(row)
            print(rows)
            rowData=[]#empty list to transfer data
            for eachRow in row:
             if any(row):#for any row in the table
                        consultant_id = row[0]#assigns each row index to the corresponding field name
                        ward_id = row[1]
                        Room_No = row[2]
                        Time_Of_Admission = row[3]
                        transfer_date = row[4]
                        transfer_time = row[5]
                        reason_for_transfer = row[6]
                        comments = row[7]
                        Month = row[8]

        conn = sqlite3.connect('PatientTransferAudit.db')#connect db
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl_CurrentMonth (ConsultantID, WardID, RoomNo, TimeOfAdmission, TransferDate, TransferTime, ReasonsForTransfer, Comments , Month) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)", (consultant_id, ward_id, Room_No, Time_Of_Admission, transfer_date, transfer_time, reason_for_transfer,comments,Month)) 
        conn.commit()#commits all changes into the tbl_Daily in my database 
        print("complete")



        for x in range(rows):
                data=app.getGridRow("g1",x)#for each row in the table store values in the variable data
                rowData.append([data])#2D list
        print("row data",rowData)
    

        if row[8] == "January" or row[8] == "Febraury" or row[8] == "March" or row[8] == "April" or row[8] == "May" or row[8] == "June" or row[8] == "July" or row[8] == "August" or row[8] == "September" or row[8] == "October" or row[8] == "November" or row[8] == "December":
            for aList in rowData:#for each list in rowData
                app.addGridRow("g2",aList[0])#adds each list in the 2D list to current month 
                
        print(rows)
        replace_g1 = app.getGridRowCount("g1")#count number of rows in g1
        for i in range(replace_g1):
            app.replaceGridRow("g1",i,"")#for each row replace g1 with empty values



        
MedicalReason_Total = 0 #total for medical reasons
PatientRequest_Total = 0#total for patient requests
LateDischarge_Total = 0#total for late discharges
ConsultantRequest_Total = 0#total for consultant requests
SocialReason_Total = 0#total for social reasons
Other_Total = 0#total for other/unknown reasons
def AuditGraph():
    global MedicalReason_Total#reference the global variables
    global PatientRequest_Total
    global LateDischarge_Total
    global ConsultantRequest_Total
    global SocialReason_Total
    global Other_Total
    seconds = time.time()#gets the current time in seconds
    local_time = time.ctime(seconds)#converts the time in seconds into a readable format
    print("Local time:", local_time)#prints the readable time
    current_time = time.localtime()#gets the struct_time function in format(year, month, day, hour, minute, second, weekday, day of the year, daylight saving)
    hour = time.strftime("%H:%M:%S",current_time)#puts the current time in H/M/S format
    str_hour = (str(hour))#makes hour variable a string
    str_hour=str_hour.strip()
    hour,minute,second=str_hour.split(":")#splits the time into single integers of hour,minute and second
    today = datetime.date.today()#gets todays date
    last_day_of_month = calendar.monthrange(today.year,today.month)[1]#gets the exact number of days in the current month
    print(last_day_of_month)
    date = datetime.date(2023, 4, 30)
    if  today.day == last_day_of_month and today.month == 1 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "January"
    elif today.day == last_day_of_month and today.month == 2 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "February"
    elif today.day == last_day_of_month and today.month == 3 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "March"
    elif today.day == last_day_of_month and today.month == 4 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "April"   
    elif today.day == last_day_of_month and today.month == 5 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "May"
    elif today.day == last_day_of_month and today.month == 6 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "June"
    elif today.day == last_day_of_month and today.month == 7 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "July"
    elif today.day == last_day_of_month and today.month == 8 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "August"
    elif today.day == last_day_of_month and today.month == 9 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "September"
    elif today.day == last_day_of_month and today.month == 10 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "October"
    elif today.day == last_day_of_month and today.month == 11 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "November"
    elif today.day == last_day_of_month and today.month == 12 and (hour >= "20" and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "December"

    print("today is last day")
    rows_g2 = app.getGridRowCount("g2")
    print(rows_g2)
    for x in range(rows_g2):
        data=app.getGridRow("g2",x)#for each row in the table store values in the variable data
        print(data)
        if data and (data[8]==month):
            consultant_id = data[0]#assigns each row index to the corresponding field name
            ward_id = data[1]
            Room_No = data[2]
            Time_Of_Admission = data[3]
            transfer_date = data[4]
            transfer_time = data[5]
            reason_for_transfer = data[6]
            comments = data[7]
            print(reason_for_transfer)


                        
            if "1" in reason_for_transfer:
                MedicalReason_Total+=1 #increment medical reason tally by one

            elif "2" in reason_for_transfer:
                PatientRequest_Total+=1#increment patient request reason tally by one

            elif "3" in reason_for_transfer:
                LateDischarge_Total+=1#increment late discharge reason tally by one

            elif "4" in reason_for_transfer:
                ConsultantRequest_Total+=1#increment consultant request tally by one

            elif "5" in reason_for_transfer:
                SocialReason_Total+=1#increment social reason tally by one
                

            elif "6" in reason_for_transfer:
                Other_Total+=1#increment other reason tally by one


    print("total is " , SocialReason_Total)    
        



new_consultantList = 0#the different consultants in the current month grid
new_reasonsList = 0#the number of patient transfers in the current month grid
def ConsultantGraph():
    seconds = time.time()#gets the current time in seconds
    local_time = time.ctime(seconds)#converts the time in seconds into a readable format
    print("Local time:", local_time)#prints the readable time
    current_time = time.localtime()#gets the struct_time function in format(year, month, day, hour, minute, second, weekday, day of the year, daylight saving)
    hour = time.strftime("%H:%M:%S",current_time)#puts the current time in H/M/S format
    str_hour = (str(hour))#makes hour variable a string
    str_hour=str_hour.strip()
    hour,minute,second=str_hour.split(":")#splits the time into single integers of hour,minute and second
    today = datetime.date.today()#gets todays date
    last_day_of_month = calendar.monthrange(today.year,today.month)[1]#gets the exact number of days in the current month
    print(last_day_of_month)
    date = datetime.date(2023, 4, 30)
    global new_consultantList#refrences global variables to be used outisde the function
    global new_reasonsList#refrences global variables to be used outisde the function
    if  date.day == last_day_of_month and today.month == 1 and (hour >= "20" and hour <="21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "January"
    elif today.day == last_day_of_month and today.month == 2 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "February"
    elif today.day == last_day_of_month and today.month == 3 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        print("hello")
        month = "March"
    elif today.day == last_day_of_month and today.month == 4 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "April"   
    elif today.day == last_day_of_month and today.month == 5 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "May"
    elif today.day == last_day_of_month and today.month == 6 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "June"
    elif today.day == last_day_of_month and today.month == 7 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "July"
    elif today.day == last_day_of_month and today.month == 8 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "August"
    elif today.day == last_day_of_month and today.month == 9 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "September"
    elif today.day == last_day_of_month and today.month == 10 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "October"
    elif today.day == last_day_of_month and today.month == 11 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "November"
    elif today.day == last_day_of_month and today.month == 12 and (hour >= "20" and hour <= "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
        month = "December"

    print("today is last day")
    rows_g2 = app.getGridRowCount("g2")
    print(rows_g2)
    for i in range(rows_g2):
        row=app.getGridRow("g2",i)
        consultants = []#makes an empty list for consultants
        reasons = []#makes an empty list for reasons
        if row and (row[8]==month):#if row[8] is equal to the corresponding month
            for x in range(rows_g2):
                data = app.getGridRow("g2",x)#iterate through the grid and get each row
                consultant_id = data[0]#assigns the first row index to the consultant ID
                reason_for_transfer = data[6]
                consultants.append([consultant_id])#adds data to the new list
                reasons.append([reason_for_transfer])#adds reasons to new list
    print("consultants are", consultants)
    print("reasons are", reasons)
    new_consultantList = [x[0] for x in consultants if x != ['']]#remove any empty values from the created list 
    print(new_consultantList)
    
    new_reasonsList = [x[0] for x in reasons if x != ['']]#remove any empty values from the created list
    print(new_reasonsList)

def PlotConsultantGraph():
    current_time = time.localtime()#gets the struct_time function in format(year, month, day, hour, minute, second, weekday, day of the year, daylight saving)
    hour = time.strftime("%H:%M:%S",current_time)#puts the current time in H/M/S format
    str_hour = (str(hour))#makes hour variable a string
    str_hour=str_hour.strip()
    hour,minute,second=str_hour.split(":")#splits the time into single integers of hour,minute and second
    today = datetime.date.today()#gets todays date
    last_day_of_month = calendar.monthrange(today.year,today.month)[1]#gets the exact number of days in the current month
    date = datetime.date(2023, 4, 30)
    if today.day == last_day_of_month and hour >= "00": #and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month


        
        x = np.array(new_consultantList)#x-axis
        y = np.array(new_reasonsList)#y-axis 


        plt.figure(figsize=(10,6))#size of bar graph
        plt.bar(x, y, color="orange")#plot bar graph and make the bars orange 
        plt.xlabel("Consultants")#labels x axis
        plt.ylabel("Number of patient transfers")#labels y axis  
        plt.show()#show bar graph  

            

def MonthlyGraph():
    current_time = time.localtime()#gets the struct_time function in format(year, month, day, hour, minute, second, weekday, day of the year, daylight saving)
    hour = time.strftime("%H:%M:%S",current_time)#puts the current time in H/M/S format
    str_hour = (str(hour))#makes hour variable a string
    str_hour=str_hour.strip()
    hour,minute,second=str_hour.split(":")#splits the time into single integers of hour,minute and second
    today = datetime.date.today()#gets todays date
    last_day_of_month = calendar.monthrange(today.year,today.month)[1]#gets the exact number of days in the current month
    date = datetime.date(2023, 4, 30)
    if today.day == last_day_of_month and hour >= "00": #and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month
 

        x = np.array(["Medical Reason", "Patient request", "Late Discharge","Consultant Request","Social Reason","Other"])#x-axis
        y = np.array([MedicalReason_Total, PatientRequest_Total, LateDischarge_Total,ConsultantRequest_Total,SocialReason_Total,Other_Total])#y-axis 

        plt.figure(figsize=(10,6))#size of bar graph
        plt.bar(x, y, color="lightblue")#plot bar graph and make the bars orange 
        plt.xlabel("Reason For Transfer")#labels x axis
        plt.ylabel("Number of patient transfers")#labels y axis  
        plt.show()#show bar graph  


max_value = 0#sets max_value to 0 so it can be used as a global variable
highest_category = 0#sets max_value to 0 so it can be used as a global variable
common_consultant = 0#sets max_value to 0 so it can be used as a global variable
def GraphSummary():
    current_time = time.localtime()#gets the struct_time function in format(year, month, day, hour, minute, second, weekday, day of the year, daylight saving)
    hour = time.strftime("%H:%M:%S",current_time)#puts the current time in H/M/S format
    str_hour = (str(hour))#makes hour variable a string
    str_hour=str_hour.strip()
    hour,minute,second=str_hour.split(":")#splits the time into single integers of hour,minute and second
    today = datetime.date.today()#gets todays date
    last_day_of_month = calendar.monthrange(today.year,today.month)[1]#gets the exact number of days in the current month
    date = datetime.date(2023, 4, 30)
    if today.day == last_day_of_month and hour >= "00": #and hour < "21"):#if the day is the last of the month and it is between 8pm and 9pm count the totals for the current month 
        global max_value#makes variables global
        global highest_category
        global common_consultant 
        reasons_for_transfer = {"MedicalReason": MedicalReason_Total,
                                 "PatientRequest": PatientRequest_Total,
                                 "LateDischarge": LateDischarge_Total,
                                 "ConsultantRequest": ConsultantRequest_Total,
                                 "SocialReason": SocialReason_Total,
                                 "Other": Other_Total}#dictionary is made to store the variables with its respected values
        
        highest_reason_for_transfer = max(reasons_for_transfer, key=reasons_for_transfer.get)#key which gets the name of the reason for transfer with the highest value
        highest_number = reasons_for_transfer[highest_reason_for_transfer]#gets the number where the reason for transfer contains the highest value
        
        max_value = highest_number#stores the highest_number in variable max_value
        highest_category = highest_reason_for_transfer#stores the highest_reason_for_transfer in highest_category
        common_consultant = max(new_reasonsList)
        print(max_value)
        print(highest_category)
        app.setLabel("maxVal", max_value)# updates max_value label
        app.setLabel("highest_category",highest_category)#updates highest category label
        app.setLabel("Most Common Consultant",common_consultant)#updates the Most Common Consultant label 
    
def checkPass():
   
    app.hideEntry("visiblePassword")
    app.hideButton("eyehide")
    app.showButton("eye")
    

def showPass(btn):
    app.hideEntry("hiddenPassword")
    pwVar = app.getEntry("hiddenPassword")#sets hidden password variable to password entered by the user 
    app.showEntry("visiblePassword")
    app.setEntry("visiblePassword",pwVar)
    app.showButton("eyehide")
    app.hideButton("eye")
    


def hidePass(btn):
    app.hideEntry("visiblePassword")
    pwVar = app.getEntry("visiblePassword")#sets visible password to hidden password entered by the user 
    app.showEntry("hiddenPassword")
    app.setEntry("hiddenPassword",pwVar)
    app.showButton("eye")
    app.hideButton("eyehide")
  



#creates my interphase for the program 
def createInterface():
################################################################Login page################################################################
    app.startSubWindow("Login")
    app.addLabel("title","DSW Transfer Audit" ,0,1)
    app.getLabelWidget("title").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title", "white")
    app.setLabelFg("title", "blue")
    app.addLabelEntry("Username :",1,1)
    app.addSecretLabelEntry("hiddenPassword",2,1)
    app.setLabel("hiddenPassword","Password :")
    app.addLabelEntry("visiblePassword",2,1)
    app.setLabel("visiblePassword","password:")
    app.addImageButton("eye",showPass,"eye.png",2,2)
    app.addImageButton("eyehide",hidePass,"eyehide.png",2,2)
    app.hideButton("eyehide")
    app.enableEnter(validLogin)#enables the enter button to be used in only the login page 
    checkPass()
    app.setEntryBg("Username :", "lightblue")
    app.setEntryBg("hiddenPassword", "lightblue")
    app.setEntryBg("visiblePassword", "lightblue")
    app.setFocus("Username :")
    app.setBg("white")
    app.startLabelFrame("", 0, 2)
    app.addImage("tlc", "tlc.png", 0,2)#Adds the company logo
    app.setImageSize("tlc", 200,200)
    app.setGuiPadding(10,10)
    app.stopLabelFrame()
    app.setFont(18)            
    app.addButton("Login",press, 3, 0)
    app.addButton("Forgot Login",press, 3, 2)
    app.setButtonBg("Login", "lightblue")
    app.setButtonBg("Forgot Login", "lightblue")
    app.showSubWindow("Login")
    app.stopSubWindow()
    
################################################################Main Menu################################################################
    app.startSubWindow("MainMenu")
    app.setSize("fullscreen")
    app.addLabel("title2","DSW Transfer Audit",0,0,2,2)
    app.getLabelWidget("title2").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title", "white")
    app.setLabelBg("title2", "white")
    app.setLabelFg("title2", "blue")
    app.setBg("white")
    app.addImage("tlc2", "tlc.png", 0,2)#Adds the company logo
    app.addNamedButton("Patient Data","ButtonPD",press, 3, 1)
    app.addNamedButton("Audit Graphs","ButtonAG",press,3, 0)
    app.setButtonBg("ButtonPD", "lightblue")
    app.setButtonBg("ButtonAG", "lightblue")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addButtons(["Log Out"],logout)
    app.setButtonBg("Log Out", "lightblue")
 


    app.stopSubWindow()



################################################################Year Display AG################################################################
    app.startSubWindow("YearDisplayAG")
    app.setSize("fullscreen")
    app.addLabel("title3","Year")
    app.getLabelWidget("title3").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title3", "white")
    app.setLabelFg("title3", "blue")
    app.addImage("tlc3", "tlc.png", 0,2)#Adds the company logo
    app.setFont(18) 
    app.setBg("white")
    app.setStretch("columns")
    app.addNamedButton("2023","AG_2023",press,1,0)#Adds named buttons for the years
    app.addNamedButton("2024","AG_2024",press,2,0)
    app.addNamedButton("2025","AG_2025",press,3,0)
    app.addNamedButton("2026","AG_2026",press,4,0)
    app.setButtonBg("AG_2023", "lightblue")
    app.setButtonBg("AG_2024", "lightblue")
    app.setButtonBg("AG_2025", "lightblue")
    app.setButtonBg("AG_2026", "lightblue")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addNamedButton("Back","backYAG",press)
    app.setButtonBg("backYAG", "lightblue")
    

    
    app.stopSubWindow()




################################################################Year Display PD################################################################
    app.startSubWindow("YearDisplayPD")
    app.setSize("fullscreen")
    app.addLabel("title5","Year")
    app.getLabelWidget("title5").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title5", "white")
    app.setLabelFg("title5", "blue")
    app.addImage("tlc5", "tlc.png", 0,2)#Adds the company logo
    app.setFont(18)
    app.setBg("white")
    app.setStretch("columns")
    app.addNamedButton("2023","PD_2023",press,1,0)#Adds named buttons for the years
    app.addNamedButton("2024","PD_2024",press,2,0)
    app.addNamedButton("2025","PD_2025",press,3,0)
    app.addNamedButton("2026","PD_2026",press,4,0)
    app.setButtonBg("PD_2023", "lightblue")
    app.setButtonBg("PD_2024", "lightblue")
    app.setButtonBg("PD_2025", "lightblue")
    app.setButtonBg("PD_2026", "lightblue")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addNamedButton("Back","backYPD",press)
    app.setButtonBg("backYPD", "lightblue")

    app.stopSubWindow()




################################################################Month Display AG################################################################
    app.startSubWindow("MonthDisplayAG")
    app.setSize("fullscreen")
    app.addLabel("title4","Months")
    app.getLabelWidget("title4").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title4", "white")
    app.setLabelFg("title4", "blue")
    app.addImage("tlc8", "tlc.png", 0,2)#Adds the company logo
    app.addNamedButton("January","AG_January",monthGraph,1,0)
    app.addNamedButton("February","AG_February",monthGraph,2,0)
    app.addNamedButton("March","AG_March",monthGraph,3,0)
    app.addNamedButton("April","AG_April",monthGraph,4,0)
    app.addNamedButton("May","AG_May",monthGraph,5,0)
    app.addNamedButton("June","AG_June",monthGraph,6,0)
    app.addNamedButton("July","AG_July",monthGraph,7,0)
    app.addNamedButton("August","AG_August",monthGraph,8,0)
    app.addNamedButton("September","AG_September",monthGraph,9,0)
    app.addNamedButton("October","AG_October",monthGraph,10,0)
    app.addNamedButton("November","AG_November",monthGraph,11,0)
    app.addNamedButton("December","AG_December",monthGraph,12,0)
    app.setButtonBg("AG_January", "lightblue")#Adds lightblue colour 
    app.setButtonBg("AG_February", "lightblue")
    app.setButtonBg("AG_March", "lightblue")
    app.setButtonBg("AG_April", "lightblue")
    app.setButtonBg("AG_May", "lightblue")
    app.setButtonBg("AG_June", "lightblue")
    app.setButtonBg("AG_July", "lightblue")
    app.setButtonBg("AG_August", "lightblue")
    app.setButtonBg("AG_September", "lightblue")
    app.setButtonBg("AG_October", "lightblue")
    app.setButtonBg("AG_November", "lightblue")
    app.setButtonBg("AG_December", "lightblue")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addNamedButton("Back","backMAG",press)
    app.setButtonBg("backMAG", "lightblue")
    
 
    
    
    app.stopSubWindow()
    
    
    
################################################################Month Display PD################################################################
    app.startSubWindow("MonthDisplayPD")
    app.setSize("fullscreen")
    app.addLabel("title6","Months")
    app.getLabelWidget("title6").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title6", "white")
    app.setLabelFg("title6", "blue")
    app.addImage("tlc6", "tlc.png", 0,2)#Adds the company logo
    app.setFont(18) 
    app.setBg("white")
    app.addNamedButton("January","PD_January",press,1,0)#Adds named button to the buttons
    app.addNamedButton("February","PD_February",press,2,0)
    app.addNamedButton("March","PD_March",press,3,0)
    app.addNamedButton("April","PD_April",press,4,0)
    app.addNamedButton("May","PD_May",press,5,0)
    app.addNamedButton("June","PD_June",press,6,0)
    app.addNamedButton("July","PD_July",press,7,0)
    app.addNamedButton("August","PD_August",press,8,0)
    app.addNamedButton("September","PD_September",press,9,0)
    app.addNamedButton("October","PD_October",press,10,0)
    app.addNamedButton("November","PD_November",press,11,0)
    app.addNamedButton("December","PD_December",press,12,0)
    app.setButtonBg("PD_January", "lightblue")
    app.setButtonBg("PD_February", "lightblue")
    app.setButtonBg("PD_March", "lightblue")
    app.setButtonBg("PD_April", "lightblue")
    app.setButtonBg("PD_May", "lightblue")
    app.setButtonBg("PD_June", "lightblue")
    app.setButtonBg("PD_July", "lightblue")
    app.setButtonBg("PD_August", "lightblue")
    app.setButtonBg("PD_September", "lightblue")
    app.setButtonBg("PD_October", "lightblue")
    app.setButtonBg("PD_November", "lightblue")
    app.setButtonBg("PD_December", "lightblue")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addNamedButton("Back","backMPD",press)
    app.setButtonBg("backMPD", "lightblue")
 
    app.stopSubWindow()



################################################################Patient Transfer Databases################################################################
    app.startSubWindow("PatientTransferDatabases")
    app.setSize("fullscreen")
    app.addImage("tlc7", "tlc.png", 0,2)#Adds the company logo
    app.addLabel("title7","Patient Transfer Databases",0,0,2,2)
    app.getLabelWidget("title7").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title7", "white")
    app.setLabelFg("title7", "blue")
    app.setFont(18) 
    app.setBg("white")
    app.addButton("Daily",press,1,0)
    app.addButton("Current Month Database",press,1,1)
    app.setButtonBg("Daily","lightblue")
    app.setButtonBg("Current Month Database","lightblue")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addNamedButton("Back","BackPTD",press)
    app.setButtonBg("BackPTD","lightblue")
    app.stopSubWindow()



################################################################Daily Database################################################################
    app.startSubWindow("DailyDatabase")
    app.setSize("fullscreen")
    app.addLabel("title8","Daily",0,1)#Title of the table
    app.getLabelWidget("title8").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title8", "white")
    app.setLabelFg("title8", "blue")
    app.setFont(18) 
    app.setBg("white")
    app.addLabel("title9","Consultants Key",0,10,8).config(font=("","20", "bold","underline"))
    app.setSticky("e")
    app.setFont(10)
    #Adds all the consultants under the consultants key
    app.addListBox("ConsultantsDaily", ["Mr Bhogal - MB",
                                   "Mr Westscott - MW",
                                   "Mr Mohammed - M",
                                   "Mr Pringle - P",
                                   "Mr Hamilton - RH",
                                   "Mr Lee - RL",
                                   "Mr Wong - RSW",
                                   "Mr Jain - J",
                                   "Mr Shah - SS",
                                   "Mr Trikha - ST",
                                   "Mr Saurabh Jain - SJ",
                                   "Mr Williamson - W",
                                   "Mr Kulkarni - AK",
                                   "Mr Mearza - AM",
                                   "Mr Mitry - DM",
                                   "Mr Elgohary - E",
                                   "Mr Ahmed - FA",
                                   "Mr Ratnarajan - GR",
                                   "Mr Henderson - HH",
                                   "Mr Duguid - IGD",
                                   "Mr Dowler - JD",
                                   "Prof Lim - Lim",
                                   "Prof Jackson",
                                   "Mr Khan - JK",
                                   "Mr LaidLaw - L",
                                   "Miss Goawalla - G",
                                   "Miss Jain - J",
                                   "Miss Mensah - MM",
                                   "Miss Zakir - RZ",
                                   "Miss Saw - S",
                                   "Mr El-Amir - AEA",
                                   "Mr Mearza - AM",
                                   "Mr Mitry - DM",
                                   "Mr Elgohary - E",
                                   "Mr F Ahmed - FA"],1,10,10,8)
    app.setLabelBg("title9", "white")
    app.setLabelFg("title9", "blue")
    app.setSticky("nw")
    app.addLabel("title10","Transfer reasons key",0,0).config(font=("","20", "bold","underline"))
    app.setLabelBg("title10", "white")
    app.setLabelFg("title10", "blue")
    app.addLabel("medical reason","1 - Medical Reason",1,0)#Adds the different reasons for patient transfers to the user interface
    app.addLabel("patient request","2 - Patient Request",2,0)
    app.addLabel("late discharge","3 - Late discharge",3,0)
    app.addLabel("consultant request","4 - Consultant Request",4,0)
    app.addLabel("social reason","5 - Social Reason",5,0)
    app.addLabel("other","6 - Other",6,0)
    app.setFont(20)
    #creates a grid where data can be inputted  
    app.setSticky("ew")
    app.addGrid("g1",

    [["ConsultantID", "WardID","RoomNo", "TimeOfAdmission","TransferDate","TransferTime","ReasonForTransfer","Comments","Month"],

    ["","","","","","","","",""],

    ["","","","","","","","",""],

    ["","","","","","","","",""],

    ["","","","","","","","",""]],
#Allows for the features of the grid to exist and when user right-clicks on an entry box a sub-menu pops up which allows for changes to the grid 
    action=SaveTableg1,showMenu=True,actionButton ="save",addRow=addGridRowg1,row=1,column=1, rowspan=9, colspan=9)
    app.setSticky("sw")
    app.addNamedButton("Back","BackDD",press,10,0)
    app.setButtonBg("BackDD","lightblue")
   
    
    
    app.stopSubWindow()
    
    

################################################################Current Month Database################################################################
    app.startSubWindow("CurrentMonthDatabase")
    app.setSize("fullscreen")
    app.addLabel("title11","Current Month",0,1)#Title of the table
    app.getLabelWidget("title11").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title11", "white")
    app.setLabelFg("title11", "blue")
    app.setFont(18) 
    app.setBg("white")
    app.addLabel("title12","Consultants Key",0,10,8).config(font=("","20", "bold","underline"))
    app.setLabelBg("title12", "white")
    app.setLabelFg("title12", "blue")
    app.setSticky("e")
    app.setFont(10)
    #Adds all the consultants under the consultants key
    app.addListBox("ConsultantsMonth", ["Mr Bhogal - MB",
                                   "Mr Westscott - MW",
                                   "Mr Mohammed - M",
                                   "Mr Pringle - P",
                                   "Mr Hamilton - RH",
                                   "Mr Lee - RL",
                                   "Mr Wong - RSW",
                                   "Mr Jain - J",
                                   "Mr Shah - SS",
                                   "Mr Trikha - ST",
                                   "Mr Saurabh Jain - SJ",
                                   "Mr Williamson - W",
                                   "Mr Kulkarni - AK",
                                   "Mr Mearza - AM",
                                   "Mr Mitry - DM",
                                   "Mr Elgohary - E",
                                   "Mr Ahmed - FA",
                                   "Mr Ratnarajan - GR",
                                   "Mr Henderson - HH",
                                   "Mr Duguid - IGD",
                                   "Mr Dowler - JD",
                                   "Prof Lim - Lim",
                                   "Prof Jackson",
                                   "Mr Khan - JK",
                                   "Mr LaidLaw - L",
                                   "Miss Goawalla - G",
                                   "Miss Jain - J",
                                   "Miss Mensah - MM",
                                   "Miss Zakir - RZ",
                                   "Miss Saw - S",
                                   "Mr El-Amir - AEA",
                                   "Mr Mearza - AM",
                                   "Mr Mitry - DM",
                                   "Mr Elgohary - E",
                                   "Mr F Ahmed - FA"],1,10,10,8)
 
    app.setSticky("nw")
    app.addLabel("title13","Transfer reasons key",0,0).config(font=("","20", "bold","underline"))
    app.setLabelBg("title13", "white")
    app.setLabelFg("title13", "blue")
    app.addLabel("medical reason (month)","1 - Medical Reason",1,0)
    app.addLabel("patient request (month)","2 - Patient Request",2,0)
    app.addLabel("late discharge (month)","3 - Late discharge",3,0)
    app.addLabel("consultant request (month)","4 - Consultant Request",4,0)
    app.addLabel("social reason (month)","5 - Social Reason",5,0)
    app.addLabel("other (month)","6 - Other",6,0)
    app.setFont(20)
    app.setSticky("ew")
    app.addGrid("g2",

    [["ConsultantID", "WardID","RoomNo", "TimeOfAdmission","TransferDate","TransferTime","ReasonForTransfer","Comments","Month"],

    ["","","","","","","","",""],

    ["","","","","","","","",""],

    ["","","","","","","","",""],

    ["","","","","","","","",""]],
#Allows for the features of the grid to exist and when user right-clicks on an entry box a sub-menu pops up which allows for changes to the grid 
    action=SaveTableg2,showMenu=True,actionButton="save",addRow=addGridRowg2,row=1,column=1, rowspan=9, colspan=9)
    app.setSticky("sw")
    app.addNamedButton("Back","BackCD",press,10,0)
    app.setButtonBg("BackCD","lightblue")
   
    
    app.stopSubWindow()


################################################################Audit Graphs################################################################
    app.startSubWindow("AuditGraphs")
    app.setSticky("n")
    app.setPadding([40,40])
    app.addLabel("title14","Audit Graphs",0,1)
    app.getLabelWidget("title14").config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title14", "white")
    app.setLabelFg("title14", "blue")
    app.setSize("fullscreen")
    app.addImage("tlc9", "tlc.png", 0,2)#Adds the company logo
    app.setFont(18)
    app.setPadding([40,40])
    app.addNamedButton("View Graph Summary","VGS",press,1,1)#adds the View Graph Summary button for any month
    app.setSticky("e")
    app.addNamedButton("Consultant Graph","CG",press,1,2)#adds the consultant graph button for any month
    app.setButtonBg("CG","lightblue")
    app.setButtonBg("VGS","lightblue")
    app.setBg("white")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addNamedButton("Back","BackAGP",press)
    app.setButtonBg("BackAGP","lightblue")

################################################################Graph Summary################################################################
    app.startSubWindow("GraphSummary")
    app.addLabel("title15","Graph Summary",0,0).config(font=("","20", "bold","underline"))#sets font size and makes title bold and underlined
    app.setLabelBg("title15", "white")
    app.setLabelFg("title15", "blue")
    app.setSize("fullscreen")
    app.addImage("tlc10", "tlc.png", 0,2)#Adds the company logo
    app.addLabel("transfers","highest number of transfers = ",1,0)
    app.addLabel("maxVal",max_value,1,1)#adds maximum value of the reasons for transfers to the gui
    app.setLabelBg("transfers", "white")
    app.setLabelFg("transfers", "blue")
    app.addLabel("category","highest catgory of transfers = ",2,0)
    app.addLabel("highest_category",highest_category,2,1)#adds the highest category of the reasons for transfers to the gui
    app.setLabelBg("category", "white")
    app.setLabelFg("category", "blue")
    app.addLabel("common consultant","highest number of transfers for one consultant = ",3,0)
    app.setLabelBg("common consultant", "white")
    app.setLabelFg("common consultant", "blue")
    app.addLabel("Most Common Consultant", common_consultant,3,1)#shows the number of patient transfers for the most common consultant 
    app.addLabel("Consultant name","Please see the Consultant Graph for more information on the most common consultant")
    app.setLabelBg("Consultant name", "white")
    app.setLabelFg("Consultant name" , "blue")
    app.setFont(18) 
    app.setBg("white")
    app.setSticky("sw")
    app.setPadding([40,40])
    app.addNamedButton("Back","BackGS",press)
    app.setButtonBg("BackGS","lightblue")
    
    app.stopSubWindow() 

createInterface()

          








