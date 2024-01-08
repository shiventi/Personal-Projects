import os
import sys
import json
import nltk
import random
import tflearn
import numpy as np
import socketserver
import tensorflow as tf
from nltk import LancasterStemmer
from chatbot_dependencies import *
from face_recog import *
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs

nltk.download('punkt')

def load_blenderbot_model():
    tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
    model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
    return tokenizer, model

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [LancasterStemmer().stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

def load_or_train_tflearn_model(training, output):
    try:
        model = tflearn.DNN(tflearn.regression(tflearn.fully_connected(tflearn.input_data(shape=[None, len(training[0])]), 8),
                                       tflearn.fully_connected(tflearn.dropout(tflearn.net, 0.8), 8),
                                       tflearn.fully_connected(tflearn.net, len(output[0]), activation="softmax")))

        model.load("model.tflearn")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = train_tflearn_model(training, output)

    return model

def train_tflearn_model(training, output):
    tf.compat.v1.reset_default_graph()
    net = tflearn.input_data(shape=[None, len(training[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.dropout(net, 0.8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)

    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')

    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=False)

    sys.stdout = original_stdout

    model.save("model.tflearn")

    return model

def classify_intent(input_text):
    input_text_lower = input_text.lower()
    if "question" in input_text_lower:
        return "questions", 1.0
    else:
        return "default", 0.8

def add_input_to_tag(text, tag):
    with open("intents.json", "r") as file:
        intents_data = json.load(file)["intents"]

    input_lower = text.lower()
    tag_found = False

    for intent in intents_data:
        if intent["tag"] == tag:
            tag_found = True
            if input_lower not in map(str.lower, intent["patterns"]):
                intent["patterns"].append(input_lower)
                break

    if not tag_found:
        new_intent = {"tag": tag, "patterns": [input_lower], "responses": []}
        intents_data.append(new_intent)

    with open("intents.json", "w") as file:
        json.dump({"intents": intents_data}, file, indent=4)


def chat(input_text):
    try:
        with open("intents.json") as file:
            data = json.load(file)["intents"]

        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [LancasterStemmer().stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = [1 if w in doc else 0 for w in words]

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = np.array(training)
        output = np.array(output)

        model = load_or_train_tflearn_model(training, output)

        results = model.predict([bag_of_words(input_text, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        confidence = results[0][results_index] * 100

        if confidence >= 90:
            for intent in data:
                if intent['tag'] == tag:
                    if intent["tag"] == "questions":
                        if not is_personal_question(input_text.lower()):
                            abcde = web_search("https://www.google.com/search", input_text.lower(), "span", "hgKElc")
                            if abcde is None or abcde == "":
                                return str(web_search("https://www.google.com/search", input_text.lower(), "div", "PZPZlf hb8SAc"))
                            else:
                                return str(abcde)
                        else:
                            tokenizer, blenderbot_model = load_blenderbot_model()
                            inputs = tokenizer(input_text, return_tensors="pt")
                            res = blenderbot_model.generate(**inputs)
                            output = tokenizer.decode(res[0], skip_special_tokens=True)
                            return str(output)

                    else:
                        responses = intent['responses']
                        add_input_to_tag(input_text, tag)
                        return random.choice(responses)
        else:
            tokenizer, blenderbot_model = load_blenderbot_model()
            inputs = tokenizer(input_text, return_tensors="pt")
            res = blenderbot_model.generate(**inputs)
            output = tokenizer.decode(res[0], skip_special_tokens=True)
            return str(output)

    except Exception as e:
        print(f"Error in chat function: {e}")
        return "An error occurred while processing your request."

class WebChatHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        if 'user_input' in params:
            user_input = params['user_input'][0]

            bot_response = chat(user_input)
            print(bot_response)

            if isinstance(bot_response, str):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes(bot_response, 'utf-8'))
            else:
                print("Error: bot_response is not a string")

                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()

                self.wfile.write(bytes("Internal Server Error", 'utf-8'))
        else:
            print("Error: 'user_input' not found in params")

            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("Bad Request", 'utf-8'))

if __name__ == "__main__":
    port = 8001
    try:
        with socketserver.TCPServer(("", port), WebChatHandler) as httpd:
            print(f"Serving on port {port}")
            open_incognito_window("Chrome")
            url_1 = f"http://127.0.0.1:{port}/webchat.html"
            open_in_incognito_tab("Google Chrome", url_1)
            httpd.serve_forever()
    except OSError:
        with socketserver.TCPServer(("", port+1), WebChatHandler) as httpd:
            print(f"Serving on port {port+1}")
            open_incognito_window("Chrome")
            url_1 = f"http://127.0.0.1:{port+1}/webchat.html"
            open_in_incognito_tab("Google Chrome", url_1)
            httpd.serve_forever()
