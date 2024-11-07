import joblib
from sklearn.feature_extraction.text import CountVectorizer

def xgb_predict(sentence):
  data_list = [sentence]
  xg = joblib.load("xgb_model.sav")
  cv = joblib.load("vectorizer.pkl")
  cv2 = CountVectorizer(vocabulary=cv.vocabulary_,lowercase=True,stop_words='english',ngram_range = (1,1))
  X_test1= cv2.transform(data_list)
  predicted2= xg.predict(X_test1)
  return predicted2


def lr_predict(sentence):
  data_list = [sentence]
  lr = joblib.load("logistic_model.sav")
  cv = joblib.load("vectorizer.pkl")
  cv2 = CountVectorizer(vocabulary=cv.vocabulary_,lowercase=True,stop_words='english',ngram_range = (1,1))
  X_test1= cv2.transform(data_list)
  predicted2= lr.predict(X_test1)
  return predicted2

def xgb_suicide(sentence):
  data_list = [sentence]
  xg = joblib.load("suicide_xgb_model.sav")
  cv = joblib.load("suicide_vectorizer.pkl")
  cv2 = CountVectorizer(vocabulary=cv.vocabulary_,lowercase=True,stop_words='english',ngram_range = (1,1))
  X_test1= cv2.transform(data_list)
  predicted2= xg.predict(X_test1)
  return predicted2

def lr_suicide(sentence):
  data_list = [sentence]
  lr = joblib.load("suicide_logistic_model.sav")
  cv = joblib.load("suicide_vectorizer.pkl")
  cv2 = CountVectorizer(vocabulary=cv.vocabulary_,lowercase=True,stop_words='english',ngram_range = (1,1))
  X_test1= cv2.transform(data_list)
  predicted2= lr.predict(X_test1)
  return predicted2
