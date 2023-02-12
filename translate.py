import preprocess
import process as p
import nltk
from word2number import w2n
from nltk.corpus import wordnet as wn
from itertools import chain



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




def convertToSql(query,optimalPlant1,optimalPlant2,optimalPlant3,optimalPlant4,plantList):

    #initial entries list
    entries = ['ID','Date_n_Time']

    plantDict = {
        optimalPlant1.name:"sensor_node_1_tb",
        optimalPlant2.name:"sensor_node_2_tb",
        optimalPlant3.name:"sensor_node_3_tb",
        optimalPlant4.name:"sensor_node_4_tb"
    }

    #list of the months
    monthList = ['january','february','march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    monthListCap = ['January','February','March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthToDayMax = {'1':'31','2':'28','3':'31','4':'30','5':'31','6':'30','7':'31','8':'30','9':'31','10':'30','11':'31','12':'30'}

    #dictionary of the months with number equivalent
    monthDict = {'January':1,'February':2,'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    graphBool = False
    compareBool = False
    averageBool = False

    query = query.lower()
    tokens = preprocess.tokenize(query)

    for i in range(len(tokens)):
        if tokens[i] in monthList:
            tokens[i] = tokens[i].capitalize()

    clean_tokens = preprocess.remove_stop_words(tokens)
    lemmatized_tokens = preprocess.lemmatize(clean_tokens)

    for token in lemmatized_tokens:
        if token == 'mean' or token == 'average':
            lemmatized_tokens.remove(token)
            averageBool = True


    pos_tags = preprocess.pos_tagging(lemmatized_tokens)

    print('original')
    orig_pos_tags = preprocess.pos_tagging(tokens)

    queryType = []
    queryType.append(r"queryType1: {<NNP|JJ|VB|NN><NN|DT|VBP|VBZ>*<NN|JJ>}") #Display temperature from tomato plant
    queryType.append(r"parameters: {<NN|JJ|VBD><JJR|JJ|NN|IN|RBR|VBP>?<CD><CD>?}") #humidity is greater than 5 
    queryType.append(r"conjuctions: {<CC>}") #AND OR
    queryType.append(r"adjective: {<JJ>}")
    queryType.append(r"monthQuery: {<DT|JJ><NN>}") #this month or last 
    queryType.append(r"withinParameters: {<NN>?<IN><CD><CD>}") #temperature is within 
    queryType.append(r"date: {<NNP><CD><CD>?}") #from january 5 to january 30

    
    #parse the query acording to query type 1
    chunk_parserTest1 = nltk.RegexpParser(queryType[0])
    chunk_parserTest1 = chunk_parserTest1.parse(pos_tags)
    
    
    #test 1 - with action
    test1Words,test1Tags = p.getNodes("queryType1",chunk_parserTest1)
    print("test1Words")
    print(test1Words)
    test1Words = test1Words[0]

    tempTest1Words = []
    finalString = None
    finalQueries = []

    plantName = None
    plantNames = []

    synonyms = wn.synsets('graph')
    graphSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('compare')
    compareSynonyms =set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('show')
    showSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('get')
    getSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('output')
    outputSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('optimal')
    optimalSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('good')
    goodSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('greater')
    greaterSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('above')
    aboveSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('more')
    moreSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('below')
    belowSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('equal')
    equalSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))





    #cutoff the end of the phrase with plant name
    for word in test1Words:
        tempTest1Words.append(word)
        if word in plantList:
            break
    
    test1Words = tempTest1Words
        

    print("test 1 words: ")
    print(test1Words)

    parameterList = ['temperature','humidity','air','soil','light']
    parameterToSQL = {'temperature':'Temperature','humidity':'Humidity','air':'Air_Quality','soil':'Soil_Moisture','light':'Light_Intensity'}

    operationList = ['greater','le','equal']
    adjectiveList = ['optimal','good']

    #getting dates
    currentYear,currentMonth,currentDay,fullDate = p.getDate()
    print("Current Date")
    print(p.getDate())

    optimalBool = False

    #finding action
    if(len(test1Words) > 0):

        #checking for optimal condition if the trigger words for showing or graphing is not seen
        if((test1Words[0] not in showSynonyms) and (test1Words[0] not in getSynonyms) and (test1Words[0] not in graphSynonyms) and (test1Words[0] not in compareSynonyms) and (test1Words[0] not in outputSynonyms)):
            
            print('running optimal test')
            
                    
                    
            
            for word in lemmatized_tokens:

                if word in plantList:
                    
                    print("found the plant")
                    plantNames.append(word)

                    sqlQuery = "SELECT ID, Date_n_Time"
                    specificBool = False

                    for word in test1Words:
                        if word in parameterList:
                            specificBool = True
                            sqlQuery = sqlQuery + ", " + parameterToSQL[word] 


                    chunk_adjective = nltk.RegexpParser(queryType[3])
                    chunk_adjective = chunk_adjective.parse(pos_tags)
                    

                    adjectiveWordList, adjectiveTaglist = p.getNodes("adjective",chunk_adjective)

                    print("adjectiveWordList")
                    print(adjectiveWordList)

                    adjectiveWordList = adjectiveWordList[0]

                    if plantNames[0] == optimalPlant1.name:
                        optimalPlant = optimalPlant1
                        if specificBool:
                            sqlQuery= sqlQuery + " FROM sensor_node_1_tb "
                        else:
                            sqlQuery= "SELECT * FROM sensor_node_1_tb "
                            
                    elif plantNames[0] == optimalPlant2.name:
                        optimalPlant = optimalPlant2
                        if specificBool:
                            sqlQuery= sqlQuery + " FROM sensor_node_2_tb "
                        else:
                            sqlQuery= "SELECT * FROM sensor_node_2_tb "
                    elif plantNames[0] == optimalPlant3.name:
                        optimalPlant = optimalPlant3
                        if specificBool:
                            sqlQuery= sqlQuery + " FROM sensor_node_3_tb "
                        else:
                            sqlQuery= "SELECT * FROM sensor_node_3_tb "
                    elif plantNames[0] == optimalPlant4.name:
                        optimalPlant = optimalPlant4
                        if specificBool:
                            sqlQuery= sqlQuery + " FROM sensor_node_4_tb "
                        else:
                            sqlQuery= "SELECT * FROM sensor_node_4_tb "

                    whereOnce = False
                    andDelay = 0

                    #add conditions of optimal plant
                    for word in test1Words:
                        if word in parameterList:
                            if whereOnce == False:
                                sqlQuery = sqlQuery + "WHERE"
                                whereOnce = True

                            if andDelay == 0:
                                andDelay = 1
                            
                            if andDelay == 1:
                                andDelay = sqlQuery + " OR"
                            
                            if word == "temperature":
                                sqlQuery = sqlQuery + " Temperature < " + str(optimalPlant.temperature)
                                entries.append('Temperature')

                            elif word == "humidity":
                                sqlQuery = sqlQuery + " Humidity < " + str(optimalPlant.humidity)
                                entries.append('Humidity')

                            elif word == "air":
                                sqlQuery = sqlQuery + " Air_Quality < " + str(optimalPlant.airQuality)
                                entries.append('Air_Quality')

                            elif word == "soil":
                                sqlQuery = sqlQuery + " Soil_Moisture < " + str(optimalPlant.soilMoisture)
                                entries.append('Soil_Moisture')

                            elif word == "light":
                                sqlQuery = sqlQuery + " Light_Intensity < " + str(optimalPlant.lightIntensity) 
                                entries.append('Light_Intensity')

                    if specificBool != True:
                        sqlQuery = sqlQuery + " WHERE Temperature < " + str(optimalPlant.temperature) + " OR Humidity < " + str(optimalPlant.humidity) + " OR Air_Quality < " +str(optimalPlant.airQuality) + " OR Soil_Moisture < " + str(optimalPlant.soilMoisture) +  " OR Light_Intensity < " +str(optimalPlant.lightIntensity)
                        entries.append('Temperature')
                        entries.append('Humidity')
                        entries.append('Light_Intensity')
                        entries.append('Soil_Moisture')
                        entries.append('Air_Quality')



                    if 'month' in clean_tokens: #last month token
                        year = currentYear
                        if 'last' in clean_tokens or 'previous' in clean_tokens:
                            
                            if currentMonth == "01":
                                month = "12"
                                year = str(int(currentYear)-1)
                            else:   
                                month = str(int(currentMonth)-1)
                                year = currentYear
                        else:
                            month = str(currentMonth)
                            
                                
                        sqlQuery = sqlQuery + " AND Date_n_Time > '" + year + "-" + month + "-1 00:00:00'" + " AND Date_n_Time < '" + year + "-" + month + "-" + monthToDayMax[month] + " 23:59:59'"
                    
                        if 'today' in clean_tokens:
                            month = str(currentMonth)
                            sqlQuery = sqlQuery + " AND Date_n_Time > '" + currentYear + "-" + month + "-" + currentDay +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + month + "-" + currentDay +" 23:59:59'"

                        if 'yesterday' in clean_tokens:
                            month = str(currentMonth)
                            yesterday = str(int(currentDay)-1)
                            sqlQuery = sqlQuery + " AND Date_n_Time > '" + currentYear + "-" + month + "-" + yesterday +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + month + "-" + yesterday +" 23:59:59'"

                    finalQueries.append(sqlQuery)
                    optimalBool = True


        else: #not optimal condition
        

            if(test1Words[0] in graphSynonyms):
                graphBool = True
                
            if(test1Words[0] in compareSynonyms):
                compareBool = True

            
            #finding between parameters
            chunk_parameters = nltk.RegexpParser(queryType[5])
            chunk_parameters = chunk_parameters.parse(pos_tags)
            
            withinParameterWordList, withinParameterTagWordList = p.getNodes("withinParameters",chunk_parameters)
            print("within Parameter word list: ")
            print(withinParameterWordList)

            if withinParameterWordList:
                withinParameterWordList = withinParameterWordList[0]
                if withinParameterWordList[0] in parameterList:
                    withinParameter =  withinParameterWordList[0]
                    withinParameterExist = True
                    withinParameterWordList.pop(0)
                    withinParameterWordList.pop(0)
                    withinValues = withinParameterWordList
                else:
                    withinParameterExist = False
                    withinParameterWordList.pop(0)
                    withinParameterWordList.pop(0)
                    withinValues = withinParameterWordList
                        
            #finding parameters
            chunk_parameters = nltk.RegexpParser(queryType[1])
            chunk_parameters = chunk_parameters.parse(pos_tags)
            
            parameterWordList, parameterTagList = p.getNodes("parameters",chunk_parameters)
            print("Parameter word list: ")
            print(parameterWordList)

            
            conditionString = []

            if len(withinParameterWordList) < 1:
                for wordList in parameterWordList:

                    if wordList[0] in parameterList:
                        if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms or wordList[1] in aboveSynonyms or wordList[1] in moreSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' > ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' < ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[2] or wordList[1] in equalSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' = ' + str(w2n.word_to_num(wordList[2])))
                        else:
                            conditionString.append(parameterToSQL[wordList[0]] +' = ' + str(w2n.word_to_num(wordList[1])))
                        print("condition string: ")
                        print(conditionString)
                        #condition name is not given
                    elif int(wordList[2]):
                        parameterUsed = test1Words[1]

                        if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms or wordList[1] in aboveSynonyms or wordList[1] in moreSynonyms:
                            conditionString.append(parameterToSQL[parameterUsed] +' > ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                            conditionString.append(parameterToSQL[parameterUsed] +' < ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[2] or wordList[1] in equalSynonyms:
                            conditionString.append(parameterToSQL[parameterUsed] +' = ' + str(w2n.word_to_num(wordList[2])))
                        else:
                            conditionString.append(parameterToSQL[parameterUsed] +' = ' + str(w2n.word_to_num(wordList[1])))
                        print("condition string: ")
                        print(conditionString)

            #finding conjunctions
            chunk_conjuctions = nltk.RegexpParser(queryType[2])
            chunk_conjuctions = chunk_conjuctions.parse(orig_pos_tags)

            conjunctionList,conJunctionTags = p.getNodes("conjuctions",chunk_conjuctions)


            #finding datetime
            dateString = None
            #currentYear = p.getCurrentYear()
            print("current year")
            print(currentYear)

            dateList = []

            #finding between parameters
            chunk_parameters = nltk.RegexpParser(queryType[6])
            chunk_parameters = chunk_parameters.parse(pos_tags)
            
            dateWordList, dateTagList = p.getNodes("date",chunk_parameters)

            print("date word list: ")
            print(dateWordList)

            if dateWordList:
                for wordList in dateWordList:
                    if wordList[0].lower() in monthList:
                        dateList.append(wordList)
            else:
                for word in clean_tokens:
                    if word in monthListCap:
                        month = str(monthDict[word])
                        dateString = "Date_n_Time > '" + currentYear + "-" + month + "-1 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + month + "-" + monthToDayMax[month] + " 23:59:59'"
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
                dateString = "Date_n_Time > '" + str(firstYear) + "-" + str(monthDict[firstDate[0]]) + "-" +  str(firstDate[1]) + " 00:00:00'AND " + "Date_n_Time < '" + str(secondYear) + "-" + str(monthDict[secondDate[0]]) + "-" + str(secondDate[1]) + " 23:59:59'"
                print(dateString)

            elif len(dateList) == 1:
                theDate = dateList[0]
                if len(theDate) == 3:
                    dateString = "Date_n_Time > '" + str(theDate[2]) + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 00:00:00' AND Date_n_Time < '" + str(theDate[2]) + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 23:59:59'"
                else:
                    dateString = "Date_n_Time > '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 00:00:00' AND Date_n_Time < '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 23:59:59'"

            #if asked for data today
            if 'today' in lemmatized_tokens:
                    month = str(currentMonth)
                    dateString = "Date_n_Time > '" + currentYear + "-" + currentMonth + "-" + currentDay +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + currentDay +" 23:59:59'"

            if 'yesterday' in lemmatized_tokens:
                    month = str(currentMonth)
                    yesterday = str(int(currentDay)-1)
                    dateString = "Date_n_Time > '" + currentYear + "-" + currentMonth + "-" + yesterday +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + yesterday +" 23:59:59'"

            #finding query with this month or last month
            chunk_month = nltk.RegexpParser(queryType[4])
            chunk_month = chunk_month.parse(pos_tags)
            monthQueryList, monthQueryTagList = p.getNodes("monthQuery",chunk_month)

            print('Month query list:')
            print(monthQueryList)
            
            if monthQueryList:
                for monthQuery in monthQueryList:
                    if 'month' in monthQuery:
                        for monthQueryPhrase in monthQuery:
                            if monthQueryPhrase == 'this': 
                                dateString = "Date_n_Time > '" + currentYear + "-" + currentMonth + "-1 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + "30" + " 23:59:59'"
                            elif monthQueryPhrase == 'last' or monthQueryPhrase == 'previous': 
                                lastMonth = str(int(currentMonth)-1)
                                if lastMonth == '0':
                                    lastMonth = "12"
                                    currentYear= str(int(currentYear)-1)
                                dateString = "Date_n_Time > '" + currentYear + "-" + lastMonth + "-1 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + lastMonth + "-" + "30" + " 23:59:59'"

            
            #find plant name in test1 words
            for word in clean_tokens:
                if word in plantList:
                    plantNames.append(word)
            
            if not plantNames:
                for plant in plantList:
                    plantNames.append(plant)

            #final string      
            commaSet = False
            if test1Words[1] == "everything" or test1Words[1] == 'all':
                entries.append('Temperature')
                entries.append('Humidity')
                entries.append('Light_Intensity')
                entries.append('Soil_Moisture')
                entries.append('Air_Quality')
                
                finalString = "SELECT * FROM " + plantDict[plantNames[0]]
            else:
                finalString = "SELECT ID, Date_n_Time" 
                showSpecified = False
                for word in test1Words:

                    if word in parameterList:
                        entries.append(parameterToSQL[word])
                        finalString = finalString + ", "
                        finalString = finalString + parameterToSQL[word]
                        showSpecified = True


                        if withinParameterWordList:
                            if withinParameterExist == False:
                                withinParameter = parameterToSQL[word]
                
                #if paramter shown not specified
                if showSpecified == False:
                    for word in lemmatized_tokens:
                        if word in parameterList:
                            entries.append(parameterToSQL[word])
                            finalString = finalString + ", "
                            finalString = finalString + parameterToSQL[word]

 
                try:
                    finalString = finalString + " FROM " + plantDict[plantNames[0]]
                except:
                    print("***plant not found***")
                

            if withinParameterWordList:
                conditionString.append(withinParameter + " > " + withinValues[0] + " AND " + withinParameter + " < " + withinValues[1])


            #see if dateString exist
            print("Date string:")
            print(dateString)

            if(len(conditionString) > 0 or dateString != None):
                finalString = finalString + " WHERE "
            
            if(len(conditionString) > 0):
                finalString = finalString + "("

            conjunctionListNum = 0
            for i in range(len(conditionString)):
                finalString = finalString + conditionString[i] + " "
                if i < len(conditionString) - 1 and len(withinParameterWordList) < 1:
                    finalString = finalString  + conjunctionList[conjunctionListNum][0].upper() + " "
                conjunctionListNum = conjunctionListNum + 1

            if(len(conditionString) > 0):
                finalString = finalString + ") "

            if dateString != None:
                if(len(conditionString) == 0):
                    finalString = finalString + dateString
                else:
                    finalString = finalString + " AND " + dateString
            
            print(finalString)
            finalQueries.append(finalString)
            if len(plantNames) > 1:
                for i in range(1,len(plantNames)):
                    finalQueries.append(finalString.replace(plantDict[plantNames[0]],plantDict[plantNames[i]]))


    #returns the final translated string, and the headings of the parameters
    print(finalQueries, entries,graphBool,compareBool,optimalBool, averageBool,plantNames)
    return finalQueries, entries,graphBool,compareBool,optimalBool,averageBool, plantNames