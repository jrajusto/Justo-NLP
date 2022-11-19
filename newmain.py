
import preprocess
import process as p
import nltk
from word2number import w2n




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


optimalPlant1 = Plant('tomato',75,30,60,80,200)
optimalPlant2 = Plant('grape',75,30,60,80,200)
optimalPlant3 = Plant('wheat',75,30,60,80,200)
optimalPlant4 = Plant('corn',75,30,60,80,200)


def main():

    plantDict = {
        "tomato":"sensor_node_1_tb",
        "grape":"sensor_node_2_tb",
        "wheat":"sensor_node_3_tb",
        "corn":"sensor_node_4_tb"
    }

    #list of the months
    monthList = ['january','february','march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    monthToDayMax = {'1':'31','2':'28','3':'31','4':'30','5':'31','6':'30','7':'31','8':'30','9':'31','10':'30','11':'31','12':'30'}

    #list of plants available
    plantList = ['tomato','grape','wheat','corn']

    

    #dictionary of the months with number equivalent
    monthDict = {'january':1,'february':2,'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
    
    
    #query = "Show the core temperature from the grapes plants where humidity is greater than 20 or temperature is equal to 30 and temperature is less than 5 in december 2 to december 7 2021"
    #query = "Show the core temperature from the grapes plants where humidity is greater than 20 in december 2 to december 7 2021"
    #query = "Show all from the grapes plants" 
    #query = "Has the tomato plants maintain optimal codition last month"
    #query = "Show the core temperature from the corn plants"
    query = "Graph the core temperature and humidity from the corn plants"



    
    query = query.lower()
    tokens = preprocess.tokenize(query)
    #tokens = preprocess.numToWord(tokens)
    clean_tokens = preprocess.remove_stop_words(tokens)
    lemmatized_tokens = preprocess.lemmatize(clean_tokens)

    pos_tags = preprocess.pos_tagging(lemmatized_tokens)
    print('original')
    orig_pos_tags = preprocess.pos_tagging(tokens)

    queryType = []
    queryType.append(r"queryType1: {<NNP|NN>*<NN|DT><NN>}") #Display temperature from tomato plant
    queryType.append(r"parameters: {<NN><JJR|JJ|NN>?<CD><CD>?}") #humidity is greater than 5 from january 5 to january 30
    queryType.append(r"conjuctions: {<CC>}") #AND OR
    queryType.append(r"adjective: {<JJ>}")


    

    chunk_parserTest1 = nltk.RegexpParser(queryType[0])
    chunk_parserTest1 = chunk_parserTest1.parse(pos_tags)
    print(chunk_parserTest1)
    
    
    #test 1 - with action
    test1Words,test1Tags = p.getNodes("queryType1",chunk_parserTest1)
    print(test1Words)
    test1Words = test1Words[0]
    print(test1Words)

    parameterList = ['temperature','humidity','air','soil','light']
    parameterToSQL = {'temperature':'Temperature','humidity':'Humidity','air':'AirQuality','soil':'SoilMoisture','light':'LightIntensity'}

    operationList = ['greater','le','equal']
    showWords = ['show','display','graph']
    graphWords = ['graph']
    adjectiveList = ['optimal','good']

    #getting dates
    currentYear,currentMonth,currentDay,fullDate = p.getDate()

    #finding action
    if(len(test1Words) > 0):

        if(test1Words[0] not in showWords):

            for word in test1Words:
                if word in plantList:
                    plant = word
                    chunk_adjective = nltk.RegexpParser(queryType[3])
                    chunk_adjective = chunk_adjective.parse(pos_tags)
                    adjectiveWordList, adjectiveTaglist = p.getNodes("adjective",chunk_adjective)
                    sensorNode = plantDict[plant]
                    adjectiveWordList = adjectiveWordList[0]

                    if adjectiveWordList[0] in adjectiveList:
                        if 'month' in tokens:
                            if 'last' in tokens:
                                month = str(int(currentMonth)-1)
                            else:
                                month = currentMonth
                                
                            finalString = "SELECT * FROM " + sensorNode + " WHERE Date_n_Time > " + currentYear + "-" + currentMonth + "-1 00:00:00" + " AND Date_n_Time < " + currentYear + "-" + currentMonth + "-" + monthToDayMax[month] + " 11:59:59"

        else:
            if(test1Words[0] in graphWords):
                graph = 1
            
            #finding parameters
            chunk_parameters = nltk.RegexpParser(queryType[1])
            chunk_parameters = chunk_parameters.parse(pos_tags)
            
            parameterWordList, parameterTagList = p.getNodes("parameters",chunk_parameters)
            print(parameterWordList)

            
            conditionString = []


            for wordList in parameterWordList:
                if wordList[0] in parameterList:
                    if wordList[1] == operationList[0]:
                        conditionString.append(wordList[0]+' > ' + str(w2n.word_to_num(wordList[2])))
                    elif wordList[1] == operationList[1]:
                        conditionString.append(wordList[0]+' < ' + str(w2n.word_to_num(wordList[2])))
                    elif wordList[1] == operationList[2]:
                        conditionString.append(wordList[0]+' = ' + str(w2n.word_to_num(wordList[2])))
                    else:
                        conditionString.append(wordList[0]+' = ' + str(w2n.word_to_num(wordList[1])))
                    print("conditionString")
                    print(conditionString)
                        
            #finding conjunctions
            chunk_conjuctions = nltk.RegexpParser(queryType[2])
            chunk_conjuctions = chunk_conjuctions.parse(orig_pos_tags)

            conjunctionList,conJunctionTags = p.getNodes("conjuctions",chunk_conjuctions)


            #finding datetime
            dateString = None
            currentYear = p.getCurrentYear()
            print(currentYear)

            dateList = []

            for wordList in parameterWordList:
                if wordList[0] in monthList:
                    dateList.append(wordList)

            #if there are two dates given
            if len(dateList) == 2:
                firstDate = dateList[0]
                secondDate = dateList[1]

                #if the first date contains month and date and the second date contains month,date, and year
                if len(firstDate) == 2 and len(secondDate) == 3:
                    secondYear = secondDate[2]
                    if monthDict[firstDate[0]] > monthDict[secondDate[0]]: 
                        firstYear = secondYear - 1
                    else:
                        firstYear = secondYear

                #if the first date and second date both contains month, date, and year
                elif len(firstDate) == 3 and len(secondDate) == 3:
                    secondYear = secondDate[2]
                    firstYear = firstDate[2]
                else:
                    secondYear = currentYear
                    if monthDict[firstDate[0]] > monthDict[secondDate[0]]: 
                        firstYear = secondYear - 1
                    else:
                        firstYear = secondYear
                        
                #YYYY-MM-DD hh: mm: ss.nnn
                dateString = "AND Date_n_Time > '" + str(firstYear) + "-" + str(monthDict[firstDate[0]]) + "-" +  str(firstDate[1]) + " 00:00:00'AND " + "Date_n_Time < '" + str(secondYear) + "-" + str(monthDict[secondDate[0]]) + "-" + str(secondDate[1]) + " 23:59:59'"
                print(dateString)

            elif len(dateList) == 1:
                theDate = dateList[0]
                if len(theDate) == 3:
                    dateString = "AND Date_n_Time = '" + str(theDate[2]) + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) 
                else:
                    dateString = "AND Date_n_Time = '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) 
                



            #final string
            if test1Words[1] == "everything" or test1Words[1] == 'all':
                finalString = "SELECT * FROM " + plantDict[test1Words[2]]
            else:
                finalString = "SELECT Date_n_Time " 
                for word in test1Words:

                    if word in parameterList:
                        finalString = finalString + ", "
                        finalString = finalString + parameterToSQL[word]

                for word in test1Words:
                    if word in plantList:
                        plantName = word
                finalString = finalString + " FROM " + plantDict[plantName]

            if(len(conditionString) > 0 and dateString != None):
                finalString = finalString + " WHERE "
            
            if(len(conditionString) > 0):
                finalString = finalString + "("

            conjunctionListNum = 0
            for i in range(len(conditionString)):
                finalString = finalString + conditionString[i] + " "
                if i < len(conditionString) - 1:
                    finalString = finalString  + conjunctionList[conjunctionListNum][0].upper() + " "
                conjunctionListNum = conjunctionListNum + 1

            if(len(conditionString) > 0):
                finalString = finalString + ") "

            if dateString != None:
                finalString = finalString + dateString
            
    print(finalString)
        



if __name__ == '__main__':
    main()

