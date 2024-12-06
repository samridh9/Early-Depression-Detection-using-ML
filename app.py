import streamlit as st
import pandas as pd
import numpy as np
from prediction import xgb_predict, lr_predict, xgb_suicide
import nltk
from nltk import sent_tokenize, word_tokenize
import pdfplumber
import danger_words
nltk.download('punkt')
import PyPDF2
from fpdf import FPDF
import danger_words
import markdown
from markdownify import markdownify as md_to_plain
from io import BytesIO
nltk.download('punkt')




st.markdown("""
<style>
.streamlit-expanderHeader {
    color: red; /* Text color */
}
</style>
""", unsafe_allow_html=True)

def ShowFlags(flaglist):
    count = 0
    flagcount = len(flaglist)
    if flagcount == 0:
        st.write(":green[No red flags found!]")
    else:
        with st.expander(f"Found {flagcount} red flag/s:", True):
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

# pdf pdf report generation

def StringToPDF(string):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font(family='DejaVu',fname='DejaVuSansCondensed.ttf', uni = True)
    pdf.add_font(family='DejaVu',fname='DejaVuSansCondensed.ttf', style='B', uni = True)
    pdf.set_font('DejaVu', size=14)

    # Add content

    pdf.multi_cell(190, 10, txt=string)
    
    # Write PDF content to a BytesIO buffer as a string
    pdf_output = pdf.output(dest='S').encode('latin1')  # Convert to bytes with Latin-1 encoding
    return pdf_output


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



def Refresh():
    st.stop()



data=""
def GetPDFText(current_pdf):
    try:
        data = ""
        pages = current_pdf.pages
        for page in pages:
            data += page.extract_text()
    except:
        data = ""
    return data

st.title("Welcome to :violet[DEPTH – Depression Evaluation and Predictive Tracking for Health]")
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

pdf_text=""

with st.sidebar:
    st.title("Express Your Thoughts Here")
    essay = st.text_input("")
    submit = st.button("Submit Text", on_click=Display(essay))
    with st.form("my-form", clear_on_submit=True):
        uploaded_files = st.file_uploader('Upload PDF files here:', type="pdf", accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                st.write(f"Processing: {uploaded_file.name}")
        # Extract text from the PDF
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                pdf_text = "".join(page.extract_text() for page in pdf_reader.pages)

        submitted = st.form_submit_button("Analyze!",on_click=Display(pdf_text))
    st.write("[Immediate Help Resources](https://www.nimh.nih.gov/health/find-help)")


#for uplaod file report generation

string = ""
i = 0
for uploaded_file in uploaded_files:
    i+=1
    current_pdf = pdfplumber.open(uploaded_file)
    string += TEDDY(GetPDFText(current_pdf), str(i) + "/" + str(len(uploaded_files)), current_pdf.stream.name)

if len(uploaded_files) != 0:
    st.download_button(
    label="Download Report",
    data=StringToPDF(string),
    file_name="Report.pdf",
    mime="application/pdf"  
)




#report generation for essays and chatbot
def WriteToStringe(flaglist, title):
    result_string = f"\n**{title}**\n"

    if flaglist:
        for i, flag in enumerate(flaglist, start=1):
            result_string += str(i) + ". " + flag.replace("\n", " ") + "\n"
    else:
        result_string += "No red flags found!"

    result_string += "\n"
    return result_string

def TEDDYe(essay):
    if essay.strip():  # Check if the essay is not empty
        result_string = ""

        # Split the essay into sentences
        sentences = sent_tokenize(essay)

        # Initialize flag lists
        xgflags = []  # Flags for depressive thoughts
        lrflags = []  # Flags for potential struggles
        xgsflags = []  # Flags for self-destructive thoughts
        wrflags = []  # Flags for concerning words

        # Get concerning words
        concerning_words = danger_words.GetDangerWords()

        # Analyze each sentence
        for sentence in sentences:
            # Add flags based on predictions
            if xgb_predict(sentence) == 1:
                xgflags.append(sentence)
            if lr_predict(sentence) == 1:
                lrflags.append(sentence)
            if xgb_suicide(sentence) == 1:
                xgsflags.append(sentence)

            # Check for concerning words
        words = word_tokenize(sentence.lower())
        if any(word in concerning_words for word in words):
            wrflags.append(sentence)

        # Compile the results
        result_string += WriteToStringe(xgsflags, "Self-Destructive Thoughts")
        result_string += WriteToStringe(xgflags, "Depressive Thoughts")
        result_string += WriteToStringe(lrflags, "Potential Struggles")
        result_string += WriteToStringe(wrflags, "Concerning Words")

        return result_string

    else:
        return "The provided essay is empty. Please provide a valid text."


if (len(essay)) != 0:

    Str = TEDDYe(essay)


    st.download_button(
    label="Download Report",
    data=StringToPDF(Str),
    file_name="Report.pdf",
    mime="application/pdf"  
)

#bot button

final_response=""

# Main app logic
def app1():
    # Define fixed questions for the chatbot
    QUESTIONS = [
            "How have you been feeling emotionally over the past few weeks? Please describe in detail.",
            "Can you tell me about any challenges you’ve been facing recently and how they’ve been affecting you?",
            "What does a typical day look like for you, and how do you feel during different parts of the day?",
            "Have you noticed any changes in your sleep, appetite, or energy levels lately? If so, can you describe them?",
            "What activities or people bring you joy or comfort, and have you been able to engage with them recently?",
            "If you could share one thing about how you’re feeling right now, what would it be?",
            "What are your thoughts about the future? Do you feel hopeful or concerned about anything?",
            "Can you describe how you’ve been handling stress or difficult situations recently?",
            "What does support from friends or family look like for you, and have you been receiving it?",
            "If there’s something you wish others understood about how you feel, what would that be?"
    ]

    # Initialize session state variables
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = []
    if "final_response" not in st.session_state:
        st.session_state.final_response = ""
    if "results_ready" not in st.session_state:
        st.session_state.results_ready = False

    # Function to toggle the sidebar
    def toggle_sidebar():
        st.session_state.show_sidebar = not st.session_state.show_sidebar

    # Chatbot logic
    def chatbot():
        st.sidebar.header("Chatbot")
        
        # Display chat history
        for role, content in st.session_state.messages:
            if role == "assistant":
                st.sidebar.markdown(
                    f"""
                        <div style="
                        background-color: #f0f0f0;
                        border-radius: 10px;
                        padding: 10px;
                        margin: 5px 0;
                        border: 1px solid #ddd;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                        color: #333;
                        font-weight: bold;
                        max-width: 100%;
                        ">
                        <strong>Assistant:</strong><br>{content}
                        </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                 st.sidebar.markdown(
                    f"""
                        <div style="
                        background-color: rgb(178 127 250);
                        border-radius: 10px;
                        padding: 10px;
                        margin: 5px 0;
                        white-space: nowrap; 
                        overflow: hidden; 
                        text-overflow: ellipsis; 
                        width: 100%; 
                        display: inline-block;
                        color: black;       
                        border: 1px solid #ddd;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                        color: white;
                        font-weight: bold;
                        max-width: 100%;
                        ">
                        <strong>you:</strong><br>{content}
                        </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Check if there are remaining questions
        if st.session_state.current_question < len(QUESTIONS):
            question = QUESTIONS[st.session_state.current_question]
            
            # Only show the assistant's question if it's new
            if not st.session_state.messages or st.session_state.messages[-1][0] != "assistant":
                st.session_state.messages.append(("assistant", question))

            # Display the current question and capture user input
            st.sidebar.markdown(
                    f"""
                        <div style="
                        background-color: #f0f0f0;
                        border-radius: 10px;
                        padding: 10px;
                        margin: 5px 0;
                        border: 1px solid #ddd;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                        color: #333;
                        font-weight: bold;
                        max-width: 100%;
                        ">
                        <strong>Assistant:</strong><br>{question}
                        </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            prompt = st.sidebar.text_input(
                "Your response",
                key=f"response_input_{st.session_state.current_question}"
            )
            
            if prompt:
                # Save the user's response
                st.session_state.messages.append(("user", prompt))
                st.session_state.user_responses.append(prompt)

                # Move to the next question
                st.session_state.current_question += 1

                # Trigger rerun to show the next question
                st.experimental_rerun()
        else:
            # Chat complete
            st.sidebar.success(":green[Chat complete! Thank you for your responses.]")
            
            # Generate the final response
            if not st.session_state.final_response:
                st.session_state.final_response = ". ".join(st.session_state.user_responses) + "."

            # Show the "Generate Results" button
            if st.sidebar.button("Generate Results"):
                st.session_state.results_ready = True

    # Main app layout
    st.title("Start Your Conversation")

    # Button to toggle chatbot visibility
    if st.button("💬 Open Chat" if not st.session_state.show_sidebar else "❌ Close Chat"):
        toggle_sidebar()

    # Display chatbot in the sidebar if toggled on
    if st.session_state.show_sidebar:
        chatbot()

    # If results are ready, run the Display function and allow report download
    if st.session_state.results_ready:
        Display(st.session_state.final_response)

        str_data = TEDDYe(st.session_state.final_response)
        st.download_button(
            label="Download Report",
            data=StringToPDF(str_data),
            file_name="Report.pdf",
            mime="application/pdf"
        )

# Run the app
if __name__ == "__main__":
    app1()
   

# Initialize session state to track the active app
if "active_app" not in st.session_state:
    st.session_state.active_app = None

# Main app layout


# Create a placeholder for the dynamic content
dynamic_content = st.empty()

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

