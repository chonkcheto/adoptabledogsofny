import numpy as np 
import pandas as pd 
import re
from sklearn.base import BaseEstimator, TransformerMixin 

class TagCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        new = []
        
        for row in X:
            terms = [x.lower() for x in row]
            terms_cleaned = []
            for term in terms:
                term = term.strip()
                if 'foundation' in term:
                    pass 
                else: 
                    if ' and ' in term:
                        sub = term.split(' and ')
                        for subby in sub:
                            terms_cleaned.append(subby)
                    elif ' but ' in term:
                        sub2 = term.split(' but ')
                        for subby2 in sub2:
                            terms_cleaned.append(subby2)
                    elif 'loves ' in term:
                        thing = re.sub('loves ', '', term)
                        terms_cleaned.append(thing)
                    elif 'super ' in term:
                        thing2 = re.sub('super ', '', term)
                        terms_cleaned.append(thing2)
                    else:
                        terms_cleaned.append(term)
                        
            new.append(terms_cleaned)
            
        return pd.Series(new)

class DictEncoder(BaseEstimator, TransformerMixin):
    """ Take a column of list of terms and turn it into a dictionary of term : counts """
    
    def fit(self, X, y=None):
        return self 
    
    def transform(self, X):
        new = []
        for row in X:
            dd = dict()
            if len(row) == 0:
                dd['empty'] = 1
            else:
                for term in row:
                    term2 = term.lower()
                    dd[term2] = 1
            new.append(dd)
            
        return pd.Series(new)

# turn age into age_code
def CodeAge(age):
    if age == "Puppy":
        return 0
    elif age == "Young":
        return 1
    elif age == "Adult":
        return 2
    else:
        return 3

# turn size into size_code 
def CodeSize(size):
    if size == "0-25":
        return 0
    elif size == "26-60":
        return 1
    elif size == "61-100":
        return 2
    else:
        return 3
        
# to true/false # should be able to delete this chunk and the code will be OK 
def MixEncoder(br1, br2):
    if br2 != "Mixed Breed" and (br1 == br2):
        mix = 0
    else:
        mix = 1
    return mix