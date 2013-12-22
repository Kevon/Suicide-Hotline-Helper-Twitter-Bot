Suicide Hotline Helper Twitter Bot
==================================

A Python script written by Kevin Skompinski that powers the @HotlineHelper Twitter bot which detects Tweets that are suicidal in nature, and posts a reply with the National Suicide Hotline phone number information.

You can view the bot's Twitter page here: https://twitter.com/HotlineHelper

The suicide.py file is the main driver of the bot. PLEASE DO NOT RUN THE SCRIPT WITH THE CRIDENTIALS AS IT IS. It will mess up the bot I already have running, and I will get seriously confused as to what happened. You can feel free to look at my code and learn from it or use it in your own adaptation. 

The stream filter gets tweets that include a suicidal word, a personal pronoun, and an action or desire verb.

I adapted some code from my older Twitter mood analizer project to help with sentiment analysis, help filtering out any false positives and identifying suicidal tweets that have a low mood, a lot of emotion, a high ratio of negative words in context with a suicidal mention, and don't contain any words that are usually false positives like the band Suicide Silence.

The mood() function in particular has been expanded upon and is now more accurate (and I fixed some issues with the old code), and returns not only the mood on a scale of -100 to 100, but also the emotional level of a tweet (There is a difference). 

The numbers I used for the limit were based off of this paper: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3299408/

The bot will also retweet anythings that the account's followers post; usually being something positive about suicide prevention.

It will attemt to send me a direct message if it encounters an error, or e-mail me if there is a serious problem and I need to take action.

The pList and Nlist .txt files are essentially the databases of words I created to help detect and determin the mood and emotion of the tweets, where the words of the string are compared against the words in the file. 

The userList is a list that contains all the users that have been tweeted by the bot in order to prevent duplicates. The file is read when suidice.py runs and is appended when the script exits.

The script runs on Raspberry Pi model B.
