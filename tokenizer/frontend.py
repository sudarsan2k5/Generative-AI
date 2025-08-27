# Step1: Setup Streamlit
import streamlit as st
import requests



BACKEND_URL = "http://0.0.0.0:8000/ask"

st.set_page_config(
    page_title="AI Social Media Assistant",
    layout="wide"
)
st.title("🚀 SafeSpace - AI Social Media Assistant")

#Initialie chat History to ask question
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#Step2: User is able to ask Question

user_input = st.chat_input("What would you like to post on social media today?")

if user_input:
    #Append user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input }
    )


    try:
        response = requests.post(BACKEND_URL, json={"message": user_input})
        
        if response.status_code == 200:
            response_data = response.json()
            content = f'{response_data["response"]} WITH TOOL: [{response_data["tool_called"]}]'
        else:
            content = f"❌ Backend error (status {response.status_code}): {response.text}"
            
    except requests.exceptions.JSONDecodeError:
        content = f"❌ Backend returned invalid response: {response.text}"
    except Exception as e:
        content = f"❌ Connection error: {str(e)}"

    st.session_state.chat_history.append({"role": "assistant", "content": content})

#Step3:Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])