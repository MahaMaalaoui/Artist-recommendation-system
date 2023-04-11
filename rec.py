import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity


#loading data
data = pd.read_csv("/lastfm-matrix-germany.csv",delimiter=',',encoding='latin-1')

#verify if a user exist
def vef_user(usr_id):

 return(usr_id in data['user'].unique())



#recom popular artist
def rec_pop():
 
 data_pop = data.drop(['user'],axis=1)

 top10_singer=data_pop.sum().sort_values(ascending=False)[:5]

 return(list(top10_singer.index))




#recom random artist
def rec_rand():
 
 art_names=list(data.columns)
 random.choices(art_names, k=5)
 return(random.choices(art_names, k=5))




#find list of artists known(cond=0)/unknown(cond=1) to a user 
def find_sing(usr_id,cond):
 

 data1 = data.loc[(data['user'] == usr_id)].drop(['user'],axis=1)

 data2=data1.loc[:, ~(data1== cond).any()]
 art_names=list(data2.columns)
 return(art_names)




#random_artist
def rand_art(arts):
  if (len(arts)>5):
   return(random.sample(arts, k=5))
  else:
   return(random.sample(arts, k=len(arts)))



#recom_unknown_artist
def rec_unk(usr_id):
 
 unk_art_lst=find_sing(usr_id,0)
 return(rand_art(unk_art_lst))
 





#recom similair singers
def rec_sim(usr_id):
 

 # Get user index
 picked_userid = usr_id
 
 
 
 #no need to user column for computing similarity between users
 #data2 = data.set_index('user')
 data.index = data['user']
 data2=data.drop('user', axis=1)
 


 #compute similarity between users
 user_similarity=pd.DataFrame(cosine_similarity(data2, data2))
 


 # Remove picked user ID from the candidate list
 user_similarity.drop(index=picked_userid,inplace=True)
 


 # Number of similar users to use
 n = 5

 # User similarity threashold
 user_similarity_threshold = 0.3

 # Get top n similar users
 similar_users = user_similarity[user_similarity[picked_userid]>user_similarity_threshold][picked_userid].sort_values(ascending=False)[:n]
 
  
 

   # a small dataframe that contains similar users
 base=pd.DataFrame(columns=data.columns)
 for i in list(similar_users.index):
  data1 = data.loc[(data.index ==i)]
  base=pd.concat([base, data1], axis=0)

   #list of similar singers
 sim_usrs=base.loc[:, ~(base== 0).any()]
 sim_usrs_singer=list(sim_usrs.columns)
  


 # Get list of artist listned by the target user
 usr_sing=find_sing(usr_id,0)
 

 #recommand similair artist
 sim =list(set(sim_usrs_singer) - set(usr_sing))

 return(rand_art(sim))










