import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
import io
import PyPDF2 as pdf



#  environment variables
load_dotenv()

# frontend of streamlit
st.set_page_config(
    page_title="TIU EXAM HELPER",
    page_icon=":clipboard:",  # cute emoji
    initial_sidebar_state="expanded",
    layout="wide", 
)


st.title("TIU EXAM HELPER")

st.markdown("Jan Hit me jaari\n")
st.markdown("Puch jo puchna ha \n")


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# model setup
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_gemini_response(input_text, pdf_text, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input_text, pdf_text, prompt])
    return response.text


def input_pdf_setup(uploaded_file):
  if uploaded_file is not None:
      pdf_reader = pdf.PdfReader(uploaded_file)
      pdf_text = ""
      for page_num in range(len(pdf_reader.pages)):
          page = pdf_reader.pages[page_num]
          pdf_text += page.extract_text()

      return pdf_text
  else:
        raise FileNotFoundError("No file uploaded")



input_text=st.text_area("Question dal : ",key="input")
uploaded_file=st.file_uploader("colledge ka notes dal ",type=["pdf"])


if uploaded_file is not None:
    st.write("PDf upload hogaya..")


submit1 = st.button("Answer bata Guru! from pdf")


input_prompt1 = """
 You are a skill teacher ,read the pdf text , understand it and give the answer which is asked in "Question dal" input area 
 , give most accurate answer after reading and understanding the question. if answer or related term not in pdf tell no no anwsers in pdf , please search at search bar
 if pdf not uploaded then also give answer , give answer must 
"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        with st.spinner("Generating response..."):
          response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Pdf Upload karbe baklol")


        
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role



if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])




# chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)


user_prompt = st.chat_input("Pucho jo puchna ha kahi se bhi , apun ko sab aata ha...")
if user_prompt:
    
    
    st.chat_message("user").markdown(user_prompt)

    # message gemini ko bhejega for result
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # will show result
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
