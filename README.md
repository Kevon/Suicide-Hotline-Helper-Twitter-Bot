Suicide Hotline Helper Twitter Bot
==================================

A Python script written by Kevin Skompinski that powers the @HotlineHelper Twitter bot which detects Tweets that are suicidal in nature, and posts a reply with the National Suicide Hotline phone number information.

The suicide.py file is the main driver of the bot.

The stream filter gets tweets that include a suicidal word, a personal pronoun, and an action or desire verb.

I adapted some code from my older Twitter mood analizer project to help with sentiment analysis, help filtering out any false positives and identifying suicidal tweets that have a low mood, a lot of emotion, a high ratio of negative words in context with a suicidal mention, and don't contain any words that are usually false positives like the band Suicide Silence.  

The numbers I used for the limit were based off of this paper: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3299408/#!po=70.8333

The bot will also retweet anythings that the account's followers post; usually being something positive about suicide prevention.

It will attemt to send me a direct message if it encounters an error, or e-mail me if there is a serious problem and I need to take action.

The script runs on Raspberry Pi.
