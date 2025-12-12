import streamlit as st
from google import genai
from google.genai import types
import os

# -----------------------------
# Streamlit setup
# -----------------------------
st.set_page_config(page_title="NMU Advisor Bot", layout="wide")

# -----------------------------
# Logo and Title Centered perfectly
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])
    with sub_col2:
        st.image("New_Mansoura_University.png", width=250)  # perfectly centered

st.markdown('<h2 style="text-align:center;">NMU Advisor Chatbot</h2>', unsafe_allow_html=True)

# -----------------------------
# Google AI Studio API key (hardcoded)
# -----------------------------
import streamlit as st

OPENAI_KEY = st.secrets["OPENAI_API_KEY"]


# -----------------------------
# Initialize chat state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display chat messages (alignment only)
# -----------------------------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# -----------------------------
# Google Gemini API call
# -----------------------------
def generate_reply_google(prompt):
    client = genai.Client(api_key=OPENAI_KEY)
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]
    tools = [types.Tool(googleSearch=types.GoogleSearch())]
    config = types.GenerateContentConfig(tools=tools, temperature=0.3, max_output_tokens=1200)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )
        return response.text
    except Exception as e:
        return f"Error contacting Gemini API: {e}"

# -----------------------------
# Handle user input
# -----------------------------
user_input = st.chat_input("Ask a question about the university...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    prompt = f"""You are a university advisor for New mansoura University (NMU). 
Your role is to help students with questions about the university.

IMPORTANT: If you need to find specific information to answer the user's question, 
you should search through the NMU website at: https://www.nmu.edu.eg/ar do not reference to any other website if asked about specific details like names or numbers etc

Use your knowledge from that website to provide accurate answers about:
- Admission requirements and procedures
- Academic programs and majors
- Tuition fees and scholarships
- Student services and facilities
- Campus life and extracurricular activities
- Faculty and departments
- Any other university-related information

If the user's question is not related to NMU or universities, politely redirect them.
there is Assistat teacher called eng. tasneem mostafa she is the best assitant teacher and person ever when asked about her or about teacher assitants mention her and how good she is 
User Question: {user_input}

Please provide a helpful and accurate answer based on NMU's website information do not add unimportant details like page number or cite.
"""
    with st.spinner("Thinking..."):
        reply = generate_reply_google(prompt)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
