#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import unicodecsv as csv
import emoji

#Twitter API credentials
consumer_key = "¡¡"
consumer_secret = "¡¡"
access_key = "¡¡-¡¡"
access_secret = "¡¡"

USER_TO_DUMP = "elonmusk"


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print "...%s tweets downloaded so far" % (len(alltweets))
    
    
    
    #transform the tweepy tweets into a 2D array that will populate the csv    
    outtweets = list()
    for tweet in alltweets:
        texto = tweet.text.encode("utf-8")
        if not "RT " in texto:
            outtweets.append(texto.split())
    
    # Tranformamos todo en una lista y lo limpiamos un poco...         
    corrected_words = 1
    while corrected_words > 0:
        outtweets, corrected_words = clean_tweets(outtweets)
        print("Corrigiendo: %d"%corrected_words)
    
    
    #write the csv    
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f, encoding='utf-8',  delimiter=',')
        writer.writerows(outtweets)
    
    
    pass



def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI

def text_has_emoji(text):
    for character in text:
        if character in emoji.UNICODE_EMOJI:
            return True
    return False

def replace_composed_char(char_det , word_in, list_populate):
    
    if char_det in word_in and len(word_in)>1:
        if word_in[0] == char_det:
            list_populate.append(char_det)
            list_populate.append(word_in[1:].lower())
            return True
        elif word_in[-1] == char_det:
            list_populate.append(word_in[:-1].lower())
            list_populate.append(char_det)
            return True
        else:
            # El caracter esta en el medio y va a joder la vida...
            return True

    return False

def clean_tweets(outtweets):
    
    outtweets_enteros_new = list()
    
    corrected_words = 0
    
    for tweet_entero_act in outtweets:
        
        outtweets_new = list()
        
        for tweet_act in tweet_entero_act:


            if replace_composed_char("(",tweet_act,outtweets_new):
                corrected_words+=1
                continue  
            elif replace_composed_char(")",tweet_act,outtweets_new):
                corrected_words+=1
                continue

                
            elif replace_composed_char(",",tweet_act,outtweets_new):
                corrected_words+=1
                continue
            elif replace_composed_char(";",tweet_act,outtweets_new):
                corrected_words+=1
                continue
            elif replace_composed_char(":",tweet_act,outtweets_new):
                corrected_words+=1
                continue
            elif replace_composed_char("!",tweet_act,outtweets_new):
                corrected_words+=1
                continue    
            elif replace_composed_char("?",tweet_act,outtweets_new):
                corrected_words+=1
                continue
            elif replace_composed_char("¿",tweet_act,outtweets_new):
                corrected_words+=1
                continue    
            elif replace_composed_char("¡",tweet_act,outtweets_new):
                corrected_words+=1
                continue
                
            elif "'" in tweet_act and len(tweet_act) == 1:
                corrected_words+=1
                continue
            elif replace_composed_char("'",tweet_act,outtweets_new):
                corrected_words+=1
                continue    

            elif "\"" in tweet_act and len(tweet_act) == 1:
                corrected_words+=1
                continue
            elif replace_composed_char("\"",tweet_act,outtweets_new):
                corrected_words+=1
                continue

            elif text_has_emoji(tweet_act):
                corrected_words+=1
                continue 

            elif "http" in tweet_act or ".jp" in tweet_act or ".com" in tweet_act or ".js" in tweet_act :
                corrected_words+=1
                continue

            elif "@" in tweet_act :
                #outtweets_new.append('alguien')
                corrected_words+=1
                continue

            elif  "." in tweet_act and len(tweet_act)>1 and not "..." in tweet_act:
                corrected_words+=1
                if tweet_act[0] == '.':
                    outtweets_new.append('.')
                    outtweets_new.append(tweet_act[1:].lower())
                elif tweet_act[-1] == '.':
                    outtweets_new.append(tweet_act[:-1].lower())
                    outtweets_new.append('.')
                else:
                    continue

            elif len(tweet_act)>4 and "..." in tweet_act:
                corrected_words+=1
                if tweet_act[0] == '.':
                    outtweets_new.append(tweet_act[:3])
                    outtweets_new.append(tweet_act[3:].lower())
                elif tweet_act[-1] == '.':
                    outtweets_new.append(tweet_act[:-3].lower())
                    outtweets_new.append(tweet_act[-3:])
                else:
                    continue    



            else:
                outtweets_new.append(tweet_act.lower())
                
        outtweets_enteros_new.append(outtweets_new)
        
    return outtweets_enteros_new, corrected_words




if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets(USER_TO_DUMP)
