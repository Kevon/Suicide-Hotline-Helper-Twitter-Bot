import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener, Stream
import sys
import string
import urllib2
import math
import time
from math import sqrt
import atexit
import smtplib

Consumer_key="MUd9wj7EFReddRAIv6MdXQ"
Consumer_secret="oXc0Lqq2JFfgOckvQjBiqAvZzZRfQAHP78je7EAcxc"

Access_token="2245022965-6cSjPgiZYcs8N8hDU5MCft3xKimcYV6cDE8NsRY"
Access_token_secret="CFbW8KN1QYOEgIJw93DQfXwnHbSP3eUbNis7WWNuhDeUW"

Auth = OAuthHandler(Consumer_key, Consumer_secret)
Auth.set_access_token(Access_token, Access_token_secret)

Api = tweepy.API(Auth)

capslist = list(string.ascii_uppercase)

positives = open('pList.txt','r')
negatives = open('nList.txt','r')
pFile = positives.read()
nFile = negatives.read()

pList = pFile.split('\n')
nList = nFile.split('\n')

trackList = []

followingNames = []
followingIDs = Api.friends_ids()

usersTweeted = []

myUserName = "fuckKevon"
myUserInfo = Api.get_user(myUserName)

myEmail = "kevons5252@gmail.com"
botEmail = "hotlinehelperbot@gmail.com"
botEmailPassword = "qw213er4"

triggerWords = ["suicide"]
triggerWords2 = ["depressed", "depression", "anxiety"]
verbs = ["kill", "cut", "shoot", "hang"] #Removed "hurt" from the verbs list since it returns a lot of false positives.
pronouns = ["me", "myself", "i", "my", "i'm", "i've", "i'll", "i'd"]
desires = ["want", "will", "could", "would", "should", "commit", "going", "go", "wish", "need", "must", "think", "thinking", "desire", "contemplating"]

#List of words to set the flag variable in the mood() method to false that prevents common false positives of the word suicide.
falsePositives = ["silence", "girls", "girl", "rather", "jk", "lol", "threat", "threatening", "rt", "retweet", "justin", "bieber", "literally", "hair", "funny", "hilarious", "rip", "selfish", "stupid", "murder", "kidding", "you", "your", "youre", "if", "shaving", "out"]

#The "kill myself" is in it's own special condition to prevent the common false positives like "I want to kill my dog after he ate my homework"
#triggerWords2 catches people who are talking about how they are depressed, which doesn't need a desire keyword included since they don't desire to be depressed.

def populateTrackList():
    for t in triggerWords:
        for p in pronouns:
            for d in desires:
                trackList.append(p+" "+t+" "+d)

    for v in verbs:
        for d in desires:
            trackList.append(v+" myself i "+d)

    #Took the second set of trigger words out for the time being since they return a lot of false positives.
    for t in triggerWords2:
        for p in pronouns:
           #trackList.append(t+" "+p)
           pass

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

def reply(postID, name):
    replyText = "@"+name+" No matter what you're dealing with, hurting yourself isn't the answer. Please call 1-800-273-8255 if you need to talk."
    try:
        Api.update_status(replyText, in_reply_to_status_id=postID)
        usersTweeted.append(name)
    except tweepy.TweepError as e:
        errorHandler(e.message[0]['code'])
        #print e

def setFollowing():
    followingIDs = Api.friends_ids()
    for person in followingIDs:
        user = Api.get_user(person)
        followingNames.append(str(user.screen_name))

def buildUsers():
    usersTweeted = []
    u = open('userList.txt','r')
    users = u.read()
    userList = users.split('\n')
    for name in userList:
        usersTweeted.append(name)
    u.close()

def writeUsers():
    u = open('userList.txt','a')
    for name in usersTweeted:
        u.write(name+"\n")
    u.close()

def sendEmail(info, details):
    try:
        message = str(info)+" Error recieved from Twitter.\n"+details
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(botEmail, botEmailPassword)
        server.sendmail(botEmail, myEmail, message)         
        return True
    except SMTPException:
        return False
    
class StdOutListener(StreamListener):
    def on_status(self, status):
            author = str(status.author.screen_name)
            if author in followingNames:
                try:
                    Api.retweet(status.id)
                except tweepy.TweepError as e:
                    errorHandler(e.message[0]['code'])
            elif author not in usersTweeted:
                try:
                    swag = status.retweeted_status.retweet_count
                    #This is just a filler line to see if a Tweet caught in the stream is a retweet, which is something we dont want.
                    #If it doesnt have the retweet_count attribute, then it is not a retweet and throws the AttributeError. Also "pass" doesn't seem to work.
                except AttributeError:
                    tweet = status.text.encode('utf-8')
                    data = mood(tweet)
                    tweetMood = data[0]
                    tweetEmotion = data[1]
                    tweetRatio = data[2]
                    flag = data[3]
                    if flag == True:
                        if tweetMood <= -15.0 and tweetEmotion > 5 and tweetRatio > 10.0 or tweetMood < 20.0 and tweetEmotion >= 15 and tweetRatio > 10.0 or tweetMood < 20.0 and tweetEmotion > 10 and tweetRatio >= 20.0:
                            print tweet
                            reply(status.id, str(status.author.screen_name))

    def on_error(self, status):
        errorHandler(status)

    def on_connect(self):
        buildUsers()
        print "CONNECTED"

    def on_limit(self, track):
        errorHandler(status)
        print "LIMITED"

    def on_timeout(self):
        writeUsers()
        errorHandler(status)
        print "TIMEOUT"

    def on_disconnect(self, notice):
        writeUsers()
        errorHandler(status)
        print "DISCONNECTED"

def run():
    populateTrackList()
    setFollowing()
    buildUsers()
    s = Stream(Auth, StdOutListener())
    s.filter(follow = followingIDs, track = trackList)

def checkConnection():
    try:
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def errorHandler(status):
    if status == 406:
        pass 
        #We don't really care about 406 errors.
    elif status == 413:
        print "413 ERROR: Too many phrases being tracked. The limit is 400... We currently have "+str(len(trackList))+" attributes being tracked."

    elif status == 420:
        print "420 ERROR: Too many connections in a short amount of time and our stream is being rate limited."
        time.sleep(600)

    elif status == 187:
        print "187 ERROR: Duplicate status."

    elif status == 185:
        print "185 ERROR: Post limit has been reached. Going to send an alert email and wait for a half hour before resuming."
        if sendEmail(status, "Bot paused for a half hour."):
            print "Successfully sent email to "+myEmail
        else:
            print "ERROR: Failed to send email to "+myEmail
        time.sleep(1800)

    elif status == 403:
        print "403 ERROR: Forbidden action. Could be a duplicate Tweet."

    elif status == 64:
        print "64 ERROR: Account Suspended. Shutting the bot down."
        if sendEmail(status, "SHUT DOWN: Need to manually restart."):
            print "Successfully sent email to "+myEmail
        else:
            print "ERROR: Failed to send email to "+myEmail
        sys.exit(0)

    else:
        print str(status)+" ERROR: Unknow problem."
    
    #Send me a direct message about the error status if possible... Email me if even that failed.
    try:
        Api.send_direct_message(screen_name=myUserName,text=str(status)+" Error.")
    except tweepy.TweepError as e:
        print "151 ERROR: Too many direct messages sent to myself."
        #Isn't this ironic.
        if sendEmail(status, "Too many DM's send."):
            print "Successfully sent email to "+myEmail
        else:
            print "ERROR: Failed to send email to "+myEmail

@atexit.register
def onExit():
    positives.close()
    negatives.close()
    writeUsers()
    print "Exit Successful. Congrats!"

run()
