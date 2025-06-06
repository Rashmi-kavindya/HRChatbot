# chatbot_rules.py

import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')

rules = {
    "leave policy": "Our leave policy includes 14 annual leave days and 10 casual leave days.",
    "salary day": "Salaries are processed on the 25th of every month.",
    "internship salary": "Interns receive their salary on the 10th of every month.",
    "internship duration": "Internships typically last for 6 months.",
    "promotion": "Promotions depend on performance reviews held bi-annually.",
    "contact hr": "You can contact HR at hr@foresight.com or ext 102.",
    "greeting_1": "Hello! How can I assist you today?",
    "greeting_2": "Hi there! Feel free to ask me anything about our HR policies.",
    "greeting_3": "Good to see you! How can I help you today?",
    "greeting_4": "Hey! I'm here to help you with any HR-related questions.",
    "farewell": "Goodbye! Have a great day ahead!"
}

greeting_responses = [
    rules["greeting_1"],
    rules["greeting_2"],
    rules["greeting_3"],
    rules["greeting_4"]
]

stemmer = PorterStemmer()

intent_keywords = {
    "leave policy": ["leave", "vacation"],
    "salary day": ["salary", "pay"],
    "internship duration": ["intern", "duration"],
    "promotion": ["promotion", "review"],
    "contact hr": ["contact", "email"],
    "greeting": ["hi", "hello"],
    "farewell": ["bye", "goodbye"]
}

keyword_map = {}
for intent, keywords in intent_keywords.items():
    for word in keywords:
        keyword_map[stemmer.stem(word)] = intent

def get_hr_response(message):
    message = message.lower()
    tokens = word_tokenize(message)
    stemmed = [stemmer.stem(token) for token in tokens]

    if stemmer.stem("intern") in stemmed and stemmer.stem("salary") in stemmed:
        return rules["internship salary"]

    for word in stemmed:
        if word in keyword_map:
            intent = keyword_map[word]

            if intent == "greeting":
                return random.choice(greeting_responses)

            return rules.get(intent)

    return "I'm sorry, I couldn't understand that. Can you please rephrase?"
