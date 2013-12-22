pList = ['love', 'cats']
def mood():
    overallMood = 0
    words = ['I', 'LoVe', 'cats!!!']
    for word in words:
        word.strip('.?!,')
        print word
        lowerCaseWord = word.lower()
        if lowerCaseWord in pList:
            overallMood = overallMood+1

    print overallMood

mood()
