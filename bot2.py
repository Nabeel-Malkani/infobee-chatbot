# Meet InfoBee: your friend
import nltk
import warnings
from flask import session
from pymongo import MongoClient
from intents import Introduce_Ans, GREETING_INPUTS, GREETING_RESPONSES, Basic_Q, Basic_Ans, Basic_Om, Basic_AnsM, fev, feve_r


warnings.filterwarnings("ignore")
import random
import string  # to process standard python strings

client = MongoClient('mongodb+srv://infobee:InfoBee123@diseaseprediction.e1ihw.mongodb.net/myFirstDatabase'
                     '?retryWrites=true&w=majority')



f = open('dataset.txt', 'r', errors='ignore')
checkpoint = "./chatbot_weights.ckpt"


raw = f.read()
nltk.download('punkt')  # first-time use only
nltk.download('wordnet')  # first-time use only
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

sent_tokens[:2]

word_tokens[:5]

lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))




# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Checking for Basic_Q
def basic(sentence):
    for word in Basic_Q:
        new_sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        if new_sentence.lower() == word:
            return Basic_Ans


def fever(sentence):
    for word in fev:
        new_sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        if new_sentence.lower() == word:
            return feve_r


# Checking for Basic_QM
def basicM(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in Basic_Om:
        new_sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        if new_sentence.lower() == word:
            return Basic_AnsM


# Checking for Introduce
def IntroduceMe(sentence):
    return random.choice(Introduce_Ans)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)

    vals = cosine_similarity(tfidf[-1], tfidf)

    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = robo_response + "I am sorry! I don't understand you (میں معافی چاہتا ہوں ! مجھےآپ کی بات سمجھ نہیں آئی)"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
    sent_tokens.remove(user_response)
    return robo_response



def chat(user_response):
    user_response = user_response.lower()
    keyword = " module "
    keywordone = " module"
    keywordsecond = "module "

    if user_response != 'bye':

        if user_response == 'thanks' or user_response == 'thank you':
            flag = False
            return "If your symptoms get worse please consult a doctor immediately. Bye! take care (اگر آپ کی علامات زیادہ خراب ہوں تو فوراً ڈاکٹر سے رجوع کریں۔ اپنا خیال رکھیں۔ الله حافظ)"
        elif user_response == 'good bye' or user_response == 'goodbye' or user_response == 'allah hafiz' or user_response == 'exit':
            flag = False
            return "If your symptoms get worse please consult a doctor immediately. Bye! take care (اگر آپ کی علامات زیادہ خراب ہوں تو فوراً ڈاکٹر سے رجوع کریں۔ اپنا خیال رکھیں۔ الله حافظ)"
        elif basicM(user_response) is not None:
            if session['user'] != 'guest':
                db = client.get_database('diseasepred')
                collection = db.user_record
                record = {
                    'user_name': session['user'],
                    'input': user_response,
                    'output': basicM(user_response)
                }
                collection.insert_one(record)

                # print(basicM(user_response))
            return basicM(user_response)
        else:
            if (user_response.find(keyword) != -1 or user_response.find(keywordone) != -1 or user_response.find(
                    keywordsecond) != -1):
                # print("ROBO: ",end="")
                # print(responseone(user_response))
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'input': user_response,
                        'output': responseone(user_response)
                    }
                    collection.insert_one(record)

                #print(responseone(user_response))
                return responseone(user_response)
                sent_tokensone.remove(user_response)
            elif greeting(user_response) is not None:
                # print("ROBO: "+greeting(user_response))
                if session['user'] != 'guest':

                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'input': user_response,
                        'output': greeting(user_response)
                    }
                    collection.insert_one(record)
               # print(greeting(user_response))
                return greeting(user_response)
            elif (user_response.find("your name") != -1 or user_response.find(" your name") != -1 or user_response.find(
                    "your name ") != -1 or user_response.find(" your name ") != -1):
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'input': user_response,
                        'output': IntroduceMe(user_response)
                    }
                    collection.insert_one(record)
                #print(IntroduceMe(user_response))
                return IntroduceMe(user_response)
            elif basic(user_response) is not None:
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'input': user_response,
                        'output': basic(user_response)
                    }
                    collection.insert_one(record)
                #print(basic(user_response))
                return basic(user_response)
            elif fever(user_response) is not None:
                if session['user'] != 'guest':
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'input': user_response,
                        'output': fever(user_response)
                    }
                    collection.insert_one(record)
                #print(fever(user_response))
                return fever(user_response)
            else:
                resultresponse = response(user_response)
                print(resultresponse)
                if session['user'] != 'guest':

                    print('The user is not guest \n')
                    #print(response(user_response))
                    db = client.get_database('diseasepred')
                    collection = db.user_record
                    record = {
                        'user_name': session['user'],
                        'input': user_response,
                        'output': resultresponse
                    }
                    collection.insert_one(record)
                # print("ROBO: ",end="")
                # print(response(user_response))

                return resultresponse
                sent_tokens.remove(user_response)

    else:
        flag = False
        # print("ROBO: Bye! take care..")
        return "If your symptoms get worse please consult a doctor immediately. Bye! take care (اگر آپ کی علامات زیادہ خراب ہوں تو فوراً ڈاکٹر سے رجوع کریں۔ اپنا خیال رکھیں۔ الله حافظ)"
