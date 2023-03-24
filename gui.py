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

#list of plants available
plantList = ['tomato','grape','wheat','corn']
averageList = []

SQLtoParameter = {'Temperature':'temperature','Humidity':'humidity','Air_Quality':'air quality','Soil_Moisture':'soil moisture','Light_Intensity':'light'}

def editOptimal(name,hum,temp,soil,air,lux,node):
    if node == 1:
        optimalPlant1.setOptimal(name,hum,temp,soil,air,lux)
        plantList[0] = name
    elif node == 2:
        optimalPlant2.setOptimal(name,hum,temp,soil,air,lux)
        plantList[1] = name
    elif node == 3:
        optimalPlant3.setOptimal(name,hum,temp,soil,air,lux)
        plantList[2] = name
    elif node == 4:
        optimalPlant4.setOptimal(name,hum,temp,soil,air,lux)
        plantList[3] = name

def openOptimalWindow():
    optimalWindow = Toplevel(root)

    optimalWindow.title('Optimal conditions')
    optimalWindowFrame = LabelFrame(optimalWindow,text="Optimal Conditions")
    optimalWindowFrame.pack()

    #for sensor node 1
    sensornode1Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 1")
    sensornode1Frame.grid(column=0,row=0,ipadx=5)

    sensornode1Name = Label(sensornode1Frame,text="Name")
    sensornode1Name.grid(row=0,column=0)
    sensornode1NameInput = Entry(sensornode1Frame,width=10)
    sensornode1NameInput.grid(row=0,column=1)
    sensornode1NameInput.insert(0,optimalPlant1.name)

    sensornode1TemperatureText = Label(sensornode1Frame,text="Temperature (C)")
    sensornode1TemperatureText.grid(row=1,column=0)
    sensornode1TemperatureInput = Entry(sensornode1Frame,width=10)
    sensornode1TemperatureInput.grid(row=1,column=1)
    sensornode1TemperatureInput.insert(0,optimalPlant1.temperature)

    sensornode1HumidityText = Label(sensornode1Frame,text="Humidity")
    sensornode1HumidityText.grid(row=2,column=0)
    sensornode1HumidityInput = Entry(sensornode1Frame,width=10)
    sensornode1HumidityInput.grid(row=2,column=1)
    sensornode1HumidityInput.insert(0,optimalPlant1.humidity)

    sensornode1AirText = Label(sensornode1Frame,text="Air Quality (ppm)")
    sensornode1AirText.grid(row=3,column=0)
    sensornode1AirInput = Entry(sensornode1Frame,width=10)
    sensornode1AirInput.grid(row=3,column=1)
    sensornode1AirInput.insert(0,optimalPlant1.airQuality)

    sensornode1SoilText = Label(sensornode1Frame,text="Soil Moisture")
    sensornode1SoilText.grid(row=4,column=0)
    sensornode1SoilInput = Entry(sensornode1Frame,width=10)
    sensornode1SoilInput.grid(row=4,column=1)
    sensornode1SoilInput.insert(0,optimalPlant1.soilMoisture)

    sensornode1LightText = Label(sensornode1Frame,text="Light Intensity")
    sensornode1LightText.grid(row=5,column=0)
    sensornode1LightInput = Entry(sensornode1Frame,width=10)
    sensornode1LightInput.grid(row=5,column=1)
    sensornode1LightInput.insert(0,optimalPlant1.lightIntensity)


    sensornode1button = Button(sensornode1Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode1NameInput.get(),sensornode1HumidityInput.get(),sensornode1TemperatureInput.get(),sensornode1SoilInput.get(),sensornode1AirInput.get(),sensornode1LightInput.get(),1))
    sensornode1button.grid(row=6,column=0)

    #for sensor node 2
    sensornode2Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 2")
    sensornode2Frame.grid(column=1,row=0,ipadx=5)
    
    sensornode2Name = Label(sensornode2Frame,text="Name")
    sensornode2Name.grid(row=0,column=0)
    sensornode2NameInput = Entry(sensornode2Frame,width=10)
    sensornode2NameInput.grid(row=0,column=1)
    sensornode2NameInput.insert(0,optimalPlant2.name)

    sensornode2TemperatureText = Label(sensornode2Frame,text="Temperature (C)")
    sensornode2TemperatureText.grid(row=1,column=0)
    sensornode2TemperatureInput = Entry(sensornode2Frame,width=10)
    sensornode2TemperatureInput.grid(row=1,column=1)
    sensornode2TemperatureInput.insert(0,optimalPlant2.temperature)

    sensornode2HumidityText = Label(sensornode2Frame,text="Humidity")
    sensornode2HumidityText.grid(row=2,column=0)
    sensornode2HumidityInput = Entry(sensornode2Frame,width=10)
    sensornode2HumidityInput.grid(row=2,column=1)
    sensornode2HumidityInput.insert(0,optimalPlant2.humidity)

    sensornode2AirText = Label(sensornode2Frame,text="Air Quality (ppm)")
    sensornode2AirText.grid(row=3,column=0)
    sensornode2AirInput = Entry(sensornode2Frame,width=10)
    sensornode2AirInput.grid(row=3,column=1)
    sensornode2AirInput.insert(0,optimalPlant2.airQuality)

    sensornode2SoilText = Label(sensornode2Frame,text="Soil Moisture")
    sensornode2SoilText.grid(row=4,column=0)
    sensornode2SoilInput = Entry(sensornode2Frame,width=10)
    sensornode2SoilInput.grid(row=4,column=1)
    sensornode2SoilInput.insert(0,optimalPlant2.soilMoisture)

    sensornode2LightText = Label(sensornode2Frame,text="Light Intensity")
    sensornode2LightText.grid(row=5,column=0)
    sensornode2LightInput = Entry(sensornode2Frame,width=10)
    sensornode2LightInput.grid(row=5,column=1)
    sensornode2LightInput.insert(0,optimalPlant2.lightIntensity)


    sensornode2button = Button(sensornode2Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode2NameInput.get(),sensornode2HumidityInput.get(),sensornode2TemperatureInput.get(),sensornode2SoilInput.get(),sensornode2AirInput.get(),sensornode2LightInput.get(),2))
    sensornode2button.grid(row=6,column=0)

    #for sensor node 3
    sensornode3Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 3")
    sensornode3Frame.grid(column=2,row=0,ipadx=5)
    
    sensornode3Name = Label(sensornode3Frame,text="Name")
    sensornode3Name.grid(row=0,column=0)
    sensornode3NameInput = Entry(sensornode3Frame,width=10)
    sensornode3NameInput.grid(row=0,column=1)
    sensornode3NameInput.insert(0,optimalPlant3.name)

    sensornode3TemperatureText = Label(sensornode3Frame,text="Temperature (C)")
    sensornode3TemperatureText.grid(row=1,column=0)
    sensornode3TemperatureInput = Entry(sensornode3Frame,width=10)
    sensornode3TemperatureInput.grid(row=1,column=1)
    sensornode3TemperatureInput.insert(0,optimalPlant3.temperature)

    sensornode3HumidityText = Label(sensornode3Frame,text="Humidity")
    sensornode3HumidityText.grid(row=2,column=0)
    sensornode3HumidityInput = Entry(sensornode3Frame,width=10)
    sensornode3HumidityInput.grid(row=2,column=1)
    sensornode3HumidityInput.insert(0,optimalPlant3.humidity)

    sensornode3AirText = Label(sensornode3Frame,text="Air Quality (ppm)")
    sensornode3AirText.grid(row=3,column=0)
    sensornode3AirInput = Entry(sensornode3Frame,width=10)
    sensornode3AirInput.grid(row=3,column=1)
    sensornode3AirInput.insert(0,optimalPlant3.airQuality)

    sensornode3SoilText = Label(sensornode3Frame,text="Soil Moisture")
    sensornode3SoilText.grid(row=4,column=0)
    sensornode3SoilInput = Entry(sensornode3Frame,width=10)
    sensornode3SoilInput.grid(row=4,column=1)
    sensornode3SoilInput.insert(0,optimalPlant3.soilMoisture)

    sensornode3LightText = Label(sensornode3Frame,text="Light Intensity")
    sensornode3LightText.grid(row=5,column=0)
    sensornode3LightInput = Entry(sensornode3Frame,width=10)
    sensornode3LightInput.grid(row=5,column=1)
    sensornode3LightInput.insert(0,optimalPlant3.lightIntensity)


    sensornode3button = Button(sensornode3Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode3NameInput.get(),sensornode3HumidityInput.get(),sensornode3TemperatureInput.get(),sensornode3SoilInput.get(),sensornode3AirInput.get(),sensornode3LightInput.get(),3))
    sensornode3button.grid(row=6,column=0)

    #for sensor node 4
    sensornode4Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 4")
    sensornode4Frame.grid(column=3,row=0,ipadx=5)
    
    sensornode4Name = Label(sensornode4Frame,text="Name")
    sensornode4Name.grid(row=0,column=0)
    sensornode4NameInput = Entry(sensornode4Frame,width=10)
    sensornode4NameInput.grid(row=0,column=1)
    sensornode4NameInput.insert(0,optimalPlant4.name)

    sensornode4TemperatureText = Label(sensornode4Frame,text="Temperature (C)")
    sensornode4TemperatureText.grid(row=1,column=0)
    sensornode4TemperatureInput = Entry(sensornode4Frame,width=10)
    sensornode4TemperatureInput.grid(row=1,column=1)
    sensornode4TemperatureInput.insert(0,optimalPlant4.temperature)

    sensornode4HumidityText = Label(sensornode4Frame,text="Humidity")
    sensornode4HumidityText.grid(row=2,column=0)
    sensornode4HumidityInput = Entry(sensornode4Frame,width=10)
    sensornode4HumidityInput.grid(row=2,column=1)
    sensornode4HumidityInput.insert(0,optimalPlant4.humidity)

    sensornode4AirText = Label(sensornode4Frame,text="Air Quality (ppm)")
    sensornode4AirText.grid(row=3,column=0)
    sensornode4AirInput = Entry(sensornode4Frame,width=10)
    sensornode4AirInput.grid(row=3,column=1)
    sensornode4AirInput.insert(0,optimalPlant4.airQuality)

    sensornode4SoilText = Label(sensornode4Frame,text="Soil Moisture")
    sensornode4SoilText.grid(row=4,column=0)
    sensornode4SoilInput = Entry(sensornode4Frame,width=10)
    sensornode4SoilInput.grid(row=4,column=1)
    sensornode4SoilInput.insert(0,optimalPlant4.soilMoisture)

    sensornode4LightText = Label(sensornode4Frame,text="Light Intensity")
    sensornode4LightText.grid(row=5,column=0)
    sensornode4LightInput = Entry(sensornode4Frame,width=10)
    sensornode4LightInput.grid(row=5,column=1)
    sensornode4LightInput.insert(0,optimalPlant4.lightIntensity)


    sensornode4button = Button(sensornode4Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode4NameInput.get(),sensornode4HumidityInput.get(),sensornode4TemperatureInput.get(),sensornode4SoilInput.get(),sensornode4AirInput.get(),sensornode4LightInput.get(),4))
    sensornode4button.grid(row=6,column=0)



#get query from textbox
def getInputQuery():
    global query
    global queryView
    global outputQuerytext
    global outputAnswer
    global tableFrame

    query = inputQuery.get()

    try:
        outputQuerytext
    except:
        print('DNE')
    else:
        outputQuerytext.grid_forget()

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
    global outputAnswer
    global outputAnswerFrame
    

    outputAnswer = Label(outputAnswerFrame,text=answer)
    outputAnswer.pack()

    

#gets voice input from user
def speak():
    global speakFrame
    speakFrame = LabelFrame(firstWindow,padx=5,pady=5)
    speakFrame.pack(padx=10,pady=10)
    speakingLabel = Label(speakFrame,text="Start speaking now...")
    speakingLabel.pack()

    threading.Thread(target=readmic).start()

   
#get voice input from mic
def readmic():

    global query
    global speakingBox
    query = s.readMicrophone()
    
    try:
        outputQuerytext
    except:
        print('DNE')
    else:
        outputQuerytext.grid_forget()

    printQuery()
    speakFrame.destroy()

#create table from sql output
def createTable(output,plantName):

    global outputPlantDataFrame
    outputPlantDataFrame = LabelFrame(outputDataFrame,text = plantName)
    outputPlantDataFrame.size()
    outputPlantDataFrame.pack()

    
    global tableFrame

    tableFrame = Frame(outputPlantDataFrame)
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
    global optimalBool
    global compareBool
    global plantNames
    global outputAnswer
    global tableFrame
    global plantNo
    global outputDataFrame
    global outputAnswerFrame
    
    
    try:
        outputAnswerFrame
    except:
        print('DNE')
        outputAnswerFrame = LabelFrame(firstWindow,padx=5,pady=5,text='Answer')
        outputAnswerFrame.pack(anchor=W)
        
    else:
        outputAnswerFrame.pack_forget()
        outputAnswerFrame = LabelFrame(firstWindow,padx=5,pady=5,text='Answer')
        outputAnswerFrame.pack(anchor=W)
    
   
    try:
        outputDataFrame
    except:
        #Output data frame
        outputDataFrame = Frame(firstWindow)
        outputDataFrame.pack()
    else:
        outputDataFrame.pack_forget()
        outputDataFrame = Frame(firstWindow)
        outputDataFrame.pack()

    

    sqlQueries,headingList,graphBool,compareBool,optimalBool,averageBool,plantNames = translate.convertToSql(query,optimalPlant1,optimalPlant2,optimalPlant3,optimalPlant4,plantList)
    
    plantNo = 0
    for sqlQuery in sqlQueries:
        
        myCursor.execute(sqlQuery)
        output = myCursor.fetchall()
        #if output exist, create the table
        if output:
            createTable(output,plantNames[plantNo])
            
        print(headingList)
        print('Graph state')
        print(graphBool)

        if graphBool:

            if output:
                df = pd.DataFrame (output, columns = headingList)
                headingList.remove('ID')
                headingList.remove('Date_n_Time')

                if len(headingList) > 1:
                    figure, axis = plt.subplots(len(headingList))

                    headingNo = 0
                    for heading in headingList:
                        axis[headingNo].plot(df['Date_n_Time'],df[heading])
                        axis[headingNo].set_title(heading + " of " + plantNames[plantNo])
                        headingNo = headingNo + 1
                else:
                    plt.plot(df['Date_n_Time'],df[headingList[0]])
                    plt.title(headingList[0] + " of " + plantNames[plantNo])

                plt.tight_layout(h_pad=0.55)
                plt.show()

                headingList.insert(0,'ID')
                headingList.insert(1,'Date_n_Time')
            else:
                printAnswer("There is no data to show.")
        if compareBool:
            
            df = pd.DataFrame (output, columns = headingList)
            print(headingList)
            headingList.remove('ID')
            headingList.remove('Date_n_Time')

            headingNo = 0
            for heading in headingList:
                plt.plot(df['Date_n_Time'],df[heading])
                #axis[headingNo].set_title(heading)
                headingNo = headingNo + 1

            plt.tight_layout(h_pad=0.55)
            plt.legend(headingList)
            plt.show()

            headingList.insert(0,'ID')
            headingList.insert(1,'Date_n_Time')

        if optimalBool:
            #if output is empty
            if not output:
                printAnswer("The plants has reached optimal condition.")
            else:
                printAnswer("The plants has not reached optimal condition in these occasions.")

            print(output)

        
        if averageBool:
            df = pd.DataFrame (output, columns = headingList)
            print(headingList)
            headingList.remove('ID')
            headingList.remove('Date_n_Time')

            headingNo = 0
            outputSentence = ""
            for heading in headingList:
                outputSentence = outputSentence + "The average " + SQLtoParameter[heading] + " is " + str(round(df[heading].mean(),2)) + ". "

            printAnswer(outputSentence)

            headingList.insert(0,'ID')
            headingList.insert(1,'Date_n_Time')

        plantNo = plantNo + 1

    

#database initialization
try:
    db = mysql.connector.connect(host="localhost",user="root",password="",database="sensornetwork")
except:
    print("MySQL connection is not found.")
else:
    #gui initialization
    root = Tk()
    root.title("Prototype")
    #root.geometry("750x400")
    myCursor = db.cursor()

    #global variables
    queryView = False

    #first window
    firstWindow = LabelFrame(root)
    firstWindow.grid(row=0,column=0)

    #second window
    secondWindow = LabelFrame(root,text="Optimal conditions")
    secondWindow.grid(row=0,column=1,sticky='n')

    #showOptimal button
    showOptimal = Button(secondWindow,text="Show optimal conditions",command=openOptimalWindow)
    showOptimal.pack()

    #input query frame
    inputQueryFrame = LabelFrame(firstWindow,text="Input Query",padx=5,pady=5)
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
        #query = "Compare the core temperature and humidity from the corn plants"
        #query = "Show humidity from corn within 30 and 60"
        #query = "Show humidity from corn where temperature is between 30 and 60"
        #query = "Has the tomato and corn plant reached optimal conditions"
        #query = "Show humidity from corn greater 30 degrees temperature"

    inputQuery.insert(0,"Has the tomato and corn plant reached optimal conditions")

    #enter button
    enterButton = Button(inputQueryFrame,text="Enter",command=getInputQuery,padx=10)
    enterButton.grid(row=0,column=1)


    #speak query frame
    speakQueryFrame = LabelFrame(firstWindow,padx=5,pady=5,text='Speak Query')
    speakQueryFrame.pack(anchor=W)


    speakLabel = Label(speakQueryFrame,text = "Press the button and state your query")
    speakLabel.grid(row=1,column=0)

    #speak button
    speakButton = Button(speakQueryFrame, text = "Speak",command=speak, padx=10)
    speakButton.grid(row=1,column=1)

    #Output query frame
    outputQueryFrame = LabelFrame(firstWindow,padx=5,pady=5,text='You entered the query')
    outputQueryFrame.pack(anchor=W)

    #Output answer frame
    outputAnswerFrame = LabelFrame(firstWindow,padx=5,pady=5,text='Answer')
    outputAnswerFrame.pack(anchor=W)


    #Output data graph
    outputDataGraph = LabelFrame(firstWindow,text = 'Output Data Graph')
    outputDataGraph.pack()

    

    root.mainloop()