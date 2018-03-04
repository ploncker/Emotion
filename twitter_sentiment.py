import nltk
import pandas as pd
from nltk.corpus import stopwords
from classes.splitter_postagger_nltk import Splitter, POSTagger, DictionaryTagger

#df = pd.read_csv("C:\\Users\\ashmaro1\\Documents\\_Projects\\NSW_Health\\WestMeadHosp.csv", sep='\t' , encoding='utf-8')
df = pd.read_csv("C:\\Users\\ashmaro1\\Documents\\_Projects\\NSW_Health\\sydneyseige_angela2.csv", sep=',', encoding='utf-8')
#df = dfn[dfn['text'].notnull()]
df = df.dropna(subset = ['text'])
df = df.reset_index(drop=True)

tweets = []
stopwords_set = set(stopwords.words("english"))
    
for item in df['text']:
    words_filtered = [e.lower() for e in item.split() if len(e) >= 2]
    words_cleaned = [word for word in words_filtered
        if 'http' not in word
        and '/' not in word
        and not word.startswith('@')
        and not word.startswith('#')
        and word != 'RT']
    words_without_stopwords = [word for word in words_cleaned if not word in stopwords_set]
    tweets.append(words_cleaned)
    
df['tweets'] = pd.Series(tweets)

    
sentences=[]
for item in tweets:
    str1 = ' '.join(item)
    str1.encode("utf-8")
    sentences.append(str1)


pos=[]
for text in sentences:
    splitter = Splitter()
    postagger = POSTagger()

    splitted_sentences = splitter.split(text)
    print splitted_sentences

    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    print pos_tagged_sentences

    dicttagger = DictionaryTagger([ 'dict/positive.yml', 'dict/negative.yml', 'dict/inc.yml', 'dict/dec.yml', 'dict/inv.yml'])

    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    print dict_tagged_sentences
    pos.append(dict_tagged_sentences)
df['tagged'] = pd.Series(pos)
    
def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0

#---------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------- 
def sentence_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        print "current_token", current_token
        tags = current_token[2]
        print "tags", tags
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            print "previous_tags", previous_tags
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])


    
score = []    
for dict_tagged_sentences in df['tagged']:
    s3 = sentiment_score(dict_tagged_sentences)
    print s3
    score.append(s3)

df['score'] = pd.Series(score)

df.to_csv("C:\\Users\\ashmaro1\\Documents\\_Projects\\NSW_Health\\sydneyseige_angela2.csv", sep='\t' , header=True, encoding='utf-8')