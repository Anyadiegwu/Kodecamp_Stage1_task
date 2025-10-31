import os
import google.generativeai as genai
import requests


def get_banned_words():
    url = "https://raw.githubusercontent.com/Anyadiegwu/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/90aa689f56d5390afe673749d06f9eed9b7a4b54/en"
    response = requests.get(url)
    response.raise_for_status()
    words = set(response.text.strip().split("\n"))
    return words

banned_words = get_banned_words()

def has_banned_words(text: str) -> bool:
    lower = text.lower()
    return any(word in lower for word in banned_words)

def redact_banned(text: str) -> str:
    words = text
    for word in banned_words:
        words = words.replace(word, "[REDACTED]")
        words = words.replace(word.capitalize(), "[REDACTED]")
        words = words.replace(word.upper(), "[REDACTED]")
    return words    

genai.configure(
    api_key = os.getenv("AIzaSyCDss7sva5H8UVmWJhcjaj-yM5zqf7TtZ8")
)

model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    system_instruction = (
        "You are a helpful assistant who speaks clearly and politely."
        "Answer in plain text only. "
        "Never use Markdown, bold, italics, headers, lists, or code blocks."
    )
)

user_prompt = input("Enter your prompt: ")


if has_banned_words(user_prompt):
    print("Your prompt contains inappropriate language and cannot be processed.")
    user_prompt = redact_banned(user_prompt)
    print("Redacted Prompt: ", user_prompt)
    exit()
else:
    response = model.generate_content(user_prompt)
    ai_text = response.text
    if has_banned_words(ai_text):
        safe_text = redact_banned(ai_text)
        print("The Generated response contained inappropriate language. Here is the Modified text.")
        print("Modified Response: ", safe_text)
    else:
        print("\nGenerated Response: ")
        print(response.text)