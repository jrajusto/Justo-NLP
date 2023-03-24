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
    queryType.append(r"queryType1: {<NNP|JJ|VB|NN|WP><NN|DT|VBP|VBZ>*<NN|JJ|VBZ>}") #Display temperature from tomato plant
    queryType.append(r"parameters: {<NN|JJ|VBD><JJR|JJ|NN|IN|RBR|VBP|VBZ>?<CD><CD>?}") #humidity is greater than 5 
    queryType.append(r"conjuctions: {<CC>}") #AND OR
    queryType.append(r"adjective: {<JJ>}")
    queryType.append(r"monthQuery: {<DT|JJ|IN><NN>}") #this month or last 
    queryType.append(r"withinParameters: {<NN>?<IN><CD><CD>}") #temperature is within 
    queryType.append(r"date: {<NNP><CD><CD>?}") #from january 5 to january 30
    queryType.append(r"numParam: {<JJR|JJ|NN|IN|RBR|VBP|VBZ><CD><NN|JJ|VBD>?<NN|JJ|VBD>}") #greater than 30 percent humidity

    
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

    optimalBool = True
    
    if 'fahrenheit' in tokens:
        raise Exception('temperature values only in Celsius')
    
    if(len(test1Words) > 0):
        #check if show, get or graph is in the tokens
        for word in test1Words:
            if((word in showSynonyms) or (word in getSynonyms) or (word in graphSynonyms) or (word in compareSynonyms) or (word in outputSynonyms) or (word == "list")or (word == "plot")or (word == "what")):
                print("optimal condition met")
                optimalBool = False
                break
        if not optimalBool:
            for word in test1Words:
                if((word not in showSynonyms) and (word not in getSynonyms) and (word not in graphSynonyms) and (word not in compareSynonyms) and (word not in outputSynonyms)and (word != "check")and (word != "list")and (word != "plot")and (word != "what")):
                    test1Words.remove(word)
                else:
                    break
    print("test 1 words: ")
    print(test1Words)




    parameterList = ['temperature','humidity','air','soil','light','moisture']
    parameterToSQL = {'temperature':'Temperature','humidity':'Humidity','air':'Air_Quality','soil':'Soil_Moisture','light':'Light_Intensity','moisture':'Soil_Moisture'}

    operationList = ['greater','le','equal']
    adjectiveList = ['optimal','good']

    #getting dates
    currentYear,currentMonth,currentDay,fullDate = p.getDate()
    print("Current Date")
    print(p.getDate())


    if(optimalBool):
        
        print('running optimal test')
            
        
        for word in lemmatized_tokens:
    
            if word in plantList:
                entries = ['ID','Date_n_Time']
                
                print("found the plant")
                plantNames.append(word)

                sqlQuery = "SELECT ID, Date_n_Time"
                specificBool = False
                soilMoistureFound = False
                for word in lemmatized_tokens:
                    if word in parameterList:
                        specificBool = True
                        if parameterToSQL[word] == 'Soil_Moisture' and soilMoistureFound == False:
                            soilMoistureFound = True
                            sqlQuery = sqlQuery + ", " + parameterToSQL[word] 
                        elif  parameterToSQL[word] != 'Soil_Moisture':
                            sqlQuery = sqlQuery + ", " + parameterToSQL[word] 
                if not specificBool:
                    for word in lemmatized_tokens:
                        if word in parameterList:
                            specificBool = True
                            if parameterToSQL[word] == 'Soil_Moisture' and soilMoistureFound == False:
                                soilMoistureFound = True
                                sqlQuery = sqlQuery + ", " + parameterToSQL[word] 
                            elif  parameterToSQL[word] != 'Soil_Moisture':
                                sqlQuery = sqlQuery + ", " + parameterToSQL[word] 

                chunk_adjective = nltk.RegexpParser(queryType[3])
                chunk_adjective = chunk_adjective.parse(pos_tags)
                
                adjectiveWordList, adjectiveTaglist = p.getNodes("adjective",chunk_adjective)

                print("adjectiveWordList")
                print(adjectiveWordList)

                if adjectiveWordList:
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
                else:
                        sqlQuery = "SELECT * FROM sensor_node_3_tb "
                whereOnce = False
                andDelay = 0

                #add conditions of optimal plant
                soilMoistureFound == False
                for word in tokens:
                    if word in parameterList and not((word == 'soil' or word == 'moisture') and soilMoistureFound )and parameterToSQL[word] not in entries:
                        if whereOnce == False:
                            sqlQuery = sqlQuery + "WHERE ("
                            whereOnce = True
                        
                        if andDelay == 1:
                            sqlQuery = sqlQuery + " OR"
                            print('pass')

                        if andDelay == 0:
                            andDelay = 1
                        
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
                            soilMoistureFound = True

                        elif word == "moisture":
                            sqlQuery = sqlQuery + " Soil_Moisture < " + str(optimalPlant.soilMoisture)
                            entries.append('Soil_Moisture')
                            soilMoistureFound = True

                        elif word == "light":
                            sqlQuery = sqlQuery + " Light_Intensity < " + str(optimalPlant.lightIntensity) 
                            entries.append('Light_Intensity')

                if whereOnce:
                    sqlQuery = sqlQuery + ")"

                if specificBool != True:
                    sqlQuery = sqlQuery + " WHERE (Temperature < " + str(optimalPlant.temperature) + " OR Humidity < " + str(optimalPlant.humidity) + " OR Air_Quality < " +str(optimalPlant.airQuality) + " OR Soil_Moisture < " + str(optimalPlant.soilMoisture) +  " OR Light_Intensity < " +str(optimalPlant.lightIntensity)+")"
                    entries.append('Temperature')
                    entries.append('Humidity')
                    entries.append('Light_Intensity')
                    entries.append('Soil_Moisture')
                    entries.append('Air_Quality')



                if 'month' in clean_tokens: #last month token
                    year = currentYear
                    if 'last' in clean_tokens or 'previous' in clean_tokens or 'past' in clean_tokens:
                        
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

        if "all plants" in query or not plantNames:
            for plant in plantList:
                plantNames.append(plant)

            for count in range (1,5):
                sqlQuery = "SELECT * FROM sensor_node_"+str(count)+ "_tb "
                whereOnce = False
                andDelay = 0

                if count == 1:
                    optimalPlant = optimalPlant1
                elif count == 2:
                    optimalPlant = optimalPlant2
                elif count == 3:
                    optimalPlant = optimalPlant3
                elif count == 4:
                    optimalPlant = optimalPlant4


                #add conditions of optimal plant
                specificBool = False
                entries = ['ID','Date_n_Time']
                soilMoistureFound = False
                for word in tokens:
                    if word in parameterList and not((word == 'soil' or word == 'moisture') and soilMoistureFound) and parameterToSQL[word] not in entries:
                        
                        specificBool = True
                        if whereOnce == False:
                            sqlQuery = sqlQuery + "WHERE"
                            whereOnce = True
                        
                        if andDelay == 1:
                            sqlQuery = sqlQuery + " OR"
                            print('pass')

                        if andDelay == 0:
                            andDelay = 1
                        
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
                            soilMoistureFound = True
                        elif word == "moisture":
                            sqlQuery = sqlQuery + " Soil_Moisture < " + str(optimalPlant.soilMoisture)
                            entries.append('Soil_Moisture')
                            soilMoistureFound = True

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
                

#------------------------------------------------------------------------------------------------------------------------------------
    #finding action
    elif(len(test1Words) > 0):

    
            if(test1Words[0] in graphSynonyms or test1Words[0] == "plot"):
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
            paramFound = False

            chunk_numParam = nltk.RegexpParser(queryType[7])
            chunk_numParam = chunk_numParam.parse(pos_tags)

            chunkParamList, chunkParamTags = p.getNodes("numParam",chunk_numParam)
            print("numParam:")
            print(chunkParamList)
            
            numParamBool = False
           
            if chunkParamList:
                chunkParamList = chunkParamList[0]
                lenChunkParamList = len(chunkParamList)
                conditionString = []
                if chunkParamList[lenChunkParamList-1] in parameterList:
                    numParamBool = True
                else:
                    numParamBool = False
                
                print("numparambool")
                print(numParamBool)

            if numParamBool:
                wordList = chunkParamList
                if lenChunkParamList == 4:
                    if wordList[0] == operationList[0] or wordList[0] in greaterSynonyms or wordList[0] in aboveSynonyms or wordList[0] in moreSynonyms:
                        conditionString.append(parameterToSQL[wordList[3]] +' > ' + str(w2n.word_to_num(wordList[1])))
                    elif wordList[0] == operationList[0] or wordList[0] in belowSynonyms:
                        conditionString.append(parameterToSQL[wordList[3]] +' < ' + str(w2n.word_to_num(wordList[1])))
                    elif wordList[0] == operationList[0] or wordList[0] in equalSynonyms:
                        conditionString.append(parameterToSQL[wordList[3]] +' = ' + str(w2n.word_to_num(wordList[1])))
                    else:
                        conditionString.append(parameterToSQL[wordList[3]] +' = ' + str(w2n.word_to_num(wordList[1])))
                elif lenChunkParamList == 5:
                    if wordList[4] in parameterList:
                        if wordList[0] == operationList[0] or wordList[0] in greaterSynonyms or wordList[0] in aboveSynonyms or wordList[0] in moreSynonyms:
                            conditionString.append(parameterToSQL[wordList[4]] +' > ' + str(w2n.word_to_num(wordList[1])))
                        elif wordList[0] == operationList[0] or wordList[0] in belowSynonyms:
                            conditionString.append(parameterToSQL[wordList[4]] +' < ' + str(w2n.word_to_num(wordList[1])))
                        elif wordList[0] == operationList[0] or wordList[0] in equalSynonyms:
                            conditionString.append(parameterToSQL[wordList[4]] +' = ' + str(w2n.word_to_num(wordList[1])))
                        else:
                            conditionString.append(parameterToSQL[wordList[4]] +' = ' + str(w2n.word_to_num(wordList[1])))
                elif lenChunkParamList == 3:
                    if wordList[2] in parameterList:
                        if wordList[0] == operationList[0] or wordList[0] in greaterSynonyms or wordList[0] in aboveSynonyms or wordList[0] in moreSynonyms:
                            conditionString.append(parameterToSQL[wordList[2]] +' > ' + str(w2n.word_to_num(wordList[1])))
                        elif wordList[0] == operationList[0] or wordList[0] in belowSynonyms:
                            conditionString.append(parameterToSQL[wordList[2]] +' < ' + str(w2n.word_to_num(wordList[1])))
                        elif wordList[0] == operationList[0] or wordList[0] in equalSynonyms:
                            conditionString.append(parameterToSQL[wordList[2]] +' = ' + str(w2n.word_to_num(wordList[1])))
                        else:
                            conditionString.append(parameterToSQL[wordList[2]] +' = ' + str(w2n.word_to_num(wordList[1])))
                elif lenChunkParamList == 2:
                    conditionString.append(parameterToSQL[wordList[2]] +' = ' + str(w2n.word_to_num(wordList[1])))
                elif lenChunkParamList == 1:
                    conditionString.append(parameterToSQL[wordList[1]] +' = ' + str(w2n.word_to_num(wordList[0])))
                        
            print("condition string: ")
            print(conditionString)
            if not withinParameterWordList and not numParamBool:
                for wordList in parameterWordList:
                

                    if wordList[0] in parameterList:
                        paramFound = True
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
                        paramFound = True
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
                            elif monthQueryPhrase == 'last' or monthQueryPhrase == 'previous' or monthQueryPhrase == 'past': 
                                lastMonth = str(int(currentMonth)-1)
                                if lastMonth == '0':
                                    lastMonth = "12"
                                    currentYear= str(int(currentYear)-1)
                                dateString = "Date_n_Time > '" + currentYear + "-" + lastMonth + "-1 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + lastMonth + "-" + "30" + " 23:59:59'"

            
            #find plant name in test1 words
            for word in lemmatized_tokens:
                if word in plantList:
                    plantNames.append(word)
            
            if not plantNames:
                for plant in plantList:
                    plantNames.append(plant)

            #final string      
            commaSet = False
            if (test1Words[1] == "everything" or test1Words[1] == 'all') and "all plants" not in query:
                entries.append('Temperature')
                entries.append('Humidity')
                entries.append('Light_Intensity')
                entries.append('Soil_Moisture')
                entries.append('Air_Quality')
                
                finalString = "SELECT * FROM " + plantDict[plantNames[0]]
            else:
                finalString = "SELECT ID, Date_n_Time" 
                showSpecified = False
                soilMoistureFound = False
                for word in test1Words:
                    
                    if word in parameterList:
                        if parameterToSQL[word] == 'Soil_Moisture' and soilMoistureFound == False:
                            soilMoistureFound = True
                            entries.append(parameterToSQL[word])
                            finalString = finalString + ", "
                            finalString = finalString + parameterToSQL[word]
                            showSpecified = True
                        elif  parameterToSQL[word] != 'Soil_Moisture':
                            entries.append(parameterToSQL[word])
                            finalString = finalString + ", "
                            finalString = finalString + parameterToSQL[word]
                            showSpecified = True

                        


                        if withinParameterWordList:
                            if withinParameterExist == False:
                                withinParameter = parameterToSQL[word]
                
                #if paramter shown not specified
                if showSpecified == False:
                    soilMoistureFound = False
                    for word in tokens:
                        if word in parameterList and parameterToSQL[word] not in entries and soilMoistureFound == False and parameterToSQL[word] not in entries:
                            soilMoistureFound = True
                            entries.append(parameterToSQL[word])
                            finalString = finalString + ", "
                            finalString = finalString + parameterToSQL[word]
                        elif word in parameterList and parameterToSQL[word] not in entries and parameterToSQL[word] != 'Soil_Moisture' and parameterToSQL[word] not in entries: 
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

    #if showing no parameters
    if len(entries) == 2:
        raise Exception('no parameters given')

    print("headings")
    print(entries)
    #returns the final translated string, and the headings of the parameters
    print(finalQueries, entries,graphBool,compareBool,optimalBool, averageBool,plantNames)
    return finalQueries, entries,graphBool,compareBool,optimalBool,averageBool, plantNames