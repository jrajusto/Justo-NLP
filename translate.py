import preprocess
import process as p
import nltk
from word2number import w2n
from nltk.corpus import wordnet as wn
from itertools import chain






def convertToSql(query):

    #initial entries list
    entries = ['ID','Date_n_Time']

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
    graphBool = False

    query = query.lower()
    tokens = preprocess.tokenize(query)
    #tokens = preprocess.numToWord(tokens)
    clean_tokens = preprocess.remove_stop_words(tokens)
    lemmatized_tokens = preprocess.lemmatize(clean_tokens)

    pos_tags = preprocess.pos_tagging(lemmatized_tokens)

    print('original')
    orig_pos_tags = preprocess.pos_tagging(tokens)

    queryType = []
    queryType.append(r"queryType1: {<NNP|JJ|NN>*<NN|DT><NN>}") #Display temperature from tomato plant
    queryType.append(r"parameters: {<NN><JJR|JJ|NN>?<CD><CD>?}") #humidity is greater than 5 from january 5 to january 30
    queryType.append(r"conjuctions: {<CC>}") #AND OR
    queryType.append(r"adjective: {<JJ>}")
    queryType.append(r"monthQuery: {<DT|JJ><NN>}") #this month or last month


    
    #parse the query acording to query type 1
    chunk_parserTest1 = nltk.RegexpParser(queryType[0])
    chunk_parserTest1 = chunk_parserTest1.parse(pos_tags)

    print(chunk_parserTest1)
    
    #test 1 - with action
    test1Words,test1Tags = p.getNodes("queryType1",chunk_parserTest1)
    print(test1Words)
    test1Words = test1Words[0]

    tempTest1Words = []
    finalString = None

    synonyms = wn.synsets('graph')
    graphSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('show')
    showSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    print("Show words")
    print(showSynonyms)
    synonyms = wn.synsets('optimal')
    optimalSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    print("Optimal synonyms")
    print(optimalSynonyms)

    synonyms = wn.synsets('good')
    goodSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    print("Good synonyms")
    print(goodSynonyms)

    synonyms = wn.synsets('greater')
    greaterSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    print("Greater synonyms")
    print(greaterSynonyms)

    synonyms = wn.synsets('below')
    belowSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    print("Below synonyms")
    print(belowSynonyms)

    synonyms = wn.synsets('equal')
    equalSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
    print("Below synonyms")
    print(equalSynonyms)



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

        if((test1Words[0] not in showSynonyms) and (test1Words[0] not in graphSynonyms)):
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
                            optimalBool = True

        else:
        

            if(test1Words[0] in graphSynonyms):
                graphBool = True
            #finding parameters
            chunk_parameters = nltk.RegexpParser(queryType[1])
            chunk_parameters = chunk_parameters.parse(pos_tags)
            
            parameterWordList, parameterTagList = p.getNodes("parameters",chunk_parameters)
            print("Parameter word list: ")
            print(parameterWordList)

            
            conditionString = []


            for wordList in parameterWordList:
                print("wordList")
                print(wordList)

                if wordList[0] in parameterList:
                    if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms:
                        conditionString.append(wordList[0]+' > ' + str(w2n.word_to_num(wordList[2])))
                    elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                        conditionString.append(wordList[0]+' < ' + str(w2n.word_to_num(wordList[2])))
                    elif wordList[1] == operationList[2] or wordList[1] in equalSynonyms:
                        conditionString.append(wordList[0]+' = ' + str(w2n.word_to_num(wordList[2])))
                    else:
                        conditionString.append(wordList[0]+' = ' + str(w2n.word_to_num(wordList[1])))
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
                dateString = "Date_n_Time > '" + str(firstYear) + "-" + str(monthDict[firstDate[0]]) + "-" +  str(firstDate[1]) + " 00:00:00'AND " + "Date_n_Time < '" + str(secondYear) + "-" + str(monthDict[secondDate[0]]) + "-" + str(secondDate[1]) + " 23:59:59'"
                print(dateString)

            elif len(dateList) == 1:
                theDate = dateList[0]
                if len(theDate) == 3:
                    dateString = "Date_n_Time = '" + str(theDate[2]) + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) 
                else:
                    dateString = "Date_n_Time = '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) 

            #finding query with this month or last month
            chunk_month = nltk.RegexpParser(queryType[4])
            chunk_month = chunk_month.parse(pos_tags)
            monthQueryList, monthQueryTagList = p.getNodes("monthQuery",chunk_month)

            for monthQueryPhrase in monthQueryList:
                if monthQueryPhrase[0] == 'this': 
                    dateString = "Date_n_Time > '" + currentYear + "-" + currentMonth + "-1 00:00:00'" + " AND Date_n_Time < '" + "2022" + "-" + currentMonth + "-" + "30" + " 11:59:59'"
                elif monthQueryPhrase[0] == 'last': 
                    lastMonth = str(int(currentMonth)-1)
                    dateString = "Date_n_Time > '" + currentYear + "-" + lastMonth + "-1 00:00:00'" + " AND Date_n_Time < '" + "2022" + "-" + lastMonth + "-" + "30" + " 11:59:59'"


            #final string      
            commaSet = False
            if test1Words[1] == "everything" or test1Words[1] == 'all':
                entries.append('Temperature')
                entries.append('Humidity')
                entries.append('LightIntensity')
                entries.append('SoilMoisture')
                entries.append('AirQuality')
                
                finalString = "SELECT * FROM " + plantDict[test1Words[2]]
            else:
                finalString = "SELECT ID, Date_n_Time" 
                for word in test1Words:

                    if word in parameterList:
                        entries.append(parameterToSQL[word])
                        finalString = finalString + ", "
                        finalString = finalString + parameterToSQL[word]

                for word in test1Words:
                    if word in plantList:
                        plantName = word
                finalString = finalString + " FROM " + plantDict[plantName]

            if(len(conditionString) > 0 or dateString != None):
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
                if(len(conditionString) == 0):
                    finalString = finalString + dateString
                else:
                    finalString = finalString + " AND " + dateString
            
    print(finalString)

    #returns the final translated string, and the headings of the parameters
    return finalString, entries,graphBool,optimalBool