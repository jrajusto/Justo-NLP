from ast import Lambda
from tkinter import *
import tkinter
from turtle import heading
import speechRecog as s
import threading
import mysql.connector
from tkinter import ttk
import translate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

class Plant:
    def __init__(self,name,hum,temp,soil,air,lux):
        self.name = name
        self.humidity = hum
        self.temperature = temp
        self.soilMoisture = soil
        self.airQuality = air
        self.lightIntensity = lux

    def setOptimal(self,name,hum,temp,soil,air,lux):
        self.name = name
        self.humidity = hum
        self.temperature = temp
        self.soilMoisture = soil
        self.airQuality = air
        self.lightIntensity = lux


#optimal conditions for the plants
optimalPlant1 = Plant('tomato',75,30,60,80,200)
optimalPlant2 = Plant('grape',75,30,60,80,200)
optimalPlant3 = Plant('wheat',75,30,60,80,200)
optimalPlant4 = Plant('corn',75,30,60,80,200)

#get query from textbox
def getInputQuery():
    global query
    global queryView
    global outputQuerytext

    query = inputQuery.get()

    try:
        outputQuerytext
    except:
        print('DNE')
    else:
        outputQuerytext.pack_forget()

    
    printQuery()
        
#shows the input query to be translated on screen
def printQuery():
    global query
    global outputQuerytext

    outputQuerytext = Label(outputQueryFrame,padx=5,pady=5,text=query)
    outputQuerytext.grid(row=0,column=0)
    continueButton = Button(outputQueryFrame,text="Continue",command=translateQuery,padx=10)
    continueButton.grid(row=0,column=1)

def printAnswer(answer):
    outputAnswer = Label(outputAnswerFrame,text=answer)
    outputAnswer.pack()

    

#gets voice input from user
def speak():
    global speakFrame
    speakFrame = LabelFrame(mainWindow,padx=5,pady=5)
    speakFrame.pack(padx=10,pady=10)
    speakingLabel = Label(speakFrame,text="Start speaking now...")
    speakingLabel.pack()

    threading.Thread(target=readmic).start()

   
#get voice input from mic
def readmic():

    global query
    global speakingBox
    query = s.readMicrophone()
    printQuery()
    speakFrame.destroy()

#create table from sql output
def createTable(output):

    tableFrame = Frame(outputDataFrame)
    tableFrame.pack(side=tkinter.LEFT,padx=1)

    headings = ttk.Treeview(tableFrame,columns=tuple(headingList),show="headings")
    headings.grid(row=0, column=0)
    for i in headingList:
        headings.heading(i, text = i)

    for i in output:
        headings.insert('','end',values=i)

    for i in headingList:
        headings.column(i, width=120, anchor=CENTER)



    scrollbar = ttk.Scrollbar(tableFrame, orient=tkinter.VERTICAL, command=headings.yview)
    headings.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

#translate the query to sql query and execupte
def translateQuery():
    global sqlQuery
    global headingList
    global graphBool
    sqlQuery,headingList,graphBool,optimalBool = translate.convertToSql(query)
    myCursor.execute(sqlQuery)
    output = myCursor.fetchall()
    createTable(output)
    if graphBool:
        df = pd.DataFrame (output, columns = headingList)
        headingList.remove('ID')
        headingList.remove('Date_n_Time')
        figure, axis = plt.subplots(len(headingList))

        headingNo = 0
        for heading in headingList:
            axis[headingNo].plot(df['Date_n_Time'],df[heading])
            axis[headingNo].set_title(heading)
            headingNo = headingNo + 1
    if optimalBool:
        print('optimal')

        #axis[headingNo].set_title("Combined graph")
        #for heading in headingList:
        #    axis[headingNo].plot(df['Date_n_Time'],df[heading])
            
        plt.tight_layout(h_pad=0.55)
        plt.show()


#gui initialization
root = Tk()
root.title("Prototype")


#database initialization
db = mysql.connector.connect(host="localhost",user="root",password="",database="sensornetwork")
myCursor = db.cursor()

#global variables
queryView = False

#main window
mainWindow = LabelFrame(root)
mainWindow.pack(padx=10,pady=10)

#input query frame
inputQueryFrame = LabelFrame(mainWindow,text="Input Query",padx=5,pady=5)
inputQueryFrame.pack(anchor=W)

#input query text box
inputQuery = Entry(inputQueryFrame,width=50)
inputQuery.grid(row=0,column=0)

    #query = "Show the core temperature from the grapes plants where humidity is greater than 20 and temperature is less than 30 in december 2 to december 7 2021"
    #query = "Show the core temperature from the grapes plants where humidity is greater than 20 in december 2 to december 7 2021"
    #query = "Show the core temperature from the grapes plants where humidity is greater than 20 in december 2 2021 to december 7 2021
    #query = "Show all from the grapes plants" 
    #query = "Has the tomato plants maintain optimal codition last month"
    #query = "Show the core temperature from the corn plants"
    #query = "Show the core temperature from the corn plants this month"
    #query = "Graph the core temperature and humidity from the corn plants"

inputQuery.insert(0,"Show the core temperature from the corn plants this month")

#enter button
enterButton = Button(inputQueryFrame,text="Enter",command=getInputQuery,padx=10)
enterButton.grid(row=0,column=1)


#speak query frame
speakQueryFrame = LabelFrame(mainWindow,padx=5,pady=5,text='Speak Query')
speakQueryFrame.pack(anchor=W)


speakLabel = Label(speakQueryFrame,text = "Press the button and state your query")
speakLabel.grid(row=1,column=0)

#speak button
speakButton = Button(speakQueryFrame, text = "Speak",command=speak, padx=10)
speakButton.grid(row=1,column=1)

#Output query frame
outputQueryFrame = LabelFrame(mainWindow,padx=5,pady=5,text='You entered the query')
outputQueryFrame.pack(anchor=W)

#Output answer frame
outputAnswerFrame = LabelFrame(mainWindow,padx=5,pady=5,text='Answer')
outputAnswerFrame.pack(anchor=W)

#Output data frame
outputDataFrame = LabelFrame(mainWindow,text = 'Output Data')
outputDataFrame.size()
outputDataFrame.pack()


#Output data graph
outputDataGraph = LabelFrame(mainWindow,text = 'Output Data Graph')
outputDataGraph.pack()




root.mainloop()