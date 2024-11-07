import streamlit as st
import pandas as pd
import numpy as np
from prediction import xgb_predict, lr_predict, xgb_suicide
import nltk
from nltk import sent_tokenize, word_tokenize
import pdfplumber
import danger_words
nltk.download('punkt');

#st.write(st.__version__)   

def ShowFlags(flaglist):
    count = 0
    flagcount = len(flaglist)
    if flagcount == 0:
        st.write("No red flags found!")
    else:
        with st.expander("Found "+str(flagcount)+" red flag/s:", True):
            for flag in flaglist:
                count+=1
                st.write(str(count)+". "+flag)
            st.write("\n")

def Display(essay):
    if essay != "":
        sentences = sent_tokenize(essay)
        xgflags = []
        lrflags = []
        xgsflags = []
        wrflags = []
        
        concerning_words = danger_words.GetDangerWords()

        loading = st.progress(0, text = "Loading...")
        i = 1
        for sentence in sentences:
            loading.progress(i/len(sentences), text = "Analyzing sentence "+str(i)+"/"+str(len(sentences))+"...")
            if xgb_predict(sentence) == 1:
                xgflags.append(sentence)
            if lr_predict(sentence) == 1:
                lrflags.append(sentence)
            if xgb_suicide(sentence) == 1:
                xgsflags.append(sentence)

            words = word_tokenize(sentence.lower())
            for word in words:
                if word in concerning_words:
                    wrflags.append(sentence)
            i+=1
            
        loading.progress(1, text="Complete!")
        
        with col1:
            ShowFlags(wrflags)
            
        with col2:
            ShowFlags(lrflags)
        
        with col3:
            ShowFlags(xgflags)
        
        with col4:
            ShowFlags(xgsflags)

        #st.snow()

def GetPDFText(my_pdf):
    try:
        current_pdf = pdfplumber.open(my_pdf)
        data = ""
        pages = current_pdf.pages
        for page in pages:
            data += page.extract_text()
    except:
        data = ""
    return data

st.title("Welcome to :violet[T.E.D.D.Y.]")
st.subheader("Text-based Early Distress Detector for Youth", anchor="welcome-to-t-e-d-d-y")
st.caption("In the sidebar, enter any sufficient amount of text* that is reflective of a person's thoughts: essays, reflections, and chat conversations work best. T.E.D.D.Y. will use artificial intelligence to display sentences that may be a cause for concern.\n :red[T.E.D.D.Y. is not meant to be used as a diagnostic tool] - it is designed to give you a general idea of whether someone in your school or workplace might need more emotional support.")
st.caption("*:violet[A note to our testers:] Our research shows that the sentiments expressed in actual student data are subtle. :red[Thus, arbitrary or made-up statements for testing do not yield good results.] If you do not have actual student data for testing, we recommend searching for sample student essays (e.g., blog posts, college admission essay samples, etc.) online.")
st.write("\n")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Concerning Words Test")
    st.caption("_The following sentences include words that may be a cause for concern._")
    
with col2:
    st.subheader("Potential Struggles Test")
    st.caption("_The writer may be experiencing some struggles that need to be checked._")

with col3:
    st.subheader("Depressive Thoughts Test")
    st.caption("_The writer could be at risk for, or currently experiencing, depression._")
    
with col4:
    st.subheader("Self-Destructive Thoughts Test")
    st.caption("_The writer might be struggling with self-destructive or suicidal thoughts._")

with st.sidebar:
    st.title("Run an essay/conversation through our text analyzer!")
    essay = st.text_input("Copy-paste text here:")
    submit = st.button("Submit Text", on_click=Display(essay))
    uploaded_file = st.file_uploader('Or, upload a PDF file:', type="pdf")
    submit2 = st.button("Submit File", on_click=Display(GetPDFText(uploaded_file)))
    st.write("[Learn more about T.E.D.D.Y!](https://teddytechnovation.wordpress.com/)")
    st.write("[Help us improve!](https://forms.gle/eAYpKmd9udkdFUir6)")
