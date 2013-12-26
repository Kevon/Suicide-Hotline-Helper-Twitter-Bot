import sys
import math
import string
from math import sqrt
import smtplib

capslist = list(string.ascii_uppercase)

pFile = open('pList.txt','r').read()
nFile = open('nList.txt','r').read()

pList = pFile.split('\n')
nList = nFile.split('\n')

myEmail = "kevons5252@gmail.com"
botEmail = "hotlinehelperbot@gmail.com"
botEmailPassword = "qw213er4"

falsePositives = ["silence", "girls", "girl", "rather", "jk", "lol", "threat", "threatening", "rt", "retweet", "justin", "bieber", "literally", "hair", "funny", "hilarious", "rip", "selfish", "stupid", "murder", "kidding", "you", "your", "youre", "if", "shaving", "out"]

def mood(text):
    overallMood = 0
    overallEmotion = 0
    length = 0
    caps = 2
    ratio = 0
    flag = True
    count = len(text.split())
    exclamations = text.count('!')
    words = text.split()
    if text.find('@') != -1:
        flag = False
    if text.find('#') != -1:
        flag = False
    if exclamations > 0:
        overallEmotion = overallEmotion+2
    previous = ''
    for word in words:
        wordcaps = 0
        tempWord = word.strip(".?~#-!,")
        lowerCaseWord = tempWord.lower()
        if lowerCaseWord in pList:
            if previous == 'not':
                overallMood = overallMood-1
                ratio = ratio + 1
            else:
                overallMood = overallMood+1
            overallEmotion = overallEmotion+1
        if lowerCaseWord in nList:
            if previous == 'not':
                overallMood = overallMood+1
            else:
                overallMood = overallMood-1
                ratio = ratio + 1
            overallEmotion = overallEmotion+1
        if lowerCaseWord == 'fucking' or 'fuckin' or 'very' or 'super':
            exclamations = exclamations+1
            overallEmotion = overallEmotion+1
        if lowerCaseWord in falsePositives:
            flag = False
        for letter in list(word):
            if letter in capslist:
                wordcaps = wordcaps+1
        if wordcaps > 3:
            caps = caps + wordcaps
        previous = lowerCaseWord
    if exclamations == 0:
        exclamations = 1
    elif exclamations == 1:
        exclamations = 2
    elif exclamations == 2:
        exclamations = 2.5
    elif exclamations == 3:
        exclamations = 3
    elif exclamations == 4:
        exclamations = 3.25
    else:
        exclamations = 3.5
    if overallMood != 0:
        length = (1+(((len(text)*1.25)/10)/12))
    finalMood = ((((overallMood * 3) * (length)) * (exclamations)) * (1+(abs(overallMood/2))) * (caps/2))
    ### Adjust and cap it from -100 to 100 ###
    if finalMood > 0.0:
        finalMood = sqrt(20*finalMood)
        if finalMood > 100:
            finalMood = 100
    if finalMood < 0.0:
        finalMood = sqrt(20*abs(finalMood))
        if finalMood > 100:
            finalMood = 100
        finalMood = -finalMood
    finalRatio = ((float(ratio)/float(count)*100.0))
    return (finalMood, overallEmotion, finalRatio, flag)

def sendEmail(info):
    try:
        message = str(info)+" Error recieved from Twitter."
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(botEmail, botEmailPassword)
        server.sendmail(botEmail, myEmail, message)         
        return True
    except SMTPException:
        return False

def run(var):
    print var
    print "Mood = "+str(mood(var)[0])
    print "Emotion = "+str(mood(var)[1])
    print "Ratio = "+str(mood(var)[2])
    print "Flag = "+str(mood(var)[3])
    if mood(var)[0] <= -15.0 and mood(var)[1] > 5 and mood(var)[2] > 8.0 or mood(var)[0] <= 20.0 and mood(var)[1] > 20 and mood(var)[2] > 10.0 or mood(var)[0] <= 18.0 and mood(var)[1] > 5 and mood(var)[2] >= 20.0:
        print "PASS"
    else:
        print "FAIL"
        #sendEmail(101)
    print " "

run("im going to kill myself")
run("im going to commit suicide")
run("i'm so depressed right now")
run("I want to shoot myself in the head when I get home")
run("some day i feel really depressed and just want to curl up and die in my room alone")
run("some days I wash I wasnt alive.")
run("people who are depressed need to get over it. if you want to kill yourself, then do it losers.")
run("i'm so depressed that the simpsons is now over :<")
run("getting grades at school gives me anxiety")
run("I ALWAYS MAKE MISTAKES I SHOULD JUST KILL MYSELF.")
run("i always make mistakes i should just? kill, myself.")
run("i need to cut my hair")
run("I need to cut my hair, but im to lazy to do it myself :p")
run("People have told me that I don't know how they feel. In my life Ive had 2 family members commit suicide and 1 die of cancer Trust me. I know")
run("I'm not serious but I just wanna say if I was this tweet would make it worse. Fuck you guys you aren't helping anyone.")
