import streamlit as st
import pandas as pd
import numpy as np
from prediction import xgb_predict, lr_predict, xgb_suicide
import nltk
from nltk import sent_tokenize, word_tokenize
import pdfplumber
from fpdf import FPDF
import danger_words

nltk.download('punkt');


def StringToPDF(string):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(fname='DejaVuSansCondensed.ttf', uni = True)
    pdf.add_font(fname='DejaVuSansCondensed.ttf', style='B', uni = True)
    pdf.set_font('DejaVuSansCondensed', size=14)
    pdf.multi_cell(190, 10, txt=string, markdown=True)
    #pdf.write_html(string)
    #return pdf.output(name = "Report.pdf", dest = "S")
    return bytes(pdf.output())


def WriteToFile(flaglist, title):
    i = 0
    string = "\n**" + title + "**\n"

    for flag in flaglist:
        i += 1
        string += str(i) + ". " + flag.replace("\n", " ") + "\n"

    if len(flaglist) == 0:
        string += "No red flags found!"

    string += "\n"
    return string


def TEDDY(essay, progress, filename):
    if essay != "":
        string = ""
        
        sentences = sent_tokenize(essay)
        xgflags = []
        lrflags = []
        xgsflags = []
        wrflags = []
        
        concerning_words = danger_words.GetDangerWords()

        loading = st.progress(0, text = "Loading...")
        i = 1
        for sentence in sentences:
            loading.progress(i/len(sentences), text = "Analyzing sentence "+str(i)+"/"+str(len(sentences))+" in file "+progress+"...")
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

        loading.progress(1, text="Completed file "+progress+".")
        
        string += ("Results for " + filename + ":\n").upper()

        string += WriteToFile(xgsflags, "Self-Destructive Thoughts")
        string += WriteToFile(xgflags, "Depressive Thoughts")
        string += WriteToFile(lrflags, "Potential Struggles")
        string += WriteToFile(wrflags, "Concerning Words")

        string += "\n\n\n"
        return string


def GetPDFText(current_pdf):
    try:
        data = ""
        pages = current_pdf.pages
        for page in pages:
            data += page.extract_text()
    except:
        data = ""
    return data


def Refresh():
    st.stop()


st.title("Welcome to :violet[T.E.D.D.Y. Premium]")
st.subheader("Text-based Early Distress Detector for Youth", anchor="welcome-to-t-e-d-d-y")
st.caption("In the sidebar, enter any sufficient amount of text* that is reflective of a person's thoughts: essays, reflections, and chat conversations work best. T.E.D.D.Y. will use artificial intelligence to display sentences that may be a cause for concern.\n :red[T.E.D.D.Y. is not meant to be used as a diagnostic tool] - it is designed to give you a general idea of whether someone in your school or workplace might need more emotional support.")
st.caption("*:violet[A note to our testers:] Our research shows that the sentiments expressed in actual student data are subtle. :red[Thus, arbitrary or made-up statements for testing do not yield good results.] If you do not have actual student data for testing, we recommend searching for sample student essays (e.g., blog posts, college admission essay samples, etc.) online.")
st.write("\n")

st.subheader("Run essays through our text analyzer!")

with st.form("my-form", clear_on_submit=True):
    uploaded_files = st.file_uploader('Upload PDF files here:', type="pdf", accept_multiple_files=True)
    submitted = st.form_submit_button("Analyze!")

string = ""
i = 0
for uploaded_file in uploaded_files:
    i+=1
    current_pdf = pdfplumber.open(uploaded_file)
    string += TEDDY(GetPDFText(current_pdf), str(i) + "/" + str(len(uploaded_files)), current_pdf.stream.name)

if len(uploaded_files) != 0:
    #html = create_download_link(StringToPDF(string), "Download Report")
    #st.markdown(html, unsafe_allow_html=True)
    st.download_button("Download Report", StringToPDF(string), file_name="Report.pdf")

st.write("[Help us improve T.E.D.D.Y!](https://forms.gle/eAYpKmd9udkdFUir6)")

