#importing the neccesaary packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# READ FAKE RATINGS AND REVIEWS FROM CSV FILE
fandago=pd.read_csv('fandango_scrape.csv')

# RELATION BETWEEN RATINGS AND VOTES USING SCATTERPLOT
plt.figure()
sns.scatterplot(data=fandago,x="RATING",y="VOTES")
plt.show()

# BRING OUT THE YEAR OF EVERY MOVIE

fandago["YEAR"]=fandago["FILM"].apply(lambda title:title.split("(")[-1].replace(")",""))
print(fandago["YEAR"].value_counts())
sns.countplot(data=fandago,x="YEAR")
plt.show()

# GET TOP10 MOVIES WITH HIGHEST NO. OF VOTES

print(fandago.nlargest(10,'VOTES'))

# ZERO VOTE MOVIES
s=fandago["VOTES"]==0
print(s.sum())

#CREATE A NEW DATA FRAME  ONLY HAVING VOTES >0

data=fandago[fandago['VOTES']>0 ]
#print(data)

# VISUALIZE THE RATINGS B/W USER RATING AND DISPLAYED RATING

plt.figure()
sns.kdeplot(data=data,x="RATING",fill=True,clip=[0,5],label="Real_Rating")
sns.kdeplot(data=data,x="STARS",fill=True,clip=[0,5],label="Star_Rating")
plt.legend(loc=(0.3,0.8))
plt.show()
print(data)

# CREATE A NEW COLUMN 'DIFF' WHICH IS DIFF B/W STARS AND TRUE RATINGS
data["diff"]=(data['STARS']-data['RATING']).round(2)
print(data['diff'])

#COUNTPLOT THE 'DIFF' COLUMN
sns.countplot(data=data,x="diff")
plt.show()

# CHECK FOR MOVIE THAT HAS DIFF >=1
print(data[data['diff']>=1])

# other_sites
all_sites=pd.read_csv('all_sites_scores.csv')
print(all_sites.columns)

# ROTTEN CRITICS V/S ROTTEN USER RATINGS
plt.figure()
sns.scatterplot(data=all_sites,x='RottenTomatoes',y='RottenTomatoes_User')
plt.ylim(0,100)
plt.xlim(0,100)
plt.show()
all_sites['Rotten_diff']=all_sites['RottenTomatoes']-all_sites['RottenTomatoes_User']
print(all_sites['Rotten_diff'])
avg=all_sites['Rotten_diff'].apply(abs).mean()
print(avg)

#Create  a Distribution plot for Rotten_diff including negative values:
plt.figure(figsize=(10,4),dpi=100)
sns.histplot(data=all_sites,x='Rotten_diff',kde=True,bins=25)
plt.show()

#Create
# plt.figure(figsize=(4,3),dpi=200)
sns.histplot(x=all_sites['Rotten_diff'].apply(abs),kde=True,bins=25)
plt.show()

# TOP 5 MOVIES USERS RATED HIGHER THAN CRITICS ON AVG
print(all_sites.nsmallest(5,'Rotten_diff')[['FILM','Rotten_diff']])

# TOP 5 MOVIES CRITICS HIGHER THAN USERS RATINGS  ON AVG
print(all_sites.nlargest(5,'Rotten_diff')[['FILM','Rotten_diff']])


# METACRITIC V/S METACRITICS_USER
print(all_sites[['Metacritic','Metacritic_User']])
sns.scatterplot(data=all_sites,x='Metacritic',y='Metacritic_User')
plt.ylim(0,10)
plt.xlim(0,100)
plt.show()

# Metacritic_user_vote_count V/S IMDB_user_vote_count

print(all_sites[['Metacritic_user_vote_count','IMDB_user_vote_count']])
sns.scatterplot(data=all_sites,x='Metacritic_user_vote_count',y='IMDB_user_vote_count')
plt.show()
print(all_sites.nlargest(1,'IMDB_user_vote_count'))
print(all_sites.nlargest(1,'Metacritic_user_vote_count'))

# FANDANGO V/S ALL_SITES

# merge the two tables that have common films
df=pd.merge(fandago,all_sites,on='FILM',how='inner')
print(df)

# normalize all rating columns to 0-5 stars
df['RT_Norm']=np.round(df['RottenTomatoes']/20,1)
df['RTU_Norm']=np.round(df['RottenTomatoes_User']/20,1)
df['Meta_Norm']=np.round(df['Metacritic']/20,1)
df['Meta_U_Norm']=np.round(df['Metacritic_User']/2,1)
df['IMDB_Norm']=np.round(df['IMDB']/2,1)
print(df.columns)

# create a newdataframe with norm scores and stars
norms_score=df[['STARS','RATING','RT_Norm','RTU_Norm','Meta_Norm','Meta_U_Norm','IMDB_Norm']]
print(norms_score)

#Comparing Distribution of scores across sites

def move(ax,new_loc,**kws):
    old_legend=ax.legend_
    handles=old_legend.legendHandles
    labels=[t.get_text() for t in old_legend.get_texts()]
    title=old_legend.get_title().get_text()
    ax.legend(handles,labels,loc=new_loc,title=title,**kws)
fig,ax=plt.subplots(figsize=(6,3),dpi=200)
sns.kdeplot(data=norms_score,shade=True,clip=[0,5],palette='Set1')
move(ax,"upper left")
plt.show()

# compare rt critics v/s ratings by fandago
fig,ax=plt.subplots(figsize=(6,3),dpi=200)
sns.kdeplot(data=norms_score[['RT_Norm','STARS']],shade=True,clip=[0,5],palette='Set1')
move(ax,"upper left")
plt.show()
# hisplot
sns.histplot(data=norms_score,bins=20)
plt.show()