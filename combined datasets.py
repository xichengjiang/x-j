##
## File: assignment07.py (STAT 3250)
## Topic: Assignment 7 
##
import numpy as np # load numpy as np
import pandas as pd # load pandas as pd
import datetime
##  data files: 
##
##      'movies.txt':  A file of over 3900 movies
##      'users.dat':   A file of over 6000 reviewers who provided ratings
##      'ratings.dat': A file of over 1,000,000 movie ratings
##      'zips.txt':    A file of zip codes and location information
##
##  The file 'readme.txt' has more information about the first three files.

movies = open('/Users/jiangxicheng/Desktop/STAT3250/movies.txt').read().splitlines()
users = open('/Users/jiangxicheng/Desktop/STAT3250/users.dat').read().splitlines()
rating = open('/Users/jiangxicheng/Desktop/STAT3250/ratings.dat').read().splitlines()
zips = pd.read_csv('Desktop/STAT3250/zipcodes.txt',
                  usecols = [1,4],
                  converters={'Zipcode':str})
occupid=pd.Series(users).str.split('::').str[3]
#create a dictionary of the names of the occupations 
dict={
    0:  "other or not specified",
	1:  "academic/educator",
	2:  "artist",
	3:  "clerical/admin",
	4:  "college/grad student",
	5:  "customer service",
	6:  "doctor/health care",
	7:  "executive/managerial",
	8:  "farmer",
	9:  "homemaker",
	10:  "K-12 student",
	11:  "lawyer",
	12:  "programmer",
	13:  "retired",
	14:  "sales/marketing",
	15:  "scientist",
	16:  "self-employed",
	17:  "technician/engineer",
	18:  "tradesman/craftsman",
	19:  "unemployed",
	20:  "writer" }
#create a dataframe for users 
dfuser=pd.Series(users).str.split('::',expand=True)
dfuser.columns=['userid','gender','age','occupid','Zipcode']
str.split("-").str[0]
dfuser['Zipcode']=dfuser['Zipcode'].str.split("-").str[0]
str[:5]
dfuser['Occupation']=(dfuser['occupid'].astype(float)).map(dict)  # map the dictionary to the dataframe 
dfmov=pd.Series(movies).str.split('::',expand=True)

## 1.  The percentage of users that are female.  Do the same for the
##     percentage of users in the 35-44 age group.  In the 18-24 age group,
##     determine the percentage of male users.

gender=dfuser['gender']  #extract gender as a column
100*len(gender[gender.str.contains('F')==True])/len(gender)  #percentage that contains female 

age2=dfuser[dfuser['age']=='35']  #dataframe of people between 35 and 44
len(age2)   #number of people between 35 and 44
genf=age2[age2['gender']=='F']  #all females 
100*len(genf)/len(age2)   # the percentage 

age3=dfuser[dfuser['age']=='18']  #dataframe of people between 18--24
len(age3)   #number of people between 35 and 44
genm=age3[age3['gender']=='M']  #all males 
100*len(genm)/len(age3)   # the percentage 

"""
28.2947%  #percentage of users that are female
28.3319%  #percentage of females in the 35-44 age group
72.9828%  #percentage of males In the 18-24 age group
"""

## 2.  Give a year-by-year table of counts for the number of ratings, sorted by
##     year in ascending order.

timeraw=pd.Series(rating).str.split('::').str[3]  #extract the time column
time=pd.to_datetime(timeraw, unit='s')   #convert time to datetime
dftime=time.dt.strftime('%Y')   #create a dataframe for year 
rate=pd.Series(rating).str.split('::').str[2]   #extract the rating column
yr=rate.groupby(dftime).count().sort_values()   #create a table and sort 

"""
2000    904757
2001     68058
2002     24046
2003      3348
"""

## 3.  Determine the average rating for females and the average rating for 
##     males.

df3=dfuser.merge(dfr)
ra=df3[df3['gender'] == "F"]["rating"]   #female rating
np.sum(ra.astype(float))/len(df3[df3['gender'] == "F"])  #average of female 

ra=df3[df3['gender'] == "M"]["rating"]  #male rating 
np.sum(ra.astype(float))/len(df3[df3['gender'] == "M"])   #average for male

"""
3.62036  female
3.56887  males
"""

## 4.  Find the top-10 movies based on average rating.  (Movies and remakes 
##     should be considered different.)  Give a table with the movie title
##     (including the year) and the average rating, sorted by rating from
##     highest to lowest.  (Include ties as needed.)

movid=pd.Series(movies).str.split('::').str[0] #movie id in the movie dataframe
name=pd.Series(movies).str.split('::').str[1]  #movie titles
rateid=pd.Series(rating).str.split('::').str[1]  #movie id in the rating dataframe
rate=pd.Series(rating).str.split('::').str[2]   #movie ratings
dfrate=pd.DataFrame({'ID':rateid, 'rating':rate})   #dataframe of ID and rating 
dfname=pd.DataFrame({'ID':movid, 'name':name})    #dataframe of ID and movie title 
df=pd.merge(dfrate,dfname,on='ID')     #merge the two dataframes
grouprate=df['rating'].astype(float).groupby(df['name'])   #convert rating to floats and group by movie title 
grouprate.mean().sort_values(ascending=False)[:19]   #sort the mean of each movie rating

"""
name
Gate of Heavenly Peace, The (1995)                                     5.000000
Lured (1947)                                                           5.000000
Ulysses (Ulisse) (1954)                                                5.000000
Smashing Time (1967)                                                   5.000000
Follow the Bitch (1998)                                                5.000000
Song of Freedom (1936)                                                 5.000000
Bittersweet Motel (2000)                                               5.000000
Baby, The (1973)                                                       5.000000
One Little Indian (1973)                                               5.000000
Schlafes Bruder (Brother of Sleep) (1995)                              5.000000
I Am Cuba (Soy Cuba/Ya Kuba) (1964)                                    4.800000
Lamerica (1994)                                                        4.750000
Apple, The (Sib) (1998)                                                4.666667
Sanjuro (1962)                                                         4.608696
Seven Samurai (The Magnificent Seven) (Shichinin no samurai) (1954)    4.560510
Shawshank Redemption, The (1994)                                       4.554558
Godfather, The (1972)                                                  4.524966
Close Shave, A (1995)                                                  4.520548
Usual Suspects, The (1995)                                             4.517106
"""

## 5.  Determine the number of movies listed in 'movies.txt' for which there
##     is no rating.  Determine the percentage of these unrated movies for
##     which there is a more recent remake.

numrate=rateid.groupby(rateid).count()    #count the ids in rating 
nummovie=movid.groupby(movid).count()    #count the ids in movies 
len(nummovie)-len(numrate)     #calculate the difference

notin=mov[~mov['ID'].isin(dfrate['ID'])]  #check if movieid is in rating 
name_only=notin['titles'].str[:-6]   #strip the years in the movie 
np.sum(name_only.value_counts()!=1)    #count the number 

"""
177
0  # number of 
"""

## 6.  Determine the average rating for each occupation classification 
##     (including 'other or not specified')

occup=pd.Series(users).str.split('::').str[3]  #extract the occupation column 
useid=pd.Series(users).str.split('::').str[0]   #user id 
df1=pd.DataFrame({'ID': useid, 'OccupationID': occup})  #create a dataframe with user id and occupation
df1['Occupation']=(df1['OccupationID'].astype(float)).map(dict)  # map the dictionary to the dataframe 
df4=pd.merge(df1,df2,on='ID')  #merge two dataframes 
df4['rating'].groupby(df4['Occupation']).mean().sort_values(ascending=False)
#group ratings by occupation title and sort from the highest 
"""
Occupation
Occupation
retired                   3.781736
scientist                 3.689774
doctor/health care        3.661578
homemaker                 3.656589
clerical/admin            3.656516
programmer                3.654001
sales/marketing           3.618481
lawyer                    3.617371
technician/engineer       3.613574
executive/managerial      3.599772
self-employed             3.596575
academic/educator         3.576642
artist                    3.573081
other or not specified    3.537544
customer service          3.537529
college/grad student      3.536793
K-12 student              3.532675
tradesman/craftsman       3.530117
writer                    3.497392
farmer                    3.466741
unemployed                3.414050
"""

## 7.   the average rating for each genre, and give the results in
##     a table listing genre and average rating in descending order.

genre=pd.Series(movies).str.split('::').str[-1].str.split('|')   #
dfgen=[]
#create a loop to get a list of genres 
for i in genre: 
    for x in (0,len(i)):
        dfgen.append(i[x-1])
gen=set(dfgen)       #print the unique values in dfgen   
result=[]  #create an empty dataframe
genre1=pd.Series(movies).str.split('::').str[-1]   #extract the genre of the movies
#create a loop for each genre and calculate the average rating 
for i in list(gen):
    rateid=pd.merge(dfrate,dfmov[genre1.str.contains(i)],on='ID')
    r=rateid['rating'].astype(float).mean()
    result.append(r)
#create a new dataframe for genre and rating; sort from highest 
dfresult=pd.DataFrame({'Genre':list(gen),'Rating':result}).sort_values(ascending=False,by='Rating')

"""
          Genre    Rating
0     Film-Noir  4.075188
14  Documentary  3.933123
4           War  3.893327
11        Drama  3.766332
9         Crime  3.708679
7     Animation  3.684868
6       Mystery  3.668102
16      Musical  3.665519
1       Western  3.637770
3       Romance  3.607465
5      Thriller  3.570466
10       Comedy  3.522099
17       Action  3.491185
13    Adventure  3.477257
8        Sci-Fi  3.466521
15      Fantasy  3.447371
12   Children's  3.422035
2        Horror  3.215013
"""

## 8.  For the user age category, assume that the user has age at the midpoint
##     of the given range.  (For instance '35-44' has age (35+44)/2 = 39.5)
##     For 'under 18' assume an age of 16, and for '56+' assume an age of 60.
##     For each possible rating (1-5) determine the average age of the raters.

#create a dictionary for mapping
dictage={'1':16,'18':(18+24)/2,'25':(25+34)/2,'35':(35+44)/2,'45':(45+49)/2,'50':(50+55)/2,'56':60}
dfuser
#map the dictionary to age column 
dfuser['age']=dfuser['age'].map(dictage)
#create a dataframe for ratings
dfr=pd.Series(rating).str.split('::',expand=True)
#name the columns 
dfr.columns=['userid','ID','rating','timestamp']
#merge rating and age
userrate=pd.merge(dfuser,pd.DataFrame(dfr),on='userid')
#calculate the mean of age in each rating
(userrate['age'].astype(float)).groupby(userrate['rating']).mean()

"""
rating
1    31.710783
2    32.769485
3    33.840672
4    34.270909
5    34.368274
"""

## 9.  all combinations (if there are any) of occupation and genre for 
##     which there are no ratings.  

userrate=pd.merge(dfuser,dfr,on='userid')
df9=userrate.merge(dfmov)
df9a=df9['rating'].groupby([df9['Occupation'],df9['genres']]).size().reset_index(name='count')
df9a[df9a['count']==0]


"""
0
#there are no combination
"""

## 10. For each age group, determine the occupation that gave the lowest 
##     average rating.  Give a table that includes the age group, occupation,
##     and average rating.  (Sort by age group from youngest to oldest) 

df2=pd.merge(dfuser,dfr,on='userid')  #merge occupation and rating 
df3=(df2['rating'].astype(float)).groupby([df2['age'],df2['Occupation']]).mean()  #group rating by age and occupation
#group age by rating and occupation 
df3.columns = ['age','occupation','rating']  #name the columns
df3.groupby(level=0, group_keys=False).nsmallest(1) #calculate the smallest rating of each occupation 

"""
age  occupation title    
1    lawyer                  3.066667
18   doctor/health care      3.235525
25   unemployed              3.366426
35   farmer                  2.642045
45   college/grad student    3.280000
50   farmer                  3.437610
56   sales/marketing         3.291755
"""

## 11. Find the top-5 states in terms of average rating.  Give in table form
##     including the state and average rating, sorted from highest to lowest.
##     Note: If any of the zip codes in 'users.dat' includes letters, then we
##     classify that user as being from Canada, which we treat as a state for
##     this and the next question.

df4=pd.merge(dfuser,zips,on='Zipcode')   #merge users and zipcodes
zips=zips.drop_duplicates()  #drop duplicates
df5=pd.merge(dfr,df4,on='userid')  #merge zipcodes, users and ratings 
(df5['rating'].astype(int)).groupby(df5['State']).mean().sort_values(ascending=False)[:5]
#group ratings by state;sort by descending order 

"""
state
GU    4.236842
MS    3.996409
AK    3.985730
AP    3.938967
SC    3.807748
"""

## 12. For each genre, determine which state produced the most reviews.  
##     (Include any ties.)
dfgen=[]
#create a loop to get a list of genres 
for i in genre: 
    for x in (0,len(i)):
        dfgen.append(i[x-1])
gen=set(dfgen)       #print the unique values in dfgen   
result=[] #create a list
dfuser
#dfu=pd.DataFrame({'userid':dfuser['userid'],'Zipcode':dfuser['Zipcode']})
dfz=pd.merge(dfuser,zips)  #merge userid, zipcode, and zipfile
dfr=pd.Series(rating).str.split('::',expand=True)  #create a dataframe for rating 
dfr.columns=['userid','ID','rating','time']  #name the columns 
dfu=pd.merge(dfr,dfuser,on='userid')  #merge rating and user 
dfx=pd.merge(dfu,dfz)  #merge ratings, users, zipcodes
dfg=pd.merge(dfmov,dfx,on='ID') #merge everything 
#loop over each entry in gender and calculate the number of each state
result=[]
for i in list(gen):
    m=dfg[dfg['genres'].str.contains(i)]
    r=m['State'].groupby(m['State']).count().sort_values(ascending=False)[:1]
    result.append(str(r))
#extract the state and number info 
state=pd.Series(result).str.split('\n').str[1].str.split('    ')
state.str[0]  #define state 
#create a new dataframe that contains genre, state, number 
genstate=pd.DataFrame({'Genre':list(gen),'State':state.str[0],'Number':state.str[1]})
"""

          Genre State  Number
0     Film-Noir    CA    6239
1       Western    CA    6397
2        Horror    CA   23253
3       Romance    CA   45406
4           War    CA   20989
5      Thriller    CA   61704
6       Mystery    CA   13192
7     Animation    CA   13587
8        Sci-Fi    CA   50330
9         Crime    CA   25736
10       Comedy    CA  109518
11        Drama    CA  111456
12   Children's    CA   21920
13    Adventure    CA   42273
14  Documentary    CA    2797
15      Fantasy    CA   10898
16      Musical    CA   12697
17       Action    CA   82536


           Genre State  Number
0     Film-Noir    CA    6243
1       Western    CA    6399
2        Horror    CA   23254
3       Romance    CA   45448
4           War    CA   21010
5      Thriller    CA   61717
6       Mystery    CA   13200
7     Animation    CA   13596
8        Sci-Fi    CA   50343
9         Crime    CA   25742
10       Comedy    CA  109567
11        Drama    CA  111567
12   Children's    CA   21932
13    Adventure    CA   42287
14  Documentary    CA    2797
15      Fantasy    CA   10903
16      Musical    CA   12709
17       Action    CA   82558
"""
