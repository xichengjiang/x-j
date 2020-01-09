##xj2kv Xicheng Jiang 
## File: assignment09.py (STAT 3250)
## Topic: Assignment 9 
##
##  This assignment requires data from the file 
##
##      'ncaa.csv':  NCAA Men's Tournament Scores, 1985-2019
##
##  The organization of the file is fairly clear.  Each record has information
##  about one game, including the year, the teams, the final score, and each 
##  team's tournament seed.  All questions refer only to the data in this
##  file, not to earlier tournaments.

##  Note: The data set is from Data.World, with the addition of the 2019
##  tournament provided by your dedicated instructor.

import pandas as pd
lines = open('/Users/jiangxicheng/Desktop/STAT3250/ncaa.csv').read().splitlines()


## 1.  Find all schools that have won the championship, and make a table that
##     incluldes the school and number of championships, sorted from most to
##     least.

dfdata=pd.Series(lines).str.split(',',expand=True)  #convert to dataframe 
dfdata.columns = dfdata.iloc[0]  #convert the frist row to column names 
df=dfdata.reindex(dfdata.index.drop(0))  #drop the duplicated row 
dfchamp=df[df['Region Name']=='Championship']  #restrict the data to championships only 
ch1=dfchamp[dfchamp.iloc[:,5]> dfchamp.iloc[:,8]].iloc[:,6]  #champions 1
ch2=dfchamp[dfchamp.iloc[:,5]< dfchamp.iloc[:,8]].iloc[:,7]  #champions 2
total_champ=ch1.append(ch2)  #all the champions
total_champ.groupby(total_champ).count().sort_values(ascending=False)
#sort the championships 

"""
Duke              5
Connecticut       4
North Carolina    4
Villanova         3
Kentucky          3
Louisville        2
Kansas            2
Florida           2
Arkansas          1
Indiana           1
Virginia          1
Maryland          1
Michigan          1
Michigan St       1
Syracuse          1
UCLA              1
Arizona           1
"""

## 2.  Find the top-10 schools based on number of tournament appearances.
##     Make a table that incldes the school name and number of appearances,
##     sorted from most to least.  Include all that tie for 10th position
##     if necessary.

tour=df[df['Round']=='1']  #all the schools in tournaments each year 
tour1=tour.iloc[:,[0,6]]  #schools group one 
tour2=tour.iloc[:,[0,7]]  #group two 
tourtot=pd.concat([tour1,tour2])   #total 
#group team by itself inorder to get the count for each team 
tourtot['Team'].groupby(tourtot['Team']).count().sort_values(ascending=False)[:11]

"""
Team
Duke              34
Kansas            34
North Carolina    32
Arizona           32
Kentucky          30
Michigan St       29
Syracuse          28
Texas             26
Louisville        26
Oklahoma          26
Purdue            26
"""

## 3.  Determine the average tournament seed for each school, then make a
##     table with the 10 schools that have the lowest average (hence the
##     best teams). Sort the table from smallest to largest, and include
##     all that tie for 10th position if necessary.

allseed=(df.iloc[:,[0,4,6]]).append(df.iloc[:,[0,7,9]])  #create a df for all the schools including team name and seed 
#group scores by team name and sort from the lowest 
#select top 10 including ties 
allseednew=allseed.drop_duplicates()
#group seed by team and sort 
(allseednew['Seed'].astype(float)).groupby(allseednew['Team']).mean().sort_values()[:10]

"""
Team
Duke               2.176471
Kansas             2.500000
North Carolina     2.718750
Kentucky           3.566667
Connecticut        3.950000
Loyola Illinois    4.000000
Massachusetts      4.375000
Syracuse           4.428571
Arizona            4.437500
Ohio St            4.450000
"""

## 4.  Give a table of the average margin of victory by round, sorted by
##     round in order 1, 2, ....

#create a separate column for margin of victory
df['mov']=abs(df.iloc[:,5].astype(float)-df.iloc[:,8].astype(float))
#group margin of victory by rounds
df['mov'].groupby(df.iloc[:,1].astype(float)).mean()

"""
Round
1.0    12.956250
2.0    11.275000
3.0     9.917857
4.0     9.707143
5.0     9.485714
6.0     8.257143
"""

## 5.  Give a table of the percentage of wins by the higher seed by round,
##     sorted by round in order 1, 2, 3, ...

df1=(df.iloc[:,4]>df.iloc[:,9])& (df.iloc[:,5]<df.iloc[:,8])  #wins of the higher seed 
df2=(df.iloc[:,4]<df.iloc[:,9])& (df.iloc[:,5]>df.iloc[:,8])  #wins of the higher seed 
seedwin=df[df1].append(df[df2])
wincount=seedwin['Round'].groupby(seedwin['Round']).count() #count the wins
allcount=df['Round'].groupby(df['Round']).count()  #all counts 
100*wincount/allcount  #percentage 

"""
Round
1    37.500000
2    59.464286
3    62.500000
4    50.714286
5    42.857143
6    54.285714
"""

## 6.  Determine the average seed for all teams in the Final Four for each
##     year.  Give a table of the top-5 in terms of the lowest average seed
##     (hence teams thought to be better) that includes the year and the
##     average, sorted from smallest to largest.

finalfour=df[df['Region Name']=='Final Four']  #extract the final four dataframe
df4=pd.DataFrame({'Seed':finalfour.iloc[:,4],'Year':finalfour.iloc[:,0]})  #higher seed teams
df5=pd.DataFrame({'Seed':finalfour.iloc[:,9],'Year':finalfour.iloc[:,0]}) #teams with lower seed 
allff=pd.concat([df4,df5])  #concat all the teams and seeds
#sort all values 
allff['Seed'].astype(float).groupby(allff['Year']).mean().sort_values()[:9]

"""
Year
2008    1.00
1993    1.25
2007    1.50
2001    1.75
1999    1.75
1997    1.75
1991    1.75
2009    1.75
"""

## 7.  For the first round, determine the percentage of wins by the higher
##     seed for the 1-16 games, for the 2-15 games, ..., for the 8-9 games.
##     Give a table of the above groupings and the percentage, sorted
##     in the order given.


seedgame=df[df['Round']=='1']  #extract the dataframe for round 
gp1=seedgame[seedgame.iloc[:,5].astype(float)>seedgame.iloc[:,8].astype(float)]  #wins by higher seed
allseed=gp1.iloc[:,4].value_counts() #group by counts
seedgame.iloc[:,4].value_counts() #see the number of counts of all seeds
result=100*allseed/140  #the percentage 
#create a dictionary
dict={'1':'1-16','2':'2-15','3':'3-14','4':'4-13','5':'5-12','6':'6-11','7':'7-10','8':'8-9'}
#convert groupby object to dataframe
dfresult=result.reset_index()
#create a column by mapping
dfresult['game']=dfresult['index'].map(dict)
#sort
dfresult.sort_values(by=['index'])
del dfresult['index']  #get rid of the index name 
dfresult

"""
        Seed  game
0  99.285714  1-16
1  94.285714  2-15
2  85.000000  3-14
3  79.285714  4-13
4  64.285714  5-12
5  62.857143  6-11
6  60.714286  7-10
7  48.571429   8-9
"""

## 8.  For each champion, determine the average margin of victory in all
##     games played by that team.  Make a table to the top-10 in terms of
##     average margin, sorted from highest to lowest.  Include all that tie
##     for 10th position if necessary.

dfchamp=df[df['Region Name']=='Championship']  #all championships 
dfchamp['mov']=abs(dfchamp.iloc[:,5].astype(float)-dfchamp.iloc[:,8].astype(float))
ch1=dfchamp[dfchamp.iloc[:,5]>dfchamp.iloc[:,8]].iloc[:,[0,6]]  #wins 1
ch2=dfchamp[dfchamp.iloc[:,5]<dfchamp.iloc[:,8]].iloc[:,[0,7]]  #wins 2
all=ch1.append(ch2)   #combine the two champion columns    
all.columns=['Year','Team']  #columns of year and team 
df['mov']=abs(df.iloc[:,5].astype(float)-df.iloc[:,8].astype(float))  #
dftot=df.iloc[:,[0,6,-1]].append(df.iloc[:,[0,7,-1]])
dftot.columns=['Year','Team','mov']
tot=((dftot['mov'].astype(float)).groupby([dftot['Year'],dftot['Team']]).mean()).reset_index()
Team_all=pd.merge(all, tot, how='inner')
Team_all.sort_values(by='mov',ascending=False)[0:10]

"""
    Year            Team        mov
20  1996        Kentucky  21.500000
13  2016       Villanova  20.666667
30  2009  North Carolina  20.166667
34  2018       Villanova  17.666667
24  2001            Duke  16.666667
11  2013      Louisville  16.166667
29  2006         Florida  16.000000
18  1993  North Carolina  15.666667
32  2015            Duke  15.500000
16  1990            Duke  15.500000
"""

## 9.  For each champion, determine the average seed of all opponents of that
##     team.  Make a table of top-10 in terms of average seed, sorted from 
##     highest to lowest.  Include all that tie for 10th position if necessary.
##     Then make a table of the bottom-10, sorted from lowest to highest.
##     Again include all that tie for 10th position if necessary. 

#rename the duplicatedly named columns 
df['Seed1']=df.iloc[:,4]
df['Score1']=df.iloc[:,5]
df['Team1']=df.iloc[:,6]
df['Team2']=df.iloc[:,7]
df['Score2']=df.iloc[:,8]
df['Seed2']=df.iloc[:,9]

#create three columns, year, team and the opponent seed for each team and combine them all together 
df9_1=df[['Year','Team1','Seed2']] 
df9_1.columns=['Year','Team','Opp_seed']
df9_2=df[['Year','Team2','Seed1']]
df9_2.columns=['Year','Team','Opp_seed']
dfopp=pd.concat([df9_1,df9_2])
#group the opponent seed by year and team; find the average 
opp=(dfopp['Opp_seed'].astype(float)).groupby([dfopp['Year'],dfopp['Team']]).mean()
opp1=opp.reset_index()  #reset index 

seedopp=pd.merge(all, opp1, how='inner')  #merge the two df based on year and team 
seedopp.sort_values(by='Opp_seed',ascending=False)[:11]  #sort values from top 
seedopp.sort_values(by='Opp_seed',)[:11]   #sort from bottom 

"""
    Year            Team  Opp_seed
4   1990            UNLV  9.000000
11  2013      Louisville  8.500000
14  2019        Virginia  8.000000
8   2008          Kansas  8.000000
29  2006         Florida  7.666667
0   1986      Louisville  7.500000
23  1999     Connecticut  7.500000
5   1994        Arkansas  7.333333
6   2000     Michigan St  7.166667
28  2005  North Carolina  7.000000
1   1987         Indiana  7.000000

    Year            Team  Opp_seed
15  1985       Villanova  3.333333
12  2014     Connecticut  4.666667
13  2016       Villanova  4.833333
18  1993  North Carolina  5.500000
16  1990            Duke  5.500000
26  2003        Syracuse  5.666667
33  2017  North Carolina  5.666667
30  2009  North Carolina  5.833333
3   1989        Michigan  6.000000
25  2002        Maryland  6.000000
7   2007         Florida  6.000000
"""

## 10. Determine the 2019 champion.
#find the line with championship in 2019.
df10=df[(df['Year']=='2019') & (df['Region Name']=='Championship')]  #find the line of championship in 2019 
df10['Score1']>df10['Score2']  #see if the first team get the higher score 
df10['Team1']  #get the team name 
"""
2205    Virginia
"""
