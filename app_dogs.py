import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import streamlit as st 
import re
import dill 

# import what I need for my model to run 
from sklearn.base import BaseEstimator, TransformerMixin 
from sklearn.preprocessing import OneHotEncoder 
from sklearn.feature_extraction import DictVectorizer 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier 
from sklearn.pipeline import Pipeline 

# import custom preprocessing step(s) 
from preprocess import TagCleaner, DictEncoder, MixEncoder

# get list of tags 
with open('traits_v2.pkl', 'rb') as f:
    tags_list = dill.load(f)

# get list of breeds 
with open('dog_breeds.pkl', 'rb') as f:
    breeds_list = dill.load(f)

# load trained model 
with open('model_v2b.pkl', 'rb') as f:
    model = dill.load(f)

st.header('Adoptable Dogs of New York :dog2:')

name = st.text_input("Dog name", "Monsieur Chonkington")
tags = st.multiselect("Traits", tags_list, ['affectionate', 'couch potato'])
gender = st.radio("Gender", ['Male', 'Female'])
breed1 = st.selectbox("Primary breed", breeds_list, index=191)
breed2 = st.selectbox("Secondary breed", breeds_list, index=130)

text = st.text_area("Tell your dog's story", "Monsieur Chonkington is looking for his new best friend!", 
                    max_chars=1000, height=250)

def classify(): 
    # encode mixed status to Yes/No
    mix = MixEncoder(breed1, breed2)
    
    # make dataframe from inputs 
    X = pd.DataFrame({'name': name, 'tags': [tags], 'gender':gender,  
                      'breed.1': breed1, 'breed.2': breed2, 
                      'breed.mix': mix, 'text': text})

    # predict based 
    prediction = model.predict(X) 
    probs = model.predict_proba(X)
    prob0 = probs[0][0]
    prob1 = probs[0][1]
    
    if prediction == 1 and prob1 >= 0.66:
        st.error('Highly unlikely :sob:')
        st.write('Chances of getting adopted in 1 month: ', prob0)
        
    elif prediction == 1 and prob1 >= 0.55:
        st.error('Unlikely :worried:')
        st.write('Chances of getting adopted in 1 month: ', prob0)

    elif prediction == 1:
        st.error('Slightly unlikely :neutral_face:')
        st.write('Chances of getting adopted in 1 month: ', prob0)
        
    elif prediction == 0 and prob0 > 0.66:
        st.success('Dog is :sparkles: POPULAR :sparkles:')
        st.write('Chances of getting adopted in 1 month: ', prob0)

    elif prediction == 0 and prob0 >= 0.55: 
        st.success('Likely :smiley:')
        st.write('Chances of getting adopted in 1 month: ', prob0)

    else:
        st.success('Slightly likely :neutral_face:')
        st.write('Chances of getting adopted in 1 month: ', prob0)

st.button('Will they be adopted in 1 month?', on_click=classify)