from textblob import TextBlob
import pickle
def is_positive(sentence):
    '''
        Returns True if sentence is neutral/positive,False otherwise
    '''
    with open("datasets/words_dict.bin",'rb') as f:
        words_dict=pickle.load(f)
    score=0
    for word in TextBlob(sentence).words:
        word=word.lemmatize().lower()
        score+=words_dict.get(word,0)
    return score>=0