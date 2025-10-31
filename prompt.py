import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv
import re
import streamlit as st



def get_api_key():
    try:
        load_dotenv()
        API_KEY = os.getenv("GEMINI_API_KEY")
        if API_KEY:
            return API_KEY
    except Exception:
        pass 
    
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]


GEMINI_API_KEY = get_api_key()


@st.cache_data(ttl=3600)
def get_banned_words():
    try:
        url = "https://raw.githubusercontent.com/Anyadiegwu/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/90aa689f56d5390afe673749d06f9eed9b7a4b54/en"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        words = set(response.text.strip().split("\n"))
        return words
    except Exception as e:
        print(f"Error fetching banned words list: {e}")
        return {"badword", "inappropriate", "blockme"}

banned_words = get_banned_words()

def has_banned_words(text: str) -> bool:
    lower = text.lower()
    return any(word in lower for word in banned_words)

def redact_banned(text: str) -> str:
    for word in banned_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("[REDACTED]", text)
    return text
    # words = text
    # for word in banned_words:
    #     words = words.replace(word, "[REDACTED]")
    #     words = words.replace(word.capitalize(), "[REDACTED]")
    #     words = words.replace(word.upper(), "[REDACTED]")
    # return words    


genai.configure(
    api_key = GEMINI_API_KEY
)

model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    system_instruction = (
        "You are a helpful assistant who speaks clearly and politely."
        "Answer in plain text only. "
        "Never use Markdown, bold, italics, headers, lists, or code blocks."
    )
)

#Streamlit Interface
st.title("AI Moderator")
st.write("Enter a prompt — unsafe words are blocked.")


# user_prompt = input("Enter your prompt: ")
user_prompt = st.text_area("Enter your prompt here:", height=100)


if st.button("Generate Response"):
    if has_banned_words(user_prompt):
        # print("Your prompt contains inappropriate language and cannot be processed.")
        st.write("Your prompt contains inappropriate language and cannot be processed.")
        user_prompt = redact_banned(user_prompt)
        st.write("Redacted Prompt:" , user_prompt)
        # print("Redacted Prompt: ", user_prompt)
    else:
        with st.spinner('Generating response...'):
            try:
                response = model.generate_content(user_prompt)
                ai_text = response.text
                
                if has_banned_words(ai_text):
                    safe_text = redact_banned(ai_text)
                    # print("The Generated response contained inappropriate language. Here is the Modified text.")
                    # print("Modified Response: ", safe_text)
                    st.write("The Generated response contained inappropriate language. Here is the Modified text.")
                    st.write("Modified Response: ", safe_text)
                else:
                    st.success("Generated Response:")
                    st.write(response.text)
                    # print("\nGenerated Response: ")
                    # print(response.text)
            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")
                # print(f"An error occurred while generating content: {e}")