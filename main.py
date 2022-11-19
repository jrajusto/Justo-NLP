from select import select
import pyttsx3 as tts
import speech_recognition as ar
import preprocess
import process


def main():
    verb_count = 0 #no of verbs in the query
    textToSpeech = tts.init()
    textToSpeech.setProperty('rate',150) #changes the speed

    '''
    textToSpeech.say('Type your query') #say the words
    textToSpeech.runAndWait() 
    query = input()  #type query
    '''

    query = "Display the core temperature from the tomato plants where humidity is greater than 5!"
    tokenized_query = preprocess.tokenize(query)  
    lower_tokens = preprocess.lowercase(tokenized_query)
    lemmatized_tokens = preprocess.lemmatize(lower_tokens)
    
    
    lemmatized_clean_tokens = preprocess.remove_stop_words(lemmatized_tokens)
    query_ngrams = preprocess.create_ngram(lemmatized_clean_tokens)

    #lower_clean_tokens = preprocess.remove_stop_words(lower_tokens)

    verb_list,verb_count,noun_list = process.find_verbs(lemmatized_clean_tokens,query_ngrams) 
    for noun in noun_list:
        print(process.find_condition(noun,query_ngrams))

    print(verb_list)
    print(verb_count)
    show_flag = process.verify_verbs(verb_list) #simple display of database data
    print(show_flag)
    print("noun list")
    print(noun_list)

if __name__ == '__main__':
    main()

