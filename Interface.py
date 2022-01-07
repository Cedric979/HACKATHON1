import numpy as np
import pandas as pd
import streamlit as st
import string
from PIL import Image

global link1

df_lyrics_final = pd.read_csv('/Users/cedricpinel/Documents/Wild_Code_School/DATATHON1/Interface/df_lyrics_finel.csv')

def punct(lyrics):
      return lyrics.translate(str.maketrans('', '', string.punctuation))

####
def max_dict(dicto):
    all_values = dicto.items()
    return max(all_values) 

#####
def dict_sum(dicto2):
    return max(list(dicto2.items()), key=lambda x: sum(x[1]))[0]

image = Image.open('Copyright-Logo.png')
st.image(image)
st.title("Let's if you can really spit")
lyrics_one = st.text_area("Paste the Lyrics")

#####
max_similar = 0
similar_w_unique = 0
similar_w_not_unique = 0
def lyrics_comparator(lyrics_one, lyrics_two):
  global max_similar, similar_w_unique, similar_w_not_unique
  df_lyrics = pd.DataFrame(range(0,300),columns={'song1'}) # creating DF to compare
  df_lyrics['song1'] = pd.DataFrame(lyrics_one.split()) 
  df_lyrics['song2'] = pd.DataFrame(lyrics_two.split()) # adding another column with song frm DF
  df_lyrics.rename(columns={0:'song1'},inplace=True) # renaming column
  #Creating column comparison after putting all words lower
  df_lyrics['song1'] = df_lyrics['song1'].apply(lambda item: item.lower() if isinstance(item,str) else item)
  df_lyrics['song2'] = df_lyrics['song2'].apply(lambda item: item.lower()if isinstance(item,str) else item)
  df_lyrics['equal'] = df_lyrics[['song1','song2']].apply(lambda item:  item[0] == item[1] ,axis=1) #1 if str(item[0]) == str(item[1]) else 0,axis=1)#item[0] == item[1] ,axis=1)
  values1 = df_lyrics['song1'].value_counts(dropna=True).keys().tolist()
  counts1 = df_lyrics['song1'].value_counts(dropna=True).tolist()
  value_dict_lyrics1 = dict(zip(values1, counts1))
  values2 = df_lyrics['song2'].value_counts(dropna=True).keys().tolist()
  counts2 = df_lyrics['song2'].value_counts(dropna=True).tolist()
  value_dict_lyrics2 = dict(zip(values2, counts2))
  #Creating the lists to check the similars words but not uniques
  list_song1 = list(lyrics_one.split())
  list_song2 = list(lyrics_two.split())
  dict3 = [w for w in list_song1 if w in list_song2]
  #Obtaining the lenght to show percentage
  song1_len = df_lyrics['song1'].count() 
  song2_len = df_lyrics['song2'].count()
  #Creating a dict to see same word in disorder
  dict2 = [i for i in value_dict_lyrics1.keys() if i in value_dict_lyrics2.keys()]
  # dict2 = {i for i,j in value_dict_lyrics1.items() if i in value_dict_lyrics2}
  #st.write("similar words",dict2)
  #Variable to use outside the function
  similar_w_unique = len(dict2)
  similar_w_not_unique = len(dict3)
  max_similar = df_lyrics['equal'].sum()
  #Temporary to check
  #Rapport to return to the user
  return  similar_w_unique,similar_w_not_unique,max_similar, value_dict_lyrics1, value_dict_lyrics2

lyrics_comparator(df_lyrics_final['Lyric'][0], df_lyrics_final['Lyric'][22])


# Function for the report
max_similar = 0
similar_w_unique = 0
similar_w_not_unique = 0
def lyrics_report(lyrics_one, lyrics_two):
  global max_similar, similar_w_unique, similar_w_not_unique
  df_lyrics = pd.DataFrame(range(0,300),columns={'song1'}) # creating DF to compare
  df_lyrics['song1'] = pd.DataFrame(lyrics_one.split()) 
  df_lyrics['song2'] = pd.DataFrame(lyrics_two.split()) # adding another column with song frm DF
  df_lyrics.rename(columns={0:'song1'},inplace=True) # renaming column
  #Creating column comparison after putting all words lower
  df_lyrics['song1'] = df_lyrics['song1'].apply(lambda item: item.lower() if isinstance(item,str) else item)
  df_lyrics['song2'] = df_lyrics['song2'].apply(lambda item: item.lower()if isinstance(item,str) else item)
  df_lyrics['equal'] = df_lyrics[['song1','song2']].apply(lambda item:  item[0] == item[1] ,axis=1) #1 if str(item[0]) == str(item[1]) else 0,axis=1)#item[0] == item[1] ,axis=1)

  values1 = df_lyrics['song1'].value_counts(dropna=True).keys().tolist()
  counts1 = df_lyrics['song1'].value_counts(dropna=True).tolist()
  value_dict_lyrics1 = dict(zip(values1, counts1))
  values2 = df_lyrics['song2'].value_counts(dropna=True).keys().tolist()
  counts2 = df_lyrics['song2'].value_counts(dropna=True).tolist()
  value_dict_lyrics2 = dict(zip(values2, counts2))
  
  list_song1 = list(lyrics_one.split())
  list_song2 = list(lyrics_two.split())
  dict3 = [w for w in list_song1 if w in list_song2]

  song1_len = df_lyrics['song1'].count() 
  song2_len = df_lyrics['song2'].count()
  
  dict2 = [i for i in value_dict_lyrics1.keys() if i in value_dict_lyrics2.keys()]

  similar_w_unique = len(dict2)
 
  similar_w_not_unique = len(dict3)
 
  max_similar = df_lyrics['equal'].sum()
  st.write("The closest lyrical song contains",song2_len,"words")
  st.write(df_lyrics['equal'].sum(),"words are at the exact same position")
  # st.write("similar unique words",dict2)
  st.write(round((df_lyrics['equal'].sum()/song2_len)*100,2), "% of your song is exactly the same")
  st.write(round((len(dict3)/len(list_song2)) * 100, 2),"% of same words are used")
  #st.write("please find below the list of the words present in your song with the number of appearence")
  #st.write(value_dict_lyrics1,value_dict_lyrics2)
  return similar_w_unique, similar_w_not_unique, max_similar, value_dict_lyrics1, value_dict_lyrics2

final_dict = {}
if st.button('Get info'):
  
    for i in range(1, 1000): #len(df_lyrics_final['Lyric'])):
      
        lyrics_comparator(punct(lyrics_one), punct(df_lyrics_final['Lyric'][i]))
        final_dict[i] = [max_similar,similar_w_unique, similar_w_not_unique]

    lyrics_report(punct(lyrics_one), punct(df_lyrics_final['Lyric'][dict_sum(final_dict)]))
    st.write(df_lyrics_final.iloc[dict_sum(final_dict)][['Artist','Song']]) #veribal 
    link1 = df_lyrics_final.iloc[dict_sum(final_dict)][['SLink']][0]
    #st.write(type(link1))


    #st.write(link1)
    url = f"https://www.vagalume.com.br{link1}"
    st.write(url)

