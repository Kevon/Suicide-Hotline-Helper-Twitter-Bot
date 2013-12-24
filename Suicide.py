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
from random import choice

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
usersReplied = []

myUserName = "fuckKevon"
myUserInfo = Api.get_user(myUserName)

myEmail = "kevons5252@gmail.com"

botInfo = Api.me()
botName = botInfo.screen_name
botID = botInfo.id

botEmail = "hotlinehelperbot@gmail.com"
botEmailPassword = "qw213er4"

triggerWords = ["suicide"]
triggerWords2 = ["depressed", "depression", "anxiety"]
verbs = ["kill", "cut", "shoot", "hang"] #Removed "hurt" from the verbs list since it returns a lot of false positives.
pronouns = ["me", "myself", "i", "my", "i'm", "i've", "i'll", "i'd"]
desires = ["want", "will", "could", "would", "should", "commit", "going", "go", "wish", "need", "must", "think", "thinking", "desire", "contemplating"]

#List of words to set the flag variable in the mood() method to false that prevents common false positives of the word suicide.
falsePositives = ["silence", "girls", "girl", "rather", "jk", "lol", "threat", "threatening", "rt", "retweet", "justin", "bieber", "literally", "hair", "funny", "hilarious", "rip", "selfish", 
                  "stupid", "murder", "kidding", "you", "your", "youre", "theyre", "if", "shaving", "out", "it", "playlist", "bombers", "bomber", "say", "never", "commited", "when", "trip"]

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
    trackList.append(botName)

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

def reply(postID, name, mood, emotion, ratio, flag):
    replyText = "@"+name+" No matter what you're dealing with, hurting yourself isn't the answer. Please call 1-800-273-8255 if you need to talk."
    if flag == True:
        #Going to slowly ramp up the bot in an effort to prevent it being caught in the spam filter.
        #End values will be tweetMood <= -15.0 and tweetEmotion > 5 and tweetRatio > 10.0 or tweetMood < 20.0 and tweetEmotion >= 15 and tweetRatio > 10.0 or tweetMood < 20.0 and tweetEmotion > 10 and tweetRatio >= 20.0
        #Start values will be 10 more for each section, so we get a smaller number of tweets sent out and they'll only be the ones that are really negative or emotional.
        if mood <= -20.0 and emotion > 5 and ratio > 10.0 or mood < 20.0 and emotion >= 20 and ratio > 10.0 or mood < 20.0 and emotion > 10 and ratio >= 25.0:
            try:
                Api.update_status(replyText, in_reply_to_status_id=postID)
                usersTweeted.append(name)
            except tweepy.TweepError as e:
                errorHandler(e.message[0]['code'])
                #print e
            print tweet

def respond(postID, name, mood):
    positiveResponds = ["<3", "Stay strong!", "Thanks for the support!"]
    negativeResponds = ["Sorry.", "Just trying to help in case you need it..."]
    if mood > 40:
        respondText = "@"+name+" "+choice(positiveResponds)
        try:
            Api.update_status(respondText, in_reply_to_status_id=postID)
            usersReplied.append(name)
        except tweepy.TweepError as e:
            errorHandler(e.message[0]['code'])
    elif mood < -40:
        respondText = "@"+name+" "+choice(negativeResponds)
        try:
            Api.update_status(respondText, in_reply_to_status_id=postID)
            usersReplied.append(name)
        except tweepy.TweepError as e:
            errorHandler(e.message[0]['code'])

def setFollowing():
    followingIDs = Api.friends_ids()
    for person in followingIDs:
        user = Api.get_user(person)
        followingNames.append(str(user.screen_name))
    #followingIDs.append(botID)
    #followingNames.append(botName)

def buildUsers():
    usersTweeted = []
    u = open('userList.txt','r')
    users = u.read()
    userList = users.split('\n')
    for name in userList:
        usersTweeted.append(name)
    u.close()

    usersReplied = []
    r = open('usersReplied.txt','r')
    replied = r.read()
    repliedList = replied.split('\n')
    for name in repliedList:
        usersReplied.append(name)
    r.close()

def writeUsers():
    u = open('userList.txt','a')
    for name in usersTweeted:
        u.write(name+"\n")
    u.close()

    r = open('usersReplied.txt','a')
    for name in usersReplied:
        r.write(name+"\n")
    r.close()

def sendEmail(text, details):
    try:
        message = text+"\n\n"+details
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(botEmail, botEmailPassword)
        server.sendmail(botEmail, myEmail, message)
        print "Successfully sent email to "+myEmail       
        return True
    except SMTPException:
        print "ERROR: Failed to send email to "+myEmail
        return False

def sendDM(text, status):
    try:
        Api.send_direct_message(screen_name=myUserName,text=text)
    except tweepy.TweepError as e:
        error = str(status)+" ERROR: Too many direct messages sent to myself."
        print error
        #Send me an email if the direct message failed.
        sendEmail(error)     
    
class StdOutListener(StreamListener):
    def on_status(self, status):
            tweet = status.text.encode('utf-8')
            author = str(status.author.screen_name)
            mention = tweet.split(' ', 1)[0]
            
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
                    data = mood(tweet)
                    tweetMood = data[0]
                    tweetEmotion = data[1]
                    tweetRatio = data[2]
                    flag = data[3]
                    reply(status.id, str(status.author.screen_name), tweetMood, tweetEmotion, tweetRatio, flag)
            
            elif mention == "@"+botName and author in usersTweeted and author not in usersReplied:
                    data = mood(tweet)
                    tweetMood = data[0]
                    respond(status.id, str(status.author.screen_name), tweetMood)

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
    error = ""
    if status == 406:
        pass 
        #We don't really care about 406 errors.
    elif status == 413:
        error = str(status)+" ERROR: Too many phrases being tracked. The limit is 400... We currently have "+str(len(trackList))+" attributes being tracked."
        print error

    elif status == 420:
        error = str(status)+" ERROR: Too many connections in a short amount of time and our stream is being rate limited."
        print error
        time.sleep(600)

    elif status == 187:
        error = str(status)+" ERROR: Duplicate status."
        print error

    elif status == 185:
        error = str(status)+" ERROR: Post limit has been reached. Going to wait for a half hour before resuming."
        print error
        sendEmail(error)
        time.sleep(1800)

    elif status == 403:
        error = str(status)+" ERROR: Forbidden action. Could be a duplicate Tweet."
        print error

    elif status == 64:
        error = str(status)+" ERROR: Account Suspended. Shutting the bot down."
        print error
        sendEmail(error)
        errorExit()

    else:
        error = str(status)+" ERROR: Unknow problem."
        print error
    
    #Send me a direct message about the error status if possible... Email me if even that failed.
    sendDM(error, status)   

def errorExit():
    sendEmail("BOT SHUT DOWN. NEED TO RESTART!")
    sys.exit(0)

@atexit.register
def onExit():
    positives.close()
    negatives.close()
    writeUsers()
    print "Exit Successful. Congrats!"

run()

#I recently created a Twitter bot that identifies suicidal tweets of users and responds with the phone number for the National Suicide Prevention Lifeline if they need it. I made sure to only return tweets that contain a suicidal trigger word, an action verb or desire word like "want" or "commit" or "think", and a personal pronoun like "myself" or "I" to narrow down the returned tweets to only possibly be tweets that are of someone expressing desire to harm themself. I then performed sentiment analysis to further filter down the returned tweets and only identify ones that are of a really negative mood and highly emotional, as well as filter out most false positives are sarcastic tweets that don't require hotline information.

#The tweets the bot was responding to were accurate for the most part, and will continue to get better as time goes on and I see more ways in which we could eliminate unwanted false positives. So far, the responses from the suicide hotline helper bot were really positive, with a large number of it's responses being favorited and retweeted. 

#I took all measures to implement a way to pull back and wait a while when the account is being rate limited, and the tweets-per-minute the account was making wasn't unreasonable as it was. 

#I'm not a large corporation or a revenue-generating spam-bot. I am simply a recent graduate from SUNY University at Buffalo (my name is Kevin Skompinski and my student email is kevinsko@buffalo.edu) and this was a personal project that I've been meaning to implement for a while now. I generate no money from this and I will never have the intention to do so. However, I feel like this project has the power to really help people if they are in crisis, and could potentially do some good for people in their time of need. I do know the there are automated Twitter bots that reply to people under certain circumstances (@StealthMountain (https://twitter.com/StealthMountain) and @DBZNappa (https://twitter.com/DBZNappa) for example), so there must be ways to impliment a Twitter bot properly and not get suspended. I checked the development site and searched around for answers, but I could not find a reason why this account would be suspended. If it was tweeting too quickly, I could adjust the parameters for the secondary sentiment filtering and increase the mood and emotional thresholds to qualify for a response. If there is possibly anyone to talk to on the development team that would be able to help me avoid this situation again, that would be amazing. Or if there was some protocol to prevent what has caused this and continue to allow the account to operate, that information would be helpful too. I am an avid Twitter user with my main account being @fuckKevon, so I know how the Twitter community works and respect the guidelines in place. 

#Any help would be great, and having the account un-suspended and allowed to run  and help provide information for those in crisis would be phenomenal. 

#Thanks!
#~ Kevin Skompinski