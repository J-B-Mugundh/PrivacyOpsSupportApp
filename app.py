from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define research prompt templates for each field
field_prompts = {
    "Privacy Regulations Compliance": "In the context of privacy regulations compliance, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Ethical Data Usage": "As a research assistant specializing in ethical data usage, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Digital Forensics": "Focusing on digital forensics, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Protection Laws": "Regarding data protection laws, answer my questions in a comprehensive and informative way, using credible sources. ",
    "GDPR Compliance": "For inquiries about GDPR compliance, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Cybersecurity Ethics": "In the context of cybersecurity ethics, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Information Security Policies": "Regarding information security policies, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Types of Cases": "In relation to different types of cases, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Usage": "Concerning data usage, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Needed to be Provided": "On the topic of data needed to be provided for different cases, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Storage": "Regarding how data is stored in case filing, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Security Measures": "For questions about data security measures, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Breach Responses": "On the subject of data breach responses, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Anonymization Techniques": "In the context of data anonymization techniques, answer my questions in a comprehensive and informative way, using credible sources. ",
    "Data Encryption Methods": "Regarding data encryption methods, answer my questions in a comprehensive and informative way, using credible sources. ",
}

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question, field):
    prompt = field_prompts[field] + question
    response = chat.send_message(prompt, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="PrivacyOps Support Assistant")

st.header("PrivacyOps Support Assistant")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Add field selection dropdown
selected_field = st.selectbox("Select Field:", list(field_prompts.keys()))

input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    response = get_gemini_response(input_text, selected_field)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
    st.markdown("---") 

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
