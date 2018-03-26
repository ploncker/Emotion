# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:04:47 2018

@author: ashmaro1
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot

# Read EmoBank VAD tagged sentences
meta = pd.read_csv("C:\\Users\\ashmaro1\\Documents\\_Projects\\NSW_Health\\EmoBank-master\\corpus\\meta.tsv", sep='\t|' , encoding='utf-8')
raw = pd.read_csv("C:\\Users\\ashmaro1\\Documents\\_Projects\\NSW_Health\\EmoBank-master\\corpus\\raw.tsv", sep='\t|' , encoding='utf-8')
writer = pd.read_csv("C:\\Users\\ashmaro1\\Documents\\_Projects\\NSW_Health\\EmoBank-master\\corpus\\writer.tsv", sep='\t|' , encoding='utf-8')
df_full = pd.merge(meta, raw, on='id')
df_full = pd.merge(df_full, writer, on='id')
df_full.to_csv("C:\\Users\\ashmaro1\\Documents\\_Projects\\NSW_Health\\EmoBank-master\\corpus\\emotion_corpus.tsv", sep="\t", encoding='UTF-8')

# Read Warriner VAD tagged words
Warriner = pd.read_csv(r"C:\Users\ashmaro1\Documents\_Projects\NSW_Health\emotion\Ratings_Warriner_et_al.txt", sep='\t' , encoding='utf-8')
# map range 1 to 9 to -1 to +1
a = (np.arange(1, 10)-5)/4.0

def normalise(df):
    result = df.copy()
    for col in df.columns[2:]:
        if 'Mean' in col: 
            result[col] = (df[col]-5)/4
        if 'SD' in col:
            prev_col = col.replace('SD','Mean')
            result[col] = (df[col]/df[prev_col])*result[prev_col]
    return result

df = normalise(Warriner)

#create VAD dict
#a_dict = df.set_index(KEY).to_dict()[VALUE]
df['vad'] = list(zip(df['V.Mean.Sum'], df['A.Mean.Sum'], df['D.Mean.Sum']))
df.to_csv(r"C:\Users\ashmaro1\Documents\_Projects\NSW_Health\emotion\Ratings_Warriner_Normalised.tsv", sep="\t", encoding='UTF-8', float_format='%.3f')

VAD = pd.Series(df['vad'].values,index=df.Word).to_dict()
import yaml
with open(r"C:\Users\ashmaro1\Documents\_Projects\NSW_Health\emotion\vad.yml", 'w') as yaml_file:
    yaml.safe_dump(VAD, yaml_file)
