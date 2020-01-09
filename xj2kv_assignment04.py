## 
## name: Xicheng Jiang  computing ID: xj2kv
## File: assignment04.py (STAT 3250)
## Topic: Assignment 4
##
import pandas as pd
import numpy as np
##  This assignment requires the data file 'airline_tweets.csv'.  This file
##  contains records of over 14000 tweets and associated information related
##  to a number of airlines.  You should be able to read this file in using
##  the usual pandas methods.
data = pd.read_csv('/Users/jiangxicheng/Desktop/STAT3250/airline_tweets.csv')
##  Note: Questions 1-9 should be done without the use of loops.  
##        Questions 10-13 can be done with loops.

## 1.  Determine the number of tweets for each airline, indicated by the
##     name in the 'airline' column of the data set.  Give the airline 
##     name and number of tweets in table form.
data['unit_id'].groupby(data['airline']).count() #group tweets by airline
#type and count the number of tweets for each type 

"""
airline           tweets
American          2759
JetBlue           2222
Southwest         2420
US Airways        2913
United            3822
Virgin America     504
"""

## 2.  For each airlines tweets, determine the percentage that are positive,
##     based on the classification in 'airline_sentiment'.  Give a table of
##     airline name and percentage, sorted from largest percentage to smallest.

dfp=data[data['airline_sentiment']=='positive'] #create a dataframe for positive sentiments
m1=dfp['airline_sentiment'].groupby(dfp['airline']).count()  #group sentiments by airline type , and count each type
m2=data['airline_sentiment'].groupby(data['airline']).count() #group sentiments by airline type , and count each type
(100*m1/m2).sort_values(ascending=False) #calculate the percentage of each sentiment, sort by descending order 

"""
airline           Percentage
Virgin America    30.158730
JetBlue           24.482448
Southwest         23.553719
United            12.872841
American          12.178325
US Airways         9.234466
"""

## 3.  List all user names (in the 'name' column) with at least 20 tweets
##     along with the number of tweets for each.  Give the results in table
##     form sorted from most to least.

df2=data['unit_id'].groupby(data['name']).count()  #group the unit id by user name and count each userid under each name 
df2[df2>=20].sort_values(ascending=False)  #filter the count by 20 and sort 

"""
nam            number of tweets
JetBlueNews        63
kbosspotter        32
_mhertz            29
otisday            28
throthra           27
weezerandburnie    23
rossj987           23
MeeestarCoke       22
GREATNESSEOA       22
scoobydoo9749      21
jasemccarty        20
"""

## 4.  Determine the percentage of tweets from users who have more than one
##     tweet in this data set.

df2=data['text'].groupby(data['name']).count()  #group the unit id by user name and count each userid under each name 
ct1=np.sum(df2[df2>1]) #count users who have more than one tweet
tot=np.sum(df2) #total tweets
100*ct1/tot  #percentage 

"""
67.889%  #percentage 
"""

## 5.  Among the negative tweets, which five reasons are the most common?
##     Give the percentage of negative tweets with each of the five most 
##     common reasons.  Sort from most to least common.

neg=data[data['airline_sentiment']=='negative']  #create a dataframe for negative sentiments
rsn=neg['unit_id'].groupby(neg['negativereason']).count().sort_values(ascending=False) #sort the top reasons
totneg=(data['airline_sentiment']=='negative').count()  #count the total negative sentiments
100*rsn[0:5]/totneg  #top 5 reason

"""
#most common reasons among negative tweets
negativereason            percentage
Customer Service Issue    19.877049
Late Flight               11.372951
Can't Tell                 8.128415
Cancelled Flight           5.785519
Lost Luggage               4.945355
"""

## 6.  How many of the tweets for each airline include the phrase "on fleek"?

data['text'].str.contains('on fleek').groupby(data['airline']).sum()  
#group strings that contain 'on fleek' by airline type and count each type 

"""
airline          tweets
American            0
JetBlue           146
Southwest           0
US Airways          0
United              0
Virgin America      0
"""

## 7.  What percentage of tweets included a hashtag?

m=data['text'].str.contains('#')   #see which tweets contain a hashtag 
ct=data['text'].groupby(m).count()  #count how may tweets have the hashtag 
100*ct[1]/(ct[0]+ct[1])   #calculate the percentage of tweets included a hashtag

"""
17.001% # the percentage 
"""

## 8.  How many tweets include a link to a web site?

web=data['text'].str.contains('http')   #see which tweets contain a link 
data['text'].groupby(web).count() #count 

"""
1173  #number of tweets with a link (indictaed by http://)
"""

## 9.  How many of the tweets include an '@' for another user besides the
##     intended airline?

at=data[data['text'].str.count('@')>1]['text'].count()  #extract the text where 
# it has more than one @, and count the total number 

"""
##9
1645  # number of the tweets that include an '@' for another user besides the intended airline
"""


## 10. Suppose that a score of 1 is assigned to each positive tweet, 0 to
##     each neutral tweet, and -1 to each negative tweet.  Determine the
##     mean score for each airline, and give the results in table form with
##     airlines and mean scores, sorted from highest to lowest.

data['C']=0 #set up a new column C 

data.loc[data['airline_sentiment'] == 'positive','C'] = 1
#for positive sentiments, set them to 1 
data.loc[data['airline_sentiment'] == 'neutral','C'] = 0
#for neutral sentiments, set them to 0 
data.loc[data['airline_sentiment'] == 'negative','C'] = -1
#for negative sentiments, set them to -1 

data['C'].groupby(data['airline']).mean().sort_values(ascending=False)
#group the sentiment measurements by airline type and sort. 

"""
airline          Mean Score 
Virgin America   -0.057540
JetBlue          -0.184968
Southwest        -0.254545
United           -0.560178
American         -0.588619
US Airways       -0.684518
"""

## 11. Among the tweets that "@" a user besides the indicated airline, 
##     what percentage include an "@" directed at the other airlines 
##     in this file? (Note: Twitterusernames are not case sensitive, 
##     so '@MyName' is the same as '@MYNAME' which is the same as '@myname'.)


all=pd.Series(['@virginamerica', '@jetblue', '@southwestair','@united','@americanair','@usairways'])
m=data[data['text'].str.count('@')>1]['text'].str.lower()  #tweets that "@" a user besides the indicated airlined
m=data['text'].str.lower()  #lower case for text column 
ct=0
for i in m:  #
    n=i.split()   
    k=np.sum(all.isin(n))
    if k >1: 
        ct+=1
100*ct/len(m)

"""
##
18.7234  #percentage 
"""

## 12. Suppose the same user has two or more tweets in a row, based on how they 
##     appear in the file. For such tweet sequences, determine the percentage
##     for which the most recent tweet (which comes nearest the top of the
##     file) is a positive tweet.

ct1=0  #start ct1 and ct2 with zero 
ct2=0
len(data)
for i in range (1,14639):  #simulate for len(data)-1 times 
    if (data.loc[i,'name']==data.loc[i+1,'name']) & (data.loc[i,'name']!=data.loc[i-1,'name']): 
        ct1+=1  #see if the user tweets in a row 
        if data.loc[i,'airline_sentiment']=='positive':  #check if the recent tweet is positive
            ct2+=1
100*ct2/ct1  #the percentage 

"""
##12 
11.1896  #percentage 
"""

## 13. Give a count for the top-10 hashtags (and ties) in terms of the number 
##     of times each appears.  Give the hashtags and counts in a table
##     sorted from most frequent to least frequent.  (Note: Twitter hashtags
##     are not case sensitive, so '#HashTag', '#HASHtag' and '#hashtag' are
##     all regarded as the same. Also ignore instances of hashtags that are
##     alone with no other characters.)
           
txt=data['text']   #create a dataframe with the text column 
hash=[]   #create an empty list 
for i in range(len(txt)):  #run through every element in the text column 
    t=txt[i].lower().split()    #split every entry in lowercases 
    for m in t:   #find the elements starting with '#'
        if m.startswith('#'):
           hash.append(m)  #append the list with elements starting from # 
pd.Series(hash).value_counts()[1:11]  #get the top 10 hashtags                

"""
#the result 
#destinationdragons    76
#fail                  64
#jetblue               44
#unitedairlines        43
#customerservice       34
#usairways             30
#neveragain            26
#usairwaysfail         26
#americanairlines      25
#united                25
"""