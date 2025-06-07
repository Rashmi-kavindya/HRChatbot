# # chatbot_rules.py

# import nltk
# import random
# from nltk.tokenize import word_tokenize
# # from nltk.stem import PorterStemmer
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import wordnet
# from textblob import TextBlob
# from sentence_transformers import SentenceTransformer, util

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# lemmatizer = WordNetLemmatizer()
# model = SentenceTransformer('all-MiniLM-L6-v2')

# rules = {
#     "leave policy": "Our leave policy includes 14 annual leave days and 10 casual leave days.",
#     "salary day": "Salaries are processed on the 25th of every month.",
#     "internship salary": "Interns receive their salary on the 10th of every month.",
#     "internship duration": "Internships typically last for 6 months.",
#     "promotion": "Promotions depend on performance reviews held bi-annually.",
#     "contact hr": "You can contact HR at hr@foresight.com or ext 102.",
#     "greeting_1": "Hello! How can I assist you today?",
#     "greeting_2": "Hi there! Feel free to ask me anything about our HR policies.",
#     "greeting_3": "Good to see you! How can I help you today?",
#     "greeting_4": "Hey! I'm here to help you with any HR-related questions.",
#     "farewell": "Goodbye! Have a great day ahead!"
# }

# greeting_responses = [
#     rules["greeting_1"],
#     rules["greeting_2"],
#     rules["greeting_3"],
#     rules["greeting_4"]
# ]

# # stemmer = PorterStemmer()

# intent_keywords = {
#     "leave policy": ["leave", "vacation"],
#     "salary day": ["salary", "pay"],
#     "internship duration": ["intern", "duration"],
#     "promotion": ["promotion", "review"],
#     "contact hr": ["contact", "email"],
#     "greeting": ["hi", "hello"],
#     "farewell": ["bye", "goodbye"]
# }

# # keyword_map = {}
# # for intent, keywords in intent_keywords.items():
# #     for word in keywords:
# #         keyword_map[stemmer.stem(word)] = intent
# # Create synonym-expanded keyword map
# def get_synonyms(word):
#     synonyms = set()
#     for syn in wordnet.synsets(word):
#         for lemma in syn.lemmas():
#             synonyms.add(lemma.name().lower())
#     return synonyms

# keyword_map = {}
# for intent, keywords in intent_keywords.items():
#     for word in keywords:
#         for synonym in get_synonyms(word):
#             keyword_map[synonym] = intent

# # Spell correction
# def correct_spelling(text):
#     return str(TextBlob(text).correct())

# # Semantic similarity fallback
# def find_similar_intent(user_input):
#     input_embedding = model.encode(user_input, convert_to_tensor=True)
#     best_score = 0.0
#     best_intent = None

#     for intent in rules:
#         intent_embedding = model.encode(intent, convert_to_tensor=True)
#         similarity = util.cos_sim(input_embedding, intent_embedding).item()

#         if similarity > best_score:
#             best_score = similarity
#             best_intent = intent

#     if best_score > 0.6:
#         return rules[best_intent]
#     return None

# def get_hr_response(message):
#     message = correct_spelling(message.lower())
#     tokens = word_tokenize(message)
#     # stemmed = [stemmer.stem(token) for token in tokens]

#     # if stemmer.stem("intern") in stemmed and stemmer.stem("salary") in stemmed:
#     #     return rules["internship salary"]

#     lemmas = [lemmatizer.lemmatize(token) for token in tokens]

#     # Special rule for intern+salary
#     if "intern" in lemmas and "salary" in lemmas:
#         return rules["internship salary"]

#     # for word in stemmed:
#     #     if word in keyword_map:
#     #         intent = keyword_map[word]

#     #         if intent == "greeting":
#     #             return random.choice(greeting_responses)

#     #         return rules.get(intent)

#     for lemma in lemmas:
#         if lemma in keyword_map:
#             intent = keyword_map[lemma]
#             if intent == "greeting":
#                 return random.choice(greeting_responses)
#             return rules[intent]


#     similar = find_similar_intent(message)
#     if similar:
#         return similar

#     return "I'm sorry, I couldn't understand that. Can you please rephrase?"

# chatbot_rules.py

import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from textblob import TextBlob
from sentence_transformers import SentenceTransformer, util
from functools import lru_cache

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize tools
lemmatizer = WordNetLemmatizer()
model = SentenceTransformer('all-MiniLM-L6-v2')

# Rule-based responses
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

# Greeting pool
greeting_responses = [
    rules["greeting_1"],
    rules["greeting_2"],
    rules["greeting_3"],
    rules["greeting_4"]
]

# Intent-related keywords
intent_keywords = {
    "leave policy": ["leave", "vacation"],
    "salary day": ["salary", "pay"],
    "internship duration": ["intern", "duration"],
    "promotion": ["promotion", "review"],
    "contact hr": ["contact", "email"],
    "greeting": ["hi", "hello"],
    "farewell": ["bye", "goodbye"]
}

# Cache synonyms to improve performance
@lru_cache(maxsize=1000)
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

# Build keyword map with synonyms
keyword_map = {}
for intent, keywords in intent_keywords.items():
    for word in keywords:
        for synonym in get_synonyms(word):
            keyword_map[synonym] = intent

# Spell correction with fallback
def correct_spelling(text):
    try:
        return str(TextBlob(text).correct())
    except Exception:
        return text

# Semantic fallback using sentence similarity
def find_similar_intent(user_input):
    input_embedding = model.encode(user_input, convert_to_tensor=True)
    best_score = 0.0
    best_intent = None

    for intent in rules:
        intent_embedding = model.encode(intent, convert_to_tensor=True)
        similarity = util.cos_sim(input_embedding, intent_embedding).item()

        if similarity > best_score:
            best_score = similarity
            best_intent = intent

    if best_score > 0.6:
        return rules[best_intent]
    return None

# Main response function
def get_hr_response(message):
    # Clean and correct spelling
    message = correct_spelling(message.lower())

    # Tokenize and lemmatize
    tokens = word_tokenize(message)
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]

    # Special case - intern + salary
    if "intern" in lemmas and "salary" in lemmas:
        return rules["internship salary"]

    # Keyword/synonym intent matching
    for lemma in lemmas:
        if lemma in keyword_map:
            intent = keyword_map[lemma]
            if intent == "greeting":
                return random.choice(greeting_responses)
            return rules[intent]

    # Semantic fallback
    similar = find_similar_intent(message)
    if similar:
        return similar

    # Fallback if nothing matched
    return "I'm sorry, I couldn't understand that. Can you please rephrase?"
